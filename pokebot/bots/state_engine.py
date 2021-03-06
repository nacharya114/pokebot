#########################
# Author: Neil Acharya 
# 
# Generic Class to produce a state (numpy vector) from a battle 
#########################
import numpy as np
from abc import ABC, abstractmethod

from poke_env.environment.battle import Battle
from poke_env.environment.move_category import MoveCategory
from poke_env.environment.side_condition import SideCondition


class StateEngine(ABC):

    def __init__(self, shape, **kwargs):
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


class HeuristicStateEngine(StateEngine):

    ENTRY_HAZARDS = {
        "spikes": SideCondition.SPIKES,
        "stealhrock": SideCondition.STEALTH_ROCK,
        "stickyweb": SideCondition.STICKY_WEB,
        "toxicspikes": SideCondition.TOXIC_SPIKES,
    }

    ANTI_HAZARDS_MOVES = {"rapidspin", "defog"}

    SPEED_TIER_COEFICIENT = 0.1
    HP_FRACTION_COEFICIENT = 0.4
    SWITCH_OUT_MATCHUP_THRESHOLD = -2

    def __init__(self, **kwargs):
        super().__init__(24, **kwargs)

    def _estimate_matchup(self, mon, opponent):
        score = max([opponent.damage_multiplier(t) for t in mon.types if t is not None])
        score -= max(
            [mon.damage_multiplier(t) for t in opponent.types if t is not None]
        )
        if mon.base_stats["spe"] > opponent.base_stats["spe"]:
            score += self.SPEED_TIER_COEFICIENT
        elif opponent.base_stats["spe"] > mon.base_stats["spe"]:
            score -= self.SPEED_TIER_COEFICIENT

        score += mon.current_hp_fraction * self.HP_FRACTION_COEFICIENT
        score -= opponent.current_hp_fraction * self.HP_FRACTION_COEFICIENT

        return score

    def _stat_estimation(self, mon, stat):
        # Stats boosts value
        if mon.boosts[stat] > 1:
            boost = (2 + mon.boosts[stat]) / 2
        else:
            boost = 2 / (2 - mon.boosts[stat])
        return ((2 * mon.base_stats[stat] + 31) + 5) * boost

    def convert(self, battle: Battle):

        vec = []

        # Main mons shortcuts
        active = battle.active_pokemon
        opponent = battle.opponent_active_pokemon

        #Add stats

        # Rough estimation of damage ratio
        physical_ratio = self._stat_estimation(active, "atk") / self._stat_estimation(
            opponent, "def"
        )
        special_ratio = self._stat_estimation(active, "spa") / self._stat_estimation(
            opponent, "spd"
        )

        def_ratio = self._stat_estimation(active, "def") / self._stat_estimation(
            opponent, "atk"
        )

        spd_ratio = self._stat_estimation(active, "spd") / self._stat_estimation(
            opponent, "spa"
        )

        active_matchup = self._estimate_matchup(active, opponent)

        moves_sum = -np.zeros(4)
        moves_boost = np.zeros(4)
        move_haz = np.zeros(4)
        move_anti = np.zeros(4)

        for i, m in enumerate(battle.available_moves):

            moves_sum[i] = (m.base_power
                         * (1.5 if m.type in active.types else 1)
                         * opponent.damage_multiplier(m)
                         * (
                             physical_ratio
                             if m.category == MoveCategory.PHYSICAL
                             else special_ratio
                         )
                         * m.accuracy
                         ) / 100

            moves_boost[i] = sum(m.boosts.values()) if m.boosts else 0
            move_haz[i] = 1 if m.id in self.ENTRY_HAZARDS else 0
            move_anti[i] = 1 if m.id in self.ANTI_HAZARDS_MOVES else 0

        battle_sc = 1 if battle.side_conditions else 0
        battle_o_sc = 0 if any([self.ENTRY_HAZARDS[m.id]
                                not in battle.opponent_side_conditions if m.id in self.ENTRY_HAZARDS else False
                                for m in battle.available_moves]) else 1

        remaining_mon_team = len([mon for mon in battle.team.values() if mon.fainted]) / 6
        remaining_mon_opponent = (
                len([mon for mon in battle.opponent_team.values() if mon.fainted]) / 6
        )

        can_dynamax = 1 if battle.can_dynamax else 0

        return np.concatenate([
                            [def_ratio,
                            spd_ratio],
                            moves_sum,
                            moves_boost,
                            move_haz,
                            move_anti,
                            [battle_sc,
                            battle_o_sc],
                            [remaining_mon_opponent,
                            remaining_mon_team],
                            [active_matchup,
                            can_dynamax]
                            ])


