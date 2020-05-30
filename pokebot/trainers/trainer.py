##########################
# Author: Neil Acharya 
# 
# Generic Model Definition
##########################
from abc import ABC
from typing import Optional, List

from poke_env.player.random_player import RandomPlayer
from poke_env.player.player import Player

from rl.agents.dqn import DQNAgent
from rl.memory import SequentialMemory
from rl.policy import LinearAnnealedPolicy, EpsGreedyQPolicy
from tensorflow.keras.optimizers import Adam

from .utils import dqn_evaluation, dqn_training
from ..models.dqn import Model
from ..bots.bot import BotPlayer


class Trainer(ABC):
    
    def __init__(self, player: BotPlayer, model: Model, policy_dict: dict, agent_dict: dict):
        super().__init__()

        self.player = player

        self.model = model

        self.memory = SequentialMemory(limit=10000, window_length=1)
        self.policy = None
        self.agent = None

        self.init_policy(policy_dict)

        self.init_agent(agent_dict)

    def init_policy(self, policy_dict):
        raise NotImplementedError

    def init_agent(self, agent_dict):
        raise NotImplementedError

    def load_agent_from_file(self, fp):
        self.agent.load_weights(fp)


class SimpleDQNTrainer(Trainer):

    def __init__(self, player, model, policy_dict, agent_dict):
        super().__init__(player, model, policy_dict, agent_dict)

    def init_policy(self, policy_dict):
        self.policy = LinearAnnealedPolicy(
            EpsGreedyQPolicy(),
            **policy_dict
        )

    def init_agent(self, agent_dict):

        self.agent = DQNAgent(
            model=self.model.model,
            policy=self.policy,
            memory=self.memory,
            enable_double_dqn=True,
            **agent_dict
        )

        self.agent.compile(Adam(lr=0.00025), metrics=["mae"])

    async def train(self, opponent: Optional[Player] = RandomPlayer(battle_format="gen8randombattle")):

        # Training
        self.player.play_against(
            env_algorithm=dqn_training,
            opponent=opponent,
            env_algorithm_kwargs={"dqn": self.agent, "nb_steps": 100000},
        )

    async def evaluate(self, playerList: List[Player]):

        for p in playerList:
            # Evaluation
            print(f"Results against player: {p.username}")
            self.player.play_against(
                env_algorithm=dqn_evaluation,
                opponent=p,
                env_algorithm_kwargs={"dqn": self.agent, "nb_episodes": 100},
            )
