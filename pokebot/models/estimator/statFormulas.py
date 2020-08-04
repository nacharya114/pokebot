import numpy as np
from numpy.random import rand
import pandas as pd
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



def extractBaseStats(pokemon, df):

	
	# print(df.head(5))
	pokemonEntry = df.loc[df['name'] == pokemon]
	print(pokemonEntry)
	# print(pokemonEntry['hp'].iloc[0])
	# print(pokemonEntry['attack'].iloc[0])
	stats = [pokemonEntry['hp'].iloc[0],
		pokemonEntry['attack'].iloc[0],
		pokemonEntry['defense'].iloc[0],
		pokemonEntry['sp_attack'].iloc[0],
		pokemonEntry['sp_defense'].iloc[0],
		pokemonEntry['speed'].iloc[0]]
	print(stats)
	return stats


def loadDatabase(filepath = '../../../resources/pokemon.csv'):
	df = pd.read_csv(filepath, usecols = ['name','hp','attack','defense','sp_attack','sp_defense','speed'])
	return df

if __name__ == '__main__':
	df = loadDatabase(filepath = '../../../resources/pokemon.csv')
	extractBaseStats('Excadrill', df)
