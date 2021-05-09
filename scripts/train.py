import asyncio
import nest_asyncio
nest_asyncio.apply()

import dotmap
import json
import sys
import importlib
import uuid
import os
import datetime

from poke_env.player.random_player import RandomPlayer
from poke_env.player_configuration import PlayerConfiguration
from poke_env.server_configuration import ServerConfiguration, LocalhostServerConfiguration 
from poke_env.player.baselines import MaxBasePowerPlayer, SimpleHeuristicsPlayer

from pokebot import BotPlayer


async def train(hparams, save_dir, server_config=None):

    if server_config is None:
        server_config = LocalhostServerConfiguration
    else:
        server_config = ServerConfiguration(server_config, 'authentication-endpoint.com/action.php?')

    # wandb.config.update(hparams)
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

    opponents = [RandomPlayer(battle_format="gen8randombattle", server_configuration=server_config),
                 MaxBasePowerPlayer(battle_format="gen8randombattle", server_configuration=server_config),
                 SimpleHeuristicsPlayer(battle_format="gen8randombattle", server_configuration=server_config)]

    print("Beginning Eval")

    await trainer.evaluate(opponents)

    run_dir = os.path.join(os.path.abspath(save_dir), datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
    if not os.path.exists(run_dir):
        os.makedirs(run_dir)
    
    fp = os.path.join(run_dir, "model.h5")
    trainer.agent.save_weights(fp)

    if os.path.exists(os.path.join(save_dir, "latest_run")):
        os.makedirs(os.path.join(save_dir, "latest_run"), exist_ok=True)
    trainer.agent.save_weights(os.path.join(save_dir, "latest_run", "model.h5"))

if __name__ == '__main__':

    if len(sys.argv) < 3:
        raise Exception("Needs hparams path and model save directory.")

    hparams = dotmap.DotMap(json.load(open(sys.argv[1], 'r')))
    save_dir = sys.argv[2]

    

    server_conf = None

    if len(sys.argv) == 4:
        server_conf = sys.argv[3]

    asyncio.get_event_loop().run_until_complete(train(hparams, save_dir, server_config=server_conf))
