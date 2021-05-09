#########################
# Author: Neil Acharya 
# 
# Bot that subclasses the EnvPlayer object from poke_env  
#########################
import numpy as np
from typing import Any, Callable, List, Optional, Tuple, Union

from poke_env.environment.battle import Battle
from poke_env.player.env_player import EnvPlayer
from poke_env.player_configuration import PlayerConfiguration
from poke_env.server_configuration import ServerConfiguration
from poke_env.teambuilder.teambuilder import Teambuilder

from .state_engine              import StateEngine, SimpleStateEngine
from .utils                     import *

class BotPlayer(EnvPlayer):

    _ACTION_SPACE = list(range(4 * 2 + 6))

    def __init__(
        self,
        player_configuration: Optional[PlayerConfiguration] = None,
        *args,
        log_level: Optional[int] = None,
        server_configuration: Optional[ServerConfiguration] = None,
        team: Optional[Union[str, Teambuilder]] = None,
        state_engine: Optional[StateEngine] = None,
        **kwargs
    ):
        """
        :param player_configuration: Player configuration. If empty, defaults to an
            automatically generated username with no password. This option must be set
            if the server configuration requires authentication.
        :type player_configuration: PlayerConfiguration, optional
        :param avatar: Player avatar id. Optional.
        :type avatar: int, optional
        :param battle_format: Name of the battle format this player plays. Defaults to
            gen8randombattle.
        :type battle_format: str
        :param log_level: The player's logger level.
        :type log_level: int. Defaults to logging's default level.
        :param server_configuration: Server configuration. Defaults to Localhost Server
            Configuration.
        :type server_configuration: ServerConfiguration, optional
        :param start_listening: Whether to start listening to the server. Defaults to
            True.
        :type start_listening: bool
        :param team: The team to use for formats requiring a team. Can be a showdown
            team string, a showdown packed team string, of a ShowdownTeam object.
            Defaults to None.
        :type team: str or Teambuilder, optional
        """
        super(BotPlayer, self).__init__(
            player_configuration=player_configuration,
            avatar=None,
            battle_format="gen8randombattle",
            log_level=log_level,
            server_configuration=server_configuration,
            start_listening=True,
            team=team
        )

        if state_engine is None:
            state_engine = SimpleStateEngine()

        self.state_engine = state_engine

    def teampreview(self, battle):
        mon_performance = {}

        # For each of our pokemons
        for i, mon in enumerate(battle.team.values()):
            # We store their average performance against the opponent team
            mon_performance[i] = np.mean([
                teampreview_performance(mon, opp)
                for opp in battle.opponent_team.values()
            ])

        # We sort our mons by performance
        ordered_mons = sorted(mon_performance, key = lambda k: -mon_performance[k])

        # We start with the one we consider best overall
        # We use i + 1 as python indexes start from 0
        #  but showdown's indexes start from 1
        return "/team " + ''.join([str(i + 1) for i in ordered_mons])

    def embed_battle(self, battle):
        return self.state_engine.convert(battle)

    def compute_reward(self, battle) -> float:
        return self.reward_computing_helper(
            battle,
            fainted_value=2,
            hp_value=1,
            victory_value=30,
        )

    def _action_to_move(self, action: int, battle: Battle) -> str:
        """Converts actions to move orders.
        The conversion is done as follows:
        0 <= action < 4:
            The actionth available move in battle.available_moves is executed.
        4 <= action < 8:
            The action - 4th available move in battle.available_moves is executed,
            while dynamaxing.
        8 <= action < 14
            The action - 8th available switch in battle.available_switches is executed.
        If the proposed action is illegal, a random legal move is performed.
        :param action: The action to convert.
        :type action: int
        :param battle: The battle in which to act.
        :type battle: Battle
        :return: the order to send to the server.
        :rtype: str
        """
        if (
            action < 4
            and action < len(battle.available_moves)
            and not battle.force_switch
        ):
            return self.create_order(battle.available_moves[action])
        elif (
            battle.can_dynamax
            and 0 <= action - 4 < len(battle.available_moves)
            and not battle.force_switch
        ):
            return self.create_order(battle.available_moves[action - 4], dynamax=True)
        elif 0 <= action - 8 < len(battle.available_switches):
            return self.create_order(battle.available_switches[action - 8])
        else:
            return self.choose_random_move(battle)

    def action_space(self) -> List:
        """The action space for gen 7 single battles.
        The conversion to moves is done as follows:
            0 <= action < 4:
                The actionth available move in battle.available_moves is executed.
            4 <= action < 8:
                The action - 4th available move in battle.available_moves is executed,
                with z-move.
            8 <= action < 12:
                The action - 8th available move in battle.available_moves is executed,
                with mega-evolution.
            12 <= action < 16:
                The action - 12th available move in battle.available_moves is executed,
                while dynamaxing.
            16 <= action < 22
                The action - 16th available switch in battle.available_switches is
                executed.
        """
        return self._ACTION_SPACE

