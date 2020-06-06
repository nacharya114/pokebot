function X0 = generateInitialDistribution(M,pokemon)


% %% generate initial distribution based on a uniform stat + EV spread
% X0 = [round(diff(pokemon.HP_BaseRange) * rand(M,1) + pokemon.HP_BaseRange(1)),...
%     round(diff(pokemon.Atk_BaseRange) * rand(M,1) + pokemon.Atk_BaseRange(1)),...
%     round(diff(pokemon.Def_BaseRange) * rand(M,1) + pokemon.Def_BaseRange(1)),...
%     round(diff(pokemon.SpA_BaseRange) * rand(M,1) + pokemon.SpA_BaseRange(1)),...
%     round(diff(pokemon.SpD_BaseRange) * rand(M,1) + pokemon.SpD_BaseRange(1)),...
%     round(diff(pokemon.Spe_BaseRange) * rand(M,1) + pokemon.Spe_BaseRange(1)),...
%     ];
% 
% EV_distr_matrix = zeros(M,6);
% maxEVs = 510;
% 
% 
% for i = 1:M
%     
%     
%     order = randperm(6);
%     EVs1 = round(255 * rand(1));
%     remainingEVs = maxEVs - EVs1;
%     
%     EVs2 = round((min(255,remainingEVs) - 0) * rand(1));
%     remainingEVs = remainingEVs - EVs2;
%     
%     EVs3 = round((min(255,remainingEVs) - 0) * rand(1));
%     remainingEVs = remainingEVs - EVs3;
%     EVs4 = round((min(255,remainingEVs) - 0) * rand(1));
%     remainingEVs = remainingEVs - EVs4;
%     EVs5 = round((min(255,remainingEVs) - 0) * rand(1));
%     remainingEVs = remainingEVs - EVs5;
%     EVs6 = round(min(255,remainingEVs));
%     
%     EvsVec = [EVs1,EVs2,EVs3,EVs4,EVs5,EVs6];
%     EvsVec_rand = EvsVec(order);
%     
%     
% %     pause
%     EV_distr_matrix(i,:) = [EvsVec_rand];
% end
% X0 = [X0,EV_distr_matrix];


%% generate initial stat distribution from a set lookup on smogon

% for now prespecify the pokemon: excadrill
X0 = [round(diff(pokemon.HP_BaseRange) * rand(M,1) + pokemon.HP_BaseRange(1)),...
    round(diff(pokemon.Atk_BaseRange) * rand(M,1) + pokemon.Atk_BaseRange(1)),...
    round(diff(pokemon.Def_BaseRange) * rand(M,1) + pokemon.Def_BaseRange(1)),...
    round(diff(pokemon.SpA_BaseRange) * rand(M,1) + pokemon.SpA_BaseRange(1)),...
    round(diff(pokemon.SpD_BaseRange) * rand(M,1) + pokemon.SpD_BaseRange(1)),...
    round(diff(pokemon.Spe_BaseRange) * rand(M,1) + pokemon.Spe_BaseRange(1)),...
    ];




%extract the EVs for each distinct set
%each row denotes a specific set's EVs
EVs_setWise = [[4, 252, 0, 0, 0, 252];[0,252,4,0,0,252]];

[rows1,cols1] = size(EVs_setWise)
EV_distr_matrix = repmat(EVs_setWise,floor(M/rows1),1)

[rows,cols] = size(EV_distr_matrix)

while rows < M
    EV_distr_matrix = [EV_distr_matrix;EVs_setWise(1,:)];
    [rows,cols] = size(EV_distr_matrix)
end

%randomize

EV_distr_matrix = EV_distr_matrix(randperm(M),:)

X0 = [X0,EV_distr_matrix];












end