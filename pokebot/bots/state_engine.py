#########################
# Author: Neil Acharya 
# 
# Generic Class to produce a state (numpy vector) from a battle 
#########################
import numpy as np
from abc import ABC, abstractmethod

from poke_env.environment.battle import Battle

class StateEngine(ABC):

    def __init__(self, shape):
        super().__init__()

        self.shape = shape

    @abstractmethod
    def convert(self, battle: Battle):
        """
        :param battle: Battle object from poke_env. 
        :returns np.Array represenation of state.
        """
        raise NotImplementedError


class SimpleStateEngine(StateEngine):

    def convert(self, battle):
        # -1 indicates that the move does not have a base power
        # or is not available
        moves_base_power = -np.ones(4)
        moves_dmg_multiplier = np.ones(4)
        for i, move in enumerate(battle.available_moves):
            moves_base_power[i] = move.base_power / 100 # Simple rescaling to facilitate learning
            if move.type:
                moves_dmg_multiplier[i] = move.type.damage_multiplier(
                    battle.opponent_active_pokemon.type_1,
                    battle.opponent_active_pokemon.type_2,
                )

        # We count how many pokemons have not fainted in each team
        remaining_mon_team = len([mon for mon in battle.team.values() if mon.fainted]) / 6
        remaining_mon_opponent = (
            len([mon for mon in battle.opponent_team.values() if mon.fainted]) / 6
        )

        # Final vector with 10 components
        state = np.concatenate(
            [moves_base_power, moves_dmg_multiplier, [remaining_mon_team, remaining_mon_opponent]]
        )

        assert len(state) == self.shape

        return state
