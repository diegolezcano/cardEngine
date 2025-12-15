-- Soda Pop!
-- Equip Spell Card
-- Effect: Equip only to a Demon-Type monster. It gains 100 ATK.

function c10000105.initial_effect(c)
	-- Equip limit: Demon-Type monsters only
	aux.AddEquipProcedure(c,nil,aux.FilterBoolFunction(Card.IsRace,RACE_DEMON))
	
	-- ATK increase
	local e1=Effect.CreateEffect(c)
	e1:SetType(EFFECT_TYPE_EQUIP)
	e1:SetCode(EFFECT_UPDATE_ATTACK)
	e1:SetValue(100)
	c:RegisterEffect(e1)
end
