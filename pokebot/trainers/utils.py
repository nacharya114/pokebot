##########################
# Author: Neil Acharya 
# 
# Trainer helper funcs
##########################
import asyncio
from threading import Thread
from typing import Callable

from poke_env.player.env_player import EnvPlayer
from poke_env.player.player import Player



def dqn_training(player, dqn, nb_steps):
    dqn.fit(player, nb_steps=nb_steps)

    # This call will finished eventual unfinshed battles before returning
    player.complete_current_battle()

def dqn_evaluation(player, dqn, nb_episodes):
    # Reset battle statistics
    player.reset_battles()
    dqn.test(player, nb_episodes=nb_episodes, visualize=False, verbose=False)

    print(
        "DQN Evaluation: %d victories out of %d episodes"
        % (player.n_won_battles, nb_episodes)
    )

def play_against_human(
       player, env_algorithm: Callable, opponent: str, env_algorithm_kwargs=None
):
    """Executes a function controlling the player while facing opponent.
    The env_algorithm function is executed with the player environment as first
    argument. It exposes the open ai gym API.
    Additional arguments can be passed to the env_algorithm function with
    env_algorithm_kwargs.
    Battles against opponent will be launched as long as env_algorithm is running.
    When env_algorithm returns, the current active battle will be finished randomly
    if it is not already.
    :param env_algorithm: A function that controls the player. It must accept the
        player as first argument. Additional arguments can be passed with the
        env_algorithm_kwargs argument.
    :type env_algorithm: callable
    :param opponent: A player against with the env player will player.
    :type opponent: Player
    :param env_algorithm_kwargs: Optional arguments to pass to the env_algorithm.
        Defaults to None.
    """
    player._start_new_battle = True

    async def launch_battles(player: EnvPlayer, opponent: str):
        battles_coroutine = asyncio.gather(
            player.send_challenges(
                opponent=opponent,
                n_challenges=1
            )
        )
        await battles_coroutine

    def env_algorithm_wrapper(player, kwargs):
        env_algorithm(player, **kwargs)

        player._start_new_battle = False
        while True:
            try:
                player.complete_current_battle()
                player.reset()
            except OSError:
                break

    loop = asyncio.get_event_loop()

    if env_algorithm_kwargs is None:
        env_algorithm_kwargs = {}

    thread = Thread(
        target=lambda: env_algorithm_wrapper(player, env_algorithm_kwargs)
    )
    thread.start()

    while player._start_new_battle:
        loop.run_until_complete(launch_battles(player, opponent))
    thread.join()
