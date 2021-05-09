import asyncio
import nest_asyncio
nest_asyncio.apply()

import argparse
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
from poke_env.player.utils import cross_evaluate

from tabulate import tabulate

from pokebot import BotPlayer


async def train(hparams, save_dir, server_config=None, wandb_on=True):

    logger=None
    if wandb_on:
        import wandb
        wandb.init(project="pokebot")
        logger = wandb.log

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
        server_configuration=server_config,
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

    await trainer.train(wandb_on=wandb_on)

    opponents = [RandomPlayer(battle_format="gen8randombattle", server_configuration=server_config),
                 MaxBasePowerPlayer(battle_format="gen8randombattle", server_configuration=server_config),
                 SimpleHeuristicsPlayer(battle_format="gen8randombattle", server_configuration=server_config)]

    print("Beginning Eval")

    await trainer.evaluate(opponents, wandb_on=wandb_on)

    run_dir = os.path.join(os.path.abspath(save_dir), datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
    if not os.path.exists(run_dir):
        os.makedirs(run_dir)
    
    fp = os.path.join(run_dir, "model.h5")
    trainer.agent.save_weights(fp)

    if os.path.exists(os.path.join(os.path.abspath(save_dir), "latest_run")):
        os.makedirs(os.path.join(save_dir, "latest_run"), exist_ok=True)
    trainer.agent.save_weights(os.path.join(save_dir, "latest_run", "model.h5"))

async def test(server_config):
    # We create three random players
    players = [
        RandomPlayer(max_concurrent_battles=10, server_configuration=server_config),
        RandomPlayer(max_concurrent_battles=10, server_configuration=server_config),
    ]

    # Now, we can cross evaluate them: every player will player 20 games against every
    # other player.
    cross_evaluation = await cross_evaluate(players, n_challenges=20)

    # Defines a header for displaying results
    table = [["-"] + [p.username for p in players]]

    # Adds one line per player with corresponding results
    for p_1, results in cross_evaluation.items():
        table.append([p_1] + [cross_evaluation[p_1][p_2] for p_2 in results])

    # Displays results in a nicely formatted table.
    print(tabulate(table))

if __name__ == '__main__':

    if len(sys.argv) < 3:
        raise Exception("Needs hparams path and model save directory.")

    parser = argparse.ArgumentParser(description='Script for training a pokemon showdown bot.')

    parser.add_argument('hparams', metavar='H', help="Path to hparams file")
    parser.add_argument('save_dir', metavar="S", help='Path to save directory.')
    parser.add_argument('--server', dest='server_conf', help='PS Server location')
    parser.add_argument('--no-wandb', dest='wandb_on', action='store_false', help="Turns off wandb for run.")

    args = vars(parser.parse_args())


    hparams = dotmap.DotMap(json.load(open(args["hparams"], 'r')))
    save_dir = args["save_dir"]

    server_conf = None
    tasks = []

    loop = asyncio.get_event_loop()

    if len(sys.argv) == 4:
        server_conf = args["server_conf"]
        tasks.append(asyncio.Task(test(server_config = ServerConfiguration(server_conf, 'authentication-endpoint.com/action.php?'))))


    tasks.append(asyncio.Task(
        train(hparams, 
                save_dir, 
                server_config=server_conf, 
                wandb_on=args["wandb_on"])))

    loop.run_until_complete(asyncio.wait(tasks))

