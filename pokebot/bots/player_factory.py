import poke_env
import importlib


class PlayerFactory:

    @staticmethod
    def get_player(type="", format="gen8randombattle", **kwargs):
        baselines = importlib.import_module("poke_env.player.baselines")
        if getattr(baselines, type, lambda: None):
            clazz = getattr(baselines, type)
            return clazz(battle_format=format)

        return poke_env.player.random_player.RandomPlayer(battle_format=format)
