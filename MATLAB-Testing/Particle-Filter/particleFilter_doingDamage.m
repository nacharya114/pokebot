function [statsEstMeanVec, statsEstMaxVec,statsEstMinVec,Xt] = particleFilter_doingDamage(M,X_t_prev, damagePercent, activePokemon,battle,move,damageMult)

Xt_bar = zeros(M,13);
Xt = zeros(M,12);

weights = zeros(M,1);

%primarily update the enemy HP, Def, and SpD

for m = 1:M

    xt_m = X_t_prev(m,:);



    weight = calculateWeight_doingDamage(damagePercent, xt_m, activePokemon,battle,move,damageMult);
    weights(m) = weight;
    Xt_bar(m,:) = [xt_m,weight];
%     pause


end

weights = weights./(sum(weights));

nonZeroWeights = weights(weights > 0);
nonZeroWeightIdxs = find(weights > 0);

T = gendist(nonZeroWeights',M,1);

estimateIdxs = nonZeroWeightIdxs(T);
Xt = Xt_bar(estimateIdxs,1:12);

statsMatrix = Xt(:,1:6) + floor(Xt(:,7:12) /4);

statsEstMeanVec = [median(statsMatrix(:,1)),...
    median(statsMatrix(:,2)),...
    median(statsMatrix(:,3)),...
    median(statsMatrix(:,4)),...
    median(statsMatrix(:,5)),...
    median(statsMatrix(:,6))];

statsEstMaxVec =[max(statsMatrix(:,1)),...
    max(statsMatrix(:,2)),...
    max(statsMatrix(:,3)),...
    max(statsMatrix(:,4)),...
    max(statsMatrix(:,5)),...
    max(statsMatrix(:,6))];

statsEstMinVec = [min(statsMatrix(:,1)),...
    min(statsMatrix(:,2)),...
    min(statsMatrix(:,3)),...
    min(statsMatrix(:,4)),...
    min(statsMatrix(:,5)),...
    min(statsMatrix(:,6)) ];






end