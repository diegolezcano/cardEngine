-- Counter Trap Card Template
-- Card ID: {CARD_ID}
-- Card Name: {CARD_NAME}
-- Effect: {EFFECT_DESC}

function c{CARD_ID}.initial_effect(c)
	-- Counter trap: negate trap activation
	local e1=Effect.CreateEffect(c)
	e1:SetCategory(CATEGORY_NEGATE)
	e1:SetType(EFFECT_TYPE_ACTIVATE)
	e1:SetCode(EVENT_CHAINING)
	e1:SetCondition(c{CARD_ID}.negcon)
	e1:SetTarget(c{CARD_ID}.negtg)
	e1:SetOperation(c{CARD_ID}.negop)
	c:RegisterEffect(e1)
end

-- Condition: Check if a trap card is being activated and can be negated
function c{CARD_ID}.negcon(e,tp,eg,ep,ev,re,r,rp)
	return re:IsHasType(EFFECT_TYPE_ACTIVATE) and re:IsTrapEffect() and Duel.IsChainNegatable(ev)
end

-- Target: Set operation info for negation
function c{CARD_ID}.negtg(e,tp,eg,ep,ev,re,r,rp,chk)
	if chk==0 then return true end
	Duel.SetOperationInfo(0,CATEGORY_NEGATE,eg,1,0,0)
end

-- Operation: Negate the trap activation
function c{CARD_ID}.negop(e,tp,eg,ep,ev,re,r,rp)
	if Duel.NegateActivation(ev) then
		-- Activation successfully negated
	end
end

