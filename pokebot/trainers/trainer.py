##########################
# Author: Neil Acharya 
# 
# Generic Model Definition
##########################
from abc import ABC
from typing import Optional, List
from wandb import log

import poke_env
from poke_env.player.random_player import RandomPlayer
from poke_env.player.player import Player

from rl.agents.dqn import DQNAgent
from rl.memory import SequentialMemory
from rl.policy import LinearAnnealedPolicy, EpsGreedyQPolicy
from tensorflow.keras.optimizers import Adam

from .utils import dqn_evaluation, dqn_training, play_against_human
from ..bots.player_factory import PlayerFactory
from ..models.dqn import DQNModel
from ..bots.bot import BotPlayer


class Trainer(ABC):

    def __init__(self, player: BotPlayer, model: DQNModel, policy_dict: dict, agent_dict: dict, **kwargs):
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

    async def battle_human(self, opponent: str):
        play_against_human(self.player,
                           opponent=opponent,
                           env_algorithm=dqn_evaluation,
                           env_algorithm_kwargs={"dqn": self.agent, "nb_episodes": 1})


class SimpleDQNTrainer(Trainer):

    def __init__(self, player, model, policy_dict, agent_dict, opponent=RandomPlayer(battle_format="gen8randombattle"),
                 nbsteps=100000, **kwargs):
        super().__init__(player, model, policy_dict, agent_dict, **kwargs)

        self.opponent = opponent if isinstance(opponent, Player) else PlayerFactory.get_player(**opponent)
        self.nbsteps = nbsteps

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

        self.agent.compile(Adam(lr=0.0003), metrics=["mse"])

    async def train(self, opponent: Optional[Player] = None, nb_steps=None):

        if not opponent:
            opponent = self.opponent

        if not nb_steps:
            nb_steps = self.nbsteps

        # Training
        self.player.play_against(
            env_algorithm=dqn_training,
            opponent=opponent,
            env_algorithm_kwargs={"dqn": self.agent, "nb_steps": nb_steps},
        )

    async def evaluate(self, playerList: List[Player], logger=log):
        for p in playerList:
            # Evaluation
            print(f"Results against player: {p.username}")
            self.player.play_against(
                env_algorithm=dqn_evaluation,
                opponent=p,
                env_algorithm_kwargs={"dqn": self.agent, "nb_episodes": 100, "logger": logger},
            )
