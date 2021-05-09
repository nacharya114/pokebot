import poke_env
import importlib


class PlayerFactory:

    @staticmethod
    def get_player(type="", format="gen8randombattle", **kwargs):
        baselines = importlib.import_module("poke_env.player.baselines")
        if hasattr(baselines, type):
            clazz = getattr(baselines, type)
            return clazz(battle_format=format, **kwargs)

        return poke_env.player.random_player.RandomPlayer(battle_format=format, **kwargs)
