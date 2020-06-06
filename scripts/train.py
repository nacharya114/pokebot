import dotmap
import json
import sys
import asyncio
import importlib
import nest_asyncio
nest_asyncio.apply()

from poke_env.player.random_player import RandomPlayer
from poke_env.player_configuration import PlayerConfiguration
from poke_env.player.baselines import MaxBasePowerPlayer, SimpleHeuristicsPlayer

from pokebot import BotPlayer


async def train(hparams, fp):
    p_dict = hparams.policy
    a_dict = hparams.agent

    SEngine = importlib.import_module('pokebot.bots.state_engine')
    se_clazz = getattr(SEngine, hparams.state_engine)
    se_dict = hparams.se_params if hparams.se_params else {}

    player = BotPlayer(
        player_configuration=PlayerConfiguration("test", None),
        state_engine=se_clazz(**se_dict)
    )

    m_lib = importlib.import_module('pokebot.models')
    m_clazz = getattr(m_lib, hparams.model)
    m_dict = hparams.model_params if hparams.model_params else {}

    model = m_clazz(player, **m_dict)

    train_lib = importlib.import_module('pokebot.trainers.trainer')
    t_class = getattr(train_lib, hparams.trainer)
    t_dict = hparams.trainer_params if hparams.trainer_params else {}
    trainer = t_class(player, model, p_dict, a_dict, **t_dict)

    await trainer.train()

    opponents = [RandomPlayer(battle_format="gen8randombattle"),
                 MaxBasePowerPlayer(battle_format="gen8randombattle"),
                 SimpleHeuristicsPlayer(battle_format="gen8randombattle")]

    print("Beginning Eval")

    await trainer.evaluate(opponents)

    trainer.agent.save_weights(fp)

if __name__ == '__main__':

    if len(sys.argv) < 3:
        raise Exception("Needs hparams path and model save location.")

    hparams = dotmap.DotMap(json.load(open(sys.argv[1], 'r')))
    save_path = sys.argv[2]

    asyncio.get_event_loop().run_until_complete(train(hparams, save_path))
