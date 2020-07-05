import numpy as np
from numpy.random import rand

import poke_env as penv
from poke_env.environment.battle import Battle
from poke_env.environment.pokemon import Pokemon
from poke_env.environment.move import Move

from poke_env.environment.move_category import MoveCategory
from poke_env.environment.pokemon_type import PokemonType

def calcHPStat(pokemon, baseStat, IV, EV):


	HP = 10 + pokemon.level + np.floor( ( (2 * baseStat + IV + np.floor(EV/4))   * pokemon.level )/(100)  )
	return HP


def calcStat(pokemon,baseStat, IV,EV, natureMod):

	stat = np.floor(  natureMod * (5 + np.floor(   ((2 * baseStat + IV + np.floor(EV/4)  ) * pokemon.level) / (100))   ) )
	return stat