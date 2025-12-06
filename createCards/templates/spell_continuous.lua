-- Continuous Spell Card Template
-- Card ID: {CARD_ID}
-- Card Name: {CARD_NAME}
-- Effect: {EFFECT_DESC}

function c{CARD_ID}.initial_effect(c)
	-- Continuous effect (stays on field)
	local e1=Effect.CreateEffect(c)
	e1:SetType(EFFECT_TYPE_FIELD)
	{EFFECT_CODE}
	e1:SetRange(LOCATION_SZONE)
	{ADDITIONAL_PROPERTIES}
	c:RegisterEffect(e1)
end

