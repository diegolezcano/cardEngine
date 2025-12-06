-- Basic Spell Card Template
-- Card ID: {CARD_ID}
-- Card Name: {CARD_NAME}
-- Effect: {EFFECT_DESC}

function c{CARD_ID}.initial_effect(c)
	-- Activate effect
	local e1=Effect.CreateEffect(c)
	e1:SetType(EFFECT_TYPE_ACTIVATE)
	e1:SetCode(EVENT_FREE_CHAIN)
	{ADDITIONAL_PROPERTIES}
	e1:SetOperation(c{CARD_ID}.activate)
	c:RegisterEffect(e1)
end

-- Activation operation
function c{CARD_ID}.activate(e,tp,eg,ep,ev,re,r,rp)
	-- tp = turn player (the player who activated the card)
	{EFFECT_OPERATION}
end

