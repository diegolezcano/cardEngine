-- Counter Trap Card Template
-- Card ID: 10000025
-- Card Name: No Traps
-- Effect: When your opponent activates a Trap Card: Negate the activation.

function c10000025.initial_effect(c)
	-- Counter trap: negate opponent's trap activation
	local e1=Effect.CreateEffect(c)
	e1:SetCategory(CATEGORY_NEGATE)
	e1:SetType(EFFECT_TYPE_ACTIVATE)
	e1:SetCode(EVENT_CHAINING)
	e1:SetCondition(c10000025.negcon)
	e1:SetTarget(c10000025.negtg)
	e1:SetOperation(c10000025.negop)
	c:RegisterEffect(e1)
end

-- Condition: Check if opponent's trap card is being activated and can be negated
function c10000025.negcon(e,tp,eg,ep,ev,re,r,rp)
	return rp==1-tp and re:IsHasType(EFFECT_TYPE_ACTIVATE) and re:IsTrapEffect() and Duel.IsChainNegatable(ev)
end

-- Target: Set operation info for negation
function c10000025.negtg(e,tp,eg,ep,ev,re,r,rp,chk)
	if chk==0 then return true end
	Duel.SetOperationInfo(0,CATEGORY_NEGATE,eg,1,0,0)
end

-- Operation: Negate the trap activation
function c10000025.negop(e,tp,eg,ep,ev,re,r,rp)
	if Duel.NegateActivation(ev) then
		-- Activation successfully negated
	end
end

