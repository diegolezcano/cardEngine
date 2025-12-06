--Huntrix Weapons
--Equip only to "Rumi", "Mira" or "Zoey". Increase ATK by 100.
local s,id=GetID()
function s.eqfilter(c)
	return c:IsCode(10000017,10000018,10000019)
end
function s.initial_effect(c)
	--Equip procedure: can only be equipped to Rumi, Mira, or Zoey
	aux.AddEquipProcedure(c,nil,s.eqfilter)
	--ATK up
	local e2=Effect.CreateEffect(c)
	e2:SetType(EFFECT_TYPE_EQUIP)
	e2:SetCode(EFFECT_UPDATE_ATTACK)
	e2:SetValue(100)
	c:RegisterEffect(e2)
end
s.listed_names={10000017,10000018,10000019}

