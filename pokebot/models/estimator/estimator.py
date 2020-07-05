#########################
# Author: Neil Acharya 
# 
# Estimtor ABC for estimating battle state from Battle object.  
#########################
from abc import ABC

from poke_env.environment.battle import Battle

class Estimator(ABC):

    def __init__(self):
        super().__init__()

    def estimate(self, battle: Battle):

        raise NotImplementedError

