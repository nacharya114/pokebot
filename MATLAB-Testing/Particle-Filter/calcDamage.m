function damage = calcDamage(battle,activePokemon,oppActivePokemon, moveUsed,damageMultiplier)


activeMonTypes = activePokemon.types

level = activePokemon.level
weather = 1
burn = 1
moveType = moveUsed.type

if strcmp(moveType,'physical')
    A = activePokemon.Atk
    D = oppActivePokemon.Def
    
elseif strcmp(moveType,'special')
    A = activePokemon.SpA
    D = oppActivePokemon.SpD
    
end

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

damage = floor( (((((2*level/5) +2) * power * A/D)/50) + 2) * modifier)


end