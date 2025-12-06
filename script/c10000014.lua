--Vampire Coffin
--Can only be equipped to a DARK monster. The equipped monster gains 100 ATK.
local s,id=GetID()
function s.initial_effect(c)
	--Equip procedure: can only be equipped to DARK monsters
	aux.AddEquipProcedure(c,nil,aux.FilterBoolFunction(Card.IsAttribute,ATTRIBUTE_DARK))
	--ATK up
	local e2=Effect.CreateEffect(c)
	e2:SetType(EFFECT_TYPE_EQUIP)
	e2:SetCode(EFFECT_UPDATE_ATTACK)
	e2:SetValue(100)
	c:RegisterEffect(e2)
end

