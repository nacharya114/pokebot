function damage = calcDamage_model(battle,activePokemon, A,D, moveUsed,damageMultiplier)



activeMonTypes = activePokemon.types

level = activePokemon.level
weather = 1
burn = 1
moveType = moveUsed.type

% if strcmp(moveType,'physical')
%     A = activePokemon.attack
%     D = oppActivePokemon.defense
%     
% elseif strcmp(moveType,'special')
%     A = activePokemon.specialattack
%     D = oppActivePokemon.specialdefense
%     
% end

power = moveUsed.basepower
moveTyping = moveUsed.typing

STAB = 1
for i = 1:length(activeMonTypes)
    if any(strcmp(activeMonTypes{i},moveTyping))
       STAB = 1.5
    end
    
end



targets = 1

critical = 1

random = (1 - 0.85)*rand(1) + 0.85
% random = 1

other = 1

modifier = targets * weather*critical*random*STAB*damageMultiplier*burn*other

damage = floor(  (((((2*level/5) +2) * power * A/D)/50) + 2) * modifier )


end