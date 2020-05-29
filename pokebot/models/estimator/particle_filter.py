#########################
# Author: Rpberto Merona 
# 
# Particle Filter Estimator for State
#########################

from .estimator import Estimator

class ParticleFilter(Estimator):

    ##########################
    # Constructor
    ##########################
    def __init__(self):
        super().__init__()

    ##########################
    # Estimate function (returns State)
    ##########################
    def estimate(self, battle):
        
        pass