--Camera
--When a monster declares an attack: Negate that attack.
local s,id=GetID()
function s.initial_effect(c)
	--Activate: Negate attack
	local e1=Effect.CreateEffect(c)
	e1:SetType(EFFECT_TYPE_ACTIVATE)
	e1:SetCode(EVENT_ATTACK_ANNOUNCE)
	e1:SetCondition(s.condition)
	e1:SetOperation(s.activate)
	c:RegisterEffect(e1)
end
function s.condition(e,tp,eg,ep,ev,re,r,rp)
	return Duel.GetAttacker():IsControler(1-tp)
end
function s.activate(e,tp,eg,ep,ev,re,r,rp)
	Duel.NegateAttack()
end

