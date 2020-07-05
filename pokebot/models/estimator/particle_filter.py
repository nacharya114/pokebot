#########################
# Author: Rpberto Merona 
# 
# Particle Filter Estimator for State
#########################

# from .estimator import Estimator
import numpy as np
import random

from damage_formula import *

from statFormulas import *

class ParticleFilter:

    
    ##########################
    # Constructor
    ##########################
    def __init__(self,M, pokemon):
        self.Xt_prev = X0 #a distribution representing prior knowledge of the enemy Mon's stats
        self.M = M #the number of particles in the filter
        self.weights = np.zeros((M,1))
        self.Xt = X0
        self.Xt_bar = np.zeros((M,12))
        self.statsMatrix = self.Xt[:,0:5] + np.floor[self.Xt[:,6:11] /4];

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

        for m in range(self.M):
            xt_m = X_t_prev[m,:]
            weight = calculateWeight_doingDamage(damagePercent, xt_m, activePokemon,battle,move,oppActivePokemon);
            self.weights[m][0] = weight
            self.Xt_bar[m,:] = xt_m

        self.weights = self.weights./np.sum(self.weights)

        nonZeroWeights = self.weights[self.weights > 0];
        nonZeroWeightIdxs = np.nonzero(self.weights > 0);


        T = np.random.choice(len(nonZeroWeightIdxs), self.M, replace=True, p=nonZeroWeights.flatten())


        estimateIdxs = nonZeroWeightIdxs[T];
        self.Xt = self.Xt_bar[estimateIdxs,0:11]

        self.statsMatrix = self.Xt[:,0:5] + np.floor(self.Xt[:,6:11] /4);







    def calcWeight_doingDamage(self,damagePercent, oppStatsEstDistVec, activePokemon, battle,moveUsed,oppActivePokemon):
        N = 1000
        activeMonStats = activePokemon.stats
        damageEstVec = np.zeros((1,N))
        likelihoodVec = np.zeros((1,N))

        moveType = moveUsed.type;


        rawStats = oppStatsEstDistVec[0:5]
        statsFromEVs = np.floor[oppStatsEstDistVec[6:11]/4]
        statsEst = rawStats + statsFromEVs



        HP_opp_sample = statsEst[0];

            
        damageHP = np.round(damagePercent * HP_opp_sample/100);


        if moveCategory == MoveCategory.PHYSICAL:
            A = activeMonStats["Atk"];
            D = statsEst[2]
            
        elif moveCategory == MoveCategory.SPECIAL:
            A = activeMonStats["SpA"];
            D = statsEst[4]


        for i in range(N):

            damageEst = np.round(calcDamage_model(activePokemon,oppActivePokemon, A,D, moveUsed));
            damageEstVec[i] = damageEst;
            
            likelihoodVec[i] = int(np.abs(damageHP - damageEst) == 0)


        weight = np.sum(likelihoodVec)/N
        return weight


    def estimate_receivingDamage(self, activePokemon, oppActivePokemon, moveUsed, damagePercent):

        for m in range(self.M):
            xt_m = X_t_prev[m,:]
            weight = calculateWeight_receivingDamage(damagePercent, xt_m, activePokemon,battle,move,oppActivePokemon);
            self.weights[m][0] = weight
            self.Xt_bar[m,:] = xt_m

        self.weights = self.weights./np.sum(self.weights)

        nonZeroWeights = self.weights[self.weights > 0];
        nonZeroWeightIdxs = np.nonzero(self.weights > 0);


        T = np.random.choice(len(nonZeroWeightIdxs), self.M, replace=True, p=nonZeroWeights.flatten())


        estimateIdxs = nonZeroWeightIdxs[T];
        self.Xt = self.Xt_bar[estimateIdxs,0:11]

        self.statsMatrix = self.Xt[:,0:5] + np.floor(self.Xt[:,6:11] /4);







    def calcWeight_receivingDamage(self,damagePercent, oppStatsEstDistVec, activePokemon, battle,moveUsed,oppActivePokemon):
        N = 1000
        activeMonStats = activePokemon.stats
        damageEstVec = np.zeros((1,N))
        likelihoodVec = np.zeros((1,N))

        moveType = moveUsed.type;


        rawStats = oppStatsEstDistVec[0:5]
        statsFromEVs = np.floor[oppStatsEstDistVec[6:11]/4]
        statsEst = rawStats + statsFromEVs



        HP_opp_sample = activeMonStats["HP"];

            
        damageHP = np.round(damagePercent * HP_opp_sample/100);


        if moveCategory == MoveCategory.PHYSICAL:
            A = statsEst[1]
            D = activeMonStats["Def"];
            
        elif moveCategory == MoveCategory.SPECIAL:
            A = statsEst[3]
            D = activeMonStats["SpD"];


        for i in range(N):

            damageEst = np.round(calcDamage_model(activePokemon,oppActivePokemon, A,D, moveUsed));
            damageEstVec[i] = damageEst;
            
            likelihoodVec[i] = int(np.abs(damageHP - damageEst) == 0)


        weight = np.sum(likelihoodVec)/N
        return weight



