--Golden Leaf
--Can only be equipped to "Koala Pelancio". The equipped monster gains 100 ATK and DEF.
local s,id=GetID()
function s.initial_effect(c)
	--Equip procedure: can only be equipped to "Koala Pelancio" (card 10000011)
	aux.AddEquipProcedure(c,nil,aux.FilterBoolFunction(Card.IsCode,10000011))
	--ATK up
	local e2=Effect.CreateEffect(c)
	e2:SetType(EFFECT_TYPE_EQUIP)
	e2:SetCode(EFFECT_UPDATE_ATTACK)
	e2:SetValue(100)
	c:RegisterEffect(e2)
	--DEF up
	local e3=Effect.CreateEffect(c)
	e3:SetType(EFFECT_TYPE_EQUIP)
	e3:SetCode(EFFECT_UPDATE_DEFENSE)
	e3:SetValue(100)
	c:RegisterEffect(e3)
end
s.listed_names={10000011}

