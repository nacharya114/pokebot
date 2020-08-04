import numpy as np
from numpy.random import rand

import poke_env as penv
from poke_env.environment.battle import Battle
from poke_env.environment.pokemon import Pokemon
from poke_env.environment.move import Move

from poke_env.environment.move_category import MoveCategory
from poke_env.environment.pokemon_type import PokemonType

def calcDamage(activePokemon,oppActivePokemon, moveUsed):


	activeMonTypes = activePokemon.types
	oppActiveMonTypes = oppActivePokemon.types

	level = activePokemon.level
	weather = 1
	burn = 1
	moveCategory = moveUsed.category

	activeMonStats = activePokemon.stats
	oppActiveMonStats = oppActivePokemon.stats

	if moveCategory == MoveCategory.PHYSICAL:
		A = activeMonStats["Atk"]
		D = oppActiveMonStats["Def"]
		
	elif moveCategory == MoveCategory.SPECIAL:
		A = activeMonStats["SpA"]
		D = oppActiveMonStats["SpD"]
		


	power = moveUsed.base_power
	moveType = moveUsed.type
		
	STAB = 1

	if np.any(moveType == activeMonTypes[i] for i in range(len(activeMonTypes))):
		STAB = 1.5



	targets = 1

	critical = 1

	random = (1 - 0.85)*rand(1) + 0.85
	# random = 1

	other = 1

	damageMultiplier = moveUsed.type.damage_multiplier(oppActivePokemon.type_1, oppActivePokemon.type_2)



	modifier = targets * weather * critical*random*STAB*damageMultiplier*burn*other

	damage = np.floor( (((((2*level/5) +2) * power * A/D)/50) + 2) * modifier)
	return damage



def calcDamage_model(activePokemon,oppActivePokemon, A,D, moveUsed):


	activeMonTypes = activePokemon.types
	oppActiveMonTypes = oppActivePokemon.types

	level = activePokemon.level
	weather = 1
	burn = 1
	moveCategory = moveUsed.category

	activeMonStats = activePokemon.stats
	oppActiveMonStats = oppActivePokemon.stats

	if moveCategory == MoveCategory.PHYSICAL:
		A = activeMonStats["Atk"]
		D = oppActiveMonStats["Def"]
		
	elif moveCategory == MoveCategory.SPECIAL:
		A = activeMonStats["SpA"]
		D = oppActiveMonStats["SpD"]
		


	power = moveUsed.base_power
	moveType = moveUsed.type
		
	STAB = 1

	if np.any(moveType == activeMonTypes[i] for i in range(len(activeMonTypes))  ):
		STAB = 1.5



	targets = 1

	critical = 1

	random = (1 - 0.85)*rand(1) + 0.85
	# random = 1

	other = 1

	damageMultiplier = moveUsed.type.damage_multiplier(oppActivePokemon.type_1, oppActivePokemon.type_2)



	modifier = targets * weather * critical*random*STAB*damageMultiplier*burn*other

	damage = np.floor( (((((2*level/5) +2) * power * A/D)/50) + 2) * modifier)
	return damage
