--Huntrix Weapons
--Equip only to Demon Hunter-Type monsters. Increase ATK by 100.
local s,id=GetID()
function s.eqfilter(c)
	return c:IsRace(0x8000000) -- Demon Hunter race
end
function s.initial_effect(c)
	--Equip procedure: can only be equipped to Demon Hunter-Type monsters
	aux.AddEquipProcedure(c,nil,s.eqfilter)
	--ATK up
	local e2=Effect.CreateEffect(c)
	e2:SetType(EFFECT_TYPE_EQUIP)
	e2:SetCode(EFFECT_UPDATE_ATTACK)
	e2:SetValue(100)
	c:RegisterEffect(e2)
end

