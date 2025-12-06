-- Effect Monster Template
-- Card ID: {CARD_ID}
-- Card Name: {CARD_NAME}
-- Effect: {EFFECT_DESC}

function c{CARD_ID}.initial_effect(c)
	-- Effect 1: {EFFECT_TYPE}
	local e1=Effect.CreateEffect(c)
	{EFFECT_CODE}
	c:RegisterEffect(e1)
end

-- Effect operation function
function c{CARD_ID}.operation(e,tp,eg,ep,ev,re,r,rp)
	-- tp = turn player (controller of this card)
	-- eg = event group
	-- ep = event player
	-- ev = event value
	-- re = reason effect
	-- r = reason
	-- rp = reason player
	
	{EFFECT_OPERATION}
end

-- Additional helper functions can be added here
-- function c{CARD_ID}.filter(c)
--     return c:IsFaceup() and c:IsType(TYPE_MONSTER)
-- end

