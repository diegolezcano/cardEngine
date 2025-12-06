--Huntrix
--3 Level 4 LIGHT monsters
--"Rumi" + "Zoey" + "Mira"
--All LIGHT monsters on the field gain 50 ATK.
local s,id=GetID()
function s.matfilter(c,xyz,sumtype,tp)
	return (c:IsCode(10000017,10000018,10000019)) and c:IsAttribute(ATTRIBUTE_LIGHT) and c:IsLevel(4)
end
function s.initial_effect(c)
	c:EnableReviveLimit()
	--XYZ materials: 3 Level 4 LIGHT monsters ("Rumi" + "Zoey" + "Mira")
	Xyz.AddProcedure(c,s.matfilter,4,3)
	--ATK up for all LIGHT monsters
	local e1=Effect.CreateEffect(c)
	e1:SetType(EFFECT_TYPE_FIELD)
	e1:SetCode(EFFECT_UPDATE_ATTACK)
	e1:SetRange(LOCATION_MZONE)
	e1:SetTargetRange(LOCATION_MZONE,LOCATION_MZONE)
	e1:SetTarget(aux.TargetBoolFunction(Card.IsAttribute,ATTRIBUTE_LIGHT))
	e1:SetValue(50)
	c:RegisterEffect(e1)
end
s.listed_names={10000017,10000018,10000019}

