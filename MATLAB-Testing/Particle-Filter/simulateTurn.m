clearclcclose all
defineStructs

%define battle
% battle = struct([])
battle.activePokemon = activePokemon 
battle.opponentActivePokemon = opponentActivePokemon 

% use move 1
damage1 = calcDamage(battle,battle.activePokemon, battle.opponentActivePokemon, move1,damageMult1)
damage1Percent = 100*damage1/battle.opponentActivePokemon.HP

% battle.activePokemon = opponentActivePokemon  
% battle.opponentActivePokemon = activePokemon

damage2 = calcDamage(battle,battle.opponentActivePokemon,battle.activePokemon,move2,damageMult2)
damage2Percent = 100*damage2/battle.activePokemon.HP


% PF for doing damage to enemy mon
M = 1000

oppStatEstVec = [mean(battle.opponentActivePokemon.HP_wEVs),...
    mean(battle.opponentActivePokemon.Atk_wEVs),...
    mean(battle.opponentActivePokemon.Def_wEVs),...
    mean(battle.opponentActivePokemon.SpA_wEVs),...
    mean(battle.opponentActivePokemon.SpD_wEVs),...
    mean(battle.opponentActivePokemon.Spe_wEVs)]

oppStatEstSpreadMaxVec = [max(battle.opponentActivePokemon.HP_wEVs),...
    max(battle.opponentActivePokemon.Atk_wEVs),...
    max(battle.opponentActivePokemon.Def_wEVs),...
    max(battle.opponentActivePokemon.SpA_wEVs),...
    max(battle.opponentActivePokemon.SpD_wEVs),...
    max(battle.opponentActivePokemon.Spe_wEVs)]

oppStatEstSpreadMinVec = [min(battle.opponentActivePokemon.HP_wEVs),...
    min(battle.opponentActivePokemon.Atk_wEVs),...
    min(battle.opponentActivePokemon.Def_wEVs),...
    min(battle.opponentActivePokemon.SpA_wEVs),...
    min(battle.opponentActivePokemon.SpD_wEVs),...
    min(battle.opponentActivePokemon.Spe_wEVs)]



%TODO: replace pure uniform distribution with one informed by usage
%statistics

X0 = generateInitialDistribution(M,battle.opponentActivePokemon)

% sum(EV_distr_matrix,2)
% 
% max(EV_distr_matrix,2)
% sort(X0)

%filter for speed
didMoveFirst = false

[statsEstMeanVec, statsEstMaxVec,statsEstMinVec,Xt] = particleFilter_speed(M,X0,battle.activePokemon, didMoveFirst)

oppStatEstVec = [oppStatEstVec statsEstMeanVec]
oppStatEstSpreadMaxVec = [oppStatEstSpreadMaxVec statsEstMaxVec]
oppStatEstSpreadMinVec = [oppStatEstSpreadMinVec statsEstMinVec]


%filter for doing damage to enemy pokemon

[statsEstMeanVec, statsEstMaxVec,statsEstMinVec,Xt] = particleFilter_doingDamage(M,Xt, ...
    damage1Percent, battle.activePokemon, battle,move1,damageMult1)

oppStatEstVec = [oppStatEstVec statsEstMeanVec]
oppStatEstSpreadMaxVec = [oppStatEstSpreadMaxVec statsEstMaxVec]
oppStatEstSpreadMinVec = [oppStatEstSpreadMinVec statsEstMinVec]

% sum(Xt(:,7:12),2)
% pause
%filter for receiving damage from enemy pokemon


[statsEstMeanVec, statsEstMaxVec,statsEstMinVec,Xt] = particleFilter_receivingDamage(M,Xt, ...
    damage2Percent, battle.activePokemon,battle.opponentActivePokemon, battle,move2,damageMult2)

