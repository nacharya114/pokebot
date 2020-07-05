function weight = calculateWeight_doingDamage(damagePercent, oppStatsEstimate, activePokemon, battle,moveUsed,damageMult)
N = 1000;

% HP_opp_dist = oppStatsEstimate(:,1);
% % Atk_opp = oppStatsEstimate(2);
% Def_opp_dist = oppStatsEstimate(:,3);
% % SpA_opp = oppStatsEstimate(4);
% SpD_opp_dists = oppStatsEstimate(:,5);
% % Spe_opp = oppStatsEstimate(6);



damageEstVec = zeros(1,N);
likelihoodVec = zeros(1,N);

moveType = moveUsed.type;
rawStats = oppStatsEstimate(1:6);
statsFromEVs = floor(oppStatsEstimate(7:12)/4);
statsEst = rawStats + statsFromEVs;

%     HP_opp_sample = HP_opp_dist(randi(length(HP_opp_dist)))
HP_opp_sample = statsEst(1);

% damageHP = round(damagePercent * HP_opp_dist)
    
damageHP = round(damagePercent * HP_opp_sample/100);

if strcmp(moveType,'physical')
    A = activePokemon.Atk;
%         D_opp_sample = Def_opp_dist(randi(length(Def_opp_dist)));
    Def_opp_sample = statsEst(3);

    D = Def_opp_sample;

elseif strcmp(moveType,'special')
    A = activePokemon.SpA;
%         D_opp_sample = SpD_opp_dist(randi(length(SpD_opp_dist)));
    SpD_opp_sample = statsEst(5);
    D = SpD_opp_sample;

end


for i = 1:N

    damageEst = round(calcDamage_model(battle,activePokemon, A,D,moveUsed,damageMult));
    damageEstVec(i) = damageEst;
    
    likelihoodVec(i) = abs(damageHP - damageEst) == 0;
end


weight = sum(likelihoodVec)/N;


% if strcmp(moveType,'physical')
%     A = activePokemon.Atk
% %         D_opp_sample = Def_opp_dist(randi(length(Def_opp_dist)));
%     Def_opp_sample = oppStatsEstimate(3);
% 
%     D = Def_opp_sample
% 
% elseif strcmp(moveType,'special')
%     A = activePokemon.SpA
% %         D_opp_sample = SpD_opp_dist(randi(length(SpD_opp_dist)));
%     SpD_opp_sample = oppStatsEstimate(5);
%     D = SpD_opp_sample
% 
% end



end