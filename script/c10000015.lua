--Queen of the Night
--2 Level 4 DARK monsters
--"Josefina - The Vampire" + "Batty"
--All DARK monsters on the field gain 50 ATK.
local s,id=GetID()
function s.matfilter(c,xyz,sumtype,tp)
	return (c:IsCode(10000010) or c:IsCode(10000004)) and c:IsAttribute(ATTRIBUTE_DARK) and c:IsLevel(4)
end
function s.initial_effect(c)
	c:EnableReviveLimit()
	--XYZ materials: 2 Level 4 DARK monsters ("Josefina - The Vampire" + "Batty")
	Xyz.AddProcedure(c,s.matfilter,4,2)
	--ATK up for all DARK monsters
	local e1=Effect.CreateEffect(c)
	e1:SetType(EFFECT_TYPE_FIELD)
	e1:SetCode(EFFECT_UPDATE_ATTACK)
	e1:SetRange(LOCATION_MZONE)
	e1:SetTargetRange(LOCATION_MZONE,LOCATION_MZONE)
	e1:SetTarget(aux.TargetBoolFunction(Card.IsAttribute,ATTRIBUTE_DARK))
	e1:SetValue(50)
	c:RegisterEffect(e1)
end
s.listed_names={10000010,10000004}