oppStatEstVec = [oppStatEstVec statsEstMeanVec]
oppStatEstSpreadMaxVec = [oppStatEstSpreadMaxVec statsEstMaxVec]
oppStatEstSpreadMinVec = [oppStatEstSpreadMinVec statsEstMinVec]




%filter for doing damage to enemy pokemon

[statsEstMeanVec, statsEstMaxVec,statsEstMinVec,Xt] = particleFilter_doingDamage(M,Xt, ...
    damage1Percent, battle.activePokemon, battle,move1,damageMult1)

oppStatEstVec = [oppStatEstVec statsEstMeanVec]
oppStatEstSpreadMaxVec = [oppStatEstSpreadMaxVec statsEstMaxVec]
oppStatEstSpreadMinVec = [oppStatEstSpreadMinVec statsEstMinVec]

% sum(Xt(:,7:12),2)
% pause
%filter for receiving damage from enemy pokemon


[statsEstMeanVec, statsEstMaxVec,statsEstMinVec,Xt] = particleFilter_receivingDamage(M,Xt, ...
    damage2Percent, battle.activePokemon,battle.opponentActivePokemon, battle,move2,damageMult2)

oppStatEstVec = [oppStatEstVec statsEstMeanVec]
oppStatEstSpreadMaxVec = [oppStatEstSpreadMaxVec statsEstMaxVec]
oppStatEstSpreadMinVec = [oppStatEstSpreadMinVec statsEstMinVec]


figure(1)
subplot(6,1,1)
plot(oppStatEstVec(:,1),'b-o','LineWidth',2)
hold on
plot(oppStatEstSpreadMaxVec(:,1),'b--','LineWidth',2)
plot(oppStatEstSpreadMinVec(:,1),'b--','LineWidth',2)

plot(battle.opponentActivePokemon.HP*ones(size(oppStatEstVec(:,1))),'r--','LineWidth',2)

subplot(6,1,2)
plot(oppStatEstVec(:,2),'b-o','LineWidth',2)
hold on
plot(oppStatEstSpreadMaxVec(:,2),'b--','LineWidth',2)
plot(oppStatEstSpreadMinVec(:,2),'b--','LineWidth',2)
plot(battle.opponentActivePokemon.Atk*ones(size(oppStatEstVec(:,1))),'r--','LineWidth',2)

subplot(6,1,3)
plot(oppStatEstVec(:,3),'b-o','LineWidth',2)
hold on
plot(oppStatEstSpreadMaxVec(:,3),'b--','LineWidth',2)
plot(oppStatEstSpreadMinVec(:,3),'b--','LineWidth',2)
plot(battle.opponentActivePokemon.Def*ones(size(oppStatEstVec(:,1))),'r--','LineWidth',2)

subplot(6,1,4)
plot(oppStatEstVec(:,4),'b-o','LineWidth',2)
hold on
plot(oppStatEstSpreadMaxVec(:,4),'b--','LineWidth',2)
plot(oppStatEstSpreadMinVec(:,4),'b--','LineWidth',2)
plot(battle.opponentActivePokemon.SpA*ones(size(oppStatEstVec(:,1))),'r--','LineWidth',2)

subplot(6,1,5)
plot(oppStatEstVec(:,5),'b-o','LineWidth',2)
hold on
plot(oppStatEstSpreadMaxVec(:,5),'b--','LineWidth',2)
plot(oppStatEstSpreadMinVec(:,5),'b--','LineWidth',2)
plot(battle.opponentActivePokemon.SpD*ones(size(oppStatEstVec(:,1))),'r--','LineWidth',2)

subplot(6,1,6)
plot(oppStatEstVec(:,6),'b-o','LineWidth',2)
hold on
plot(oppStatEstSpreadMaxVec(:,6),'b--','LineWidth',2)
plot(oppStatEstSpreadMinVec(:,6),'b--','LineWidth',2)
plot(battle.opponentActivePokemon.Spe*ones(size(oppStatEstVec(:,1))),'r--','LineWidth',2)









