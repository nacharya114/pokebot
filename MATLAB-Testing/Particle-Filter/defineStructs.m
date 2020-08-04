% define active mon
%heatran
% activePokemon = struct([])

activePokemon.level = 100
activePokemon.HP = 324
activePokemon.Atk = 194
activePokemon.Def = 248
activePokemon.SpA = 359
activePokemon.SpD = 248
activePokemon.Spe = 278

activePokemon.HP_BaseRange = [292,386-63]
activePokemon.Atk_BaseRange = [166, 306-63]
activePokemon.Def_BaseRange = [195, 342-63]
activePokemon.SpA_BaseRange = [238, 394-63]
activePokemon.SpD_BaseRange = [195, 342-63]
activePokemon.Spe_BaseRange = [143, 278-63]


activePokemon.HP_EV_BaseRange = [0,255]
activePokemon.Atk_EV_BaseRange = [0, 255]
activePokemon.Def_EV_BaseRange = [0, 255]
activePokemon.SpA_EV_BaseRange = [0, 255]
activePokemon.SpD_EV_BaseRange = [0, 255]
activePokemon.Spe_EV_BaseRange = [0, 255]

activePokemon.HP_wEVs = [292,386]
activePokemon.Atk_wEVs = [166, 306]
activePokemon.Def_wEVs = [195, 342]
activePokemon.SpA_wEVs = [238, 394]
activePokemon.SpD_wEVs = [195, 342]
activePokemon.Spe_wEVs = [143, 278]

activePokemon.types = {'fire','steel'}


%define opponent active mon
%excadrill

% activePokemon = struct([])
opponentActivePokemon.level = 100
opponentActivePokemon.HP = 362
opponentActivePokemon.Atk = 369
opponentActivePokemon.Def = 156
opponentActivePokemon.SpA = 122
opponentActivePokemon.SpD = 166
opponentActivePokemon.Spe = 302

opponentActivePokemon.HP_BaseRange = [330, 424-63]
opponentActivePokemon.Atk_BaseRange = [247, 405-63]
opponentActivePokemon.Def_BaseRange = [112, 240-63]
opponentActivePokemon.SpA_BaseRange = [94, 218-63]
opponentActivePokemon.SpD_BaseRange = [121, 251-63]
opponentActivePokemon.Spe_BaseRange = [162, 302-63]

opponentActivePokemon.HP_EV_BaseRange = [0,255]
opponentActivePokemon.Atk_EV_BaseRange = [0, 255]
opponentActivePokemon.Def_EV_BaseRange = [0, 255]
opponentActivePokemon.SpA_EV_BaseRange = [0, 255]
opponentActivePokemon.SpD_EV_BaseRange = [0, 255]
opponentActivePokemon.Spe_EV_BaseRange = [0, 255]

opponentActivePokemon.HP_wEVs = [330, 424]
opponentActivePokemon.Atk_wEVs = [247, 405]
opponentActivePokemon.Def_wEVs = [112, 240]
opponentActivePokemon.SpA_wEVs = [94, 218]
opponentActivePokemon.SpD_wEVs = [121, 251]
opponentActivePokemon.Spe_wEVs = [162, 302]

opponentActivePokemon.types = {'ground','steel'}





%define moves

%move 1 fire blast
% % move1 = struct([])
% move1.type = 'special'
% 
% move1.typing = 'fire'
% move1.basepower = 110
% 
% damageMult1 = 2

%move 1 energy ball
% move1 = struct([])
move1.type = 'special'

move1.typing = 'grass'
move1.basepower = 90

damageMult1 = 1


% %move 2 earthquake
% 
% % move2 = struct([])
% move2.type = 'physical'
% 
% move2.typing = 'ground'
% move2.basepower = 100
% damageMult2 = 4

%move 2 rock slide

% move2 = struct([])
move2.type = 'physical'

move2.typing = 'rock'
move2.basepower = 75
damageMult2 = 1