def generateInitialDistribution(M,pokemon):

    # generate initial stat distribution from a set lookup on smogon

    # for now prespecify the pokemon: excadrill

    # name = pokemon.species
    name = 'Excadrill'

    df = loadDatabase(filepath = '../../../resources/pokemon.csv')
    baseStats = extractBaseStats(name, df)

    HP_BaseRange = [calcHPStat(pokemon, baseStats[0], 0, 0),calcHPStat(pokemon, baseStats[0], 31, 255)]
    Atk_BaseRange = [calcStat(pokemon,baseStats[1], 0,0, 0.9),calcStat(pokemon,baseStats[1], 31,255, 1.1)]
    Def_BaseRange = [calcStat(pokemon,baseStats[2], 0,0, 0.9),calcStat(pokemon,baseStats[2], 31,255, 1.1)]
    SpA_BaseRange = [calcStat(pokemon,baseStats[3], 0,0, 0.9),calcStat(pokemon,baseStats[3], 31,255, 1.1)]
    SpD_BaseRange = [calcStat(pokemon,baseStats[4], 0,0, 0.9),calcStat(pokemon,baseStats[4], 31,255, 1.1)]
    Spe_BaseRange = [calcStat(pokemon,baseStats[5], 0,0, 0.9),calcStat(pokemon,baseStats[5], 31,255, 1.1)]


    X0 = np.concatenate(( np.round( (HP_BaseRange[1] - HP_BaseRange[0]) * np.random.rand(M,1)  + HP_BaseRange[1]), \
        np.round( (Atk_BaseRange[1] - Atk_BaseRange[0]) * np.random.rand(M,1)  + Atk_BaseRange[1]), \
        np.round( (Def_BaseRange[1] - Def_BaseRange[0]) * np.random.rand(M,1)  + Def_BaseRange[1]), \
        np.round( (SpA_BaseRange[1] - SpA_BaseRange[0]) * np.random.rand(M,1)  + SpA_BaseRange[1]), \
        np.round( (SpD_BaseRange[1] - SpD_BaseRange[0]) * np.random.rand(M,1)  + SpD_BaseRange[1]), \
        np.round( (Spe_BaseRange[1] - Spe_BaseRange[0]) * np.random.rand(M,1)  + Spe_BaseRange[1]) \
        ),axis=1)




    #extract the EVs for each distinct set
    #each row denotes a specific set's EVs
    EVs_setWise = [[4, 252, 0, 0, 0, 252];[0,252,4,0,0,252]];

    [rows1,cols1] = size(EVs_setWise)
    EV_distr_matrix = repmat(EVs_setWise,floor(M/rows1),1)

    [rows,cols] = size(EV_distr_matrix)

    while rows < M:
        EV_distr_matrix = [EV_distr_matrix;EVs_setWise(1,:)];
        [rows,cols] = size(EV_distr_matrix)

    #randomize

    EV_distr_matrix = EV_distr_matrix(randperm(M),:)

    X0 = [X0,EV_distr_matrix];




