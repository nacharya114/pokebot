#########################
# Author: Rpberto Merona 
# 
# Particle Filter Estimator for State
#########################

# from .estimator import Estimator
import numpy as np
import random
class ParticleFilter:

    
    ##########################
    # Constructor
    ##########################
    def __init__(self,X0,M):
        self.Xt_prev = X0 #a distribution representing prior knowledge of the enemy Mon's stats
        self.M = M #the number of particles in the filter
        self.weights = np.zeros((M,1))
        self.Xt = X0
        self.Xt_bar = np.zeros((M,12))
        self.statsEstMatrix = self.Xt[:,0:5] + np.floor[self.Xt[:,6:11] /4];

    ##########################
    # Estimate functions
    ##########################


    #speed estimator
    def estimate_speed(self, activePokemon, didMoveFirst):

        activeMonStats = activePokemon.stats

        for m in range(self.M):
            xt_m = X_t_prev[m,:]
            rawStats = xt_m[0:5]
            statsFromEVs = np.floor[xt_m[6:11]/4]
            statsEst = rawStats + statsFromEVs
            
            oppSpeedStatEst = statsEst[5];
            actPokemonSpeed = activeMonStats["Spe"]

            if didMoveFirst:
                #if we moved first
                if oppSpeedStatEst == actPokemonSpeed:
                    weight = 0.5;
                elif oppSpeedStatEst > actPokemonSpeed:
                    weight = 0;
                    
                elif oppSpeedStatEst < actPokemonSpeed:
                    weight = 1;
                    


            else:
                #if the opponent moved first
                if oppSpeedStatEst == actPokemonSpeed:
                    weight = 0.5;
                elif oppSpeedStatEst > actPokemonSpeed:
                    weight = 1;
                    
                elif oppSpeedStatEst < actPokemonSpeed:
                    weight = 0;
                    


            self.weights[m][0] = weight;
            self.Xt_bar[m,:] = xt_m;



        self.weights = self.weights/np.sum(self.weights)

        nonZeroWeights = self.weights[self.weights > 0];
        nonZeroWeightIdxs = np.nonzero(self.weights > 0);


        T = np.random.choice(len(nonZeroWeightIdxs), self.M, replace=True, p=nonZeroWeights.flatten())


        estimateIdxs = nonZeroWeightIdxs[T];
        self.Xt = self.Xt_bar[estimateIdxs,0:11]

        self.statsMatrix = self.Xt[:,0:5] + np.floor(self.Xt[:,6:11] /4);

    def estimate_doingDamage(self, activePokemon, oppActivePokemon, moveUsed, damagePercent):











