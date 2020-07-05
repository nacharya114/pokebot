#########################
# Author: Neil Acharya 
# 
# Estimtor ABC for estimating battle state from Battle object.  
#########################
import numpy as np
from abc import ABC

from poke_env.environment.battle import Battle
from poke_env.environment.pokemon import Pokemon

from pokebot.models.estimator.particle_filter import ParticleFilter


class PokemonEstimator():

    def __init__(self, pkmn: Pokemon):
        super().__init__()

        self.pkmn = pkmn

        self.pf = ParticleFilter(X0=None, M=None)

    @property
    def hp(self):
        return np.mean(self.pf.statsEstMatrix[:, 0])

    @property
    def atk(self):
        return np.mean(self.pf.statsEstMatrix[:, 1])

    @property
    def defense(self)
        return np.mean(self.pf.statsEstMatrix[:, 2])

    @property
    def spatk(self):
        return np.mean(self.pf.statsEstMatrix[:, 3])

    @property
    def spdef(self):
        return np.mean(self.pf.statsEstMatrix[:, 4])

    @property
    def speed(self):
        return np.mean(self.pf.statsEstMatrix[:, 5])


    def estimate(self):

        return np.concatenate([
            self.hp,
            self.atk,
            self.defense,
            self.spatk,
            self.spdef,
            self.speed
        ])

