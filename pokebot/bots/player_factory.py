import poke_env
import importlib


class PlayerFactory:

    def __init__(self, server_configuration=None, **kwargs):
        super().__init__()

        if server_configuration is None:
            server_configuration = poke_env.server_configuration.LocalhostServerConfiguration
        self.server_configuration = server_configuration

    
    def get_player(self, type="", format="gen8randombattle", **kwargs):
        baselines = importlib.import_module("poke_env.player.baselines")
        if hasattr(baselines, type):
            clazz = getattr(baselines, type)
            return clazz(battle_format=format, 
            server_configuration=self.server_configuration,
            **kwargs)

        return poke_env.player.random_player.RandomPlayer(battle_format=format, 
                server_configuration=self.server_configuration, 
                **kwargs)
