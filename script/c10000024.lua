-- Switchy!
-- Card ID: 10000024
-- Card Name: Switchy!
-- Effect: Both players show their hands, then they exchange 1 card.

function c10000024.initial_effect(c)
	-- Quick-Play Spell activation
	local e1=Effect.CreateEffect(c)
	e1:SetCategory(CATEGORY_TOHAND)
	e1:SetType(EFFECT_TYPE_ACTIVATE)
	e1:SetCode(EVENT_FREE_CHAIN)
	e1:SetTarget(c10000024.target)
	e1:SetOperation(c10000024.activate)
	c:RegisterEffect(e1)
end

-- Target: Check both players have at least 1 card in hand
function c10000024.target(e,tp,eg,ep,ev,re,r,rp,chk)
	if chk==0 then
		local count1=Duel.GetFieldGroupCount(tp,LOCATION_HAND,0)
		local count2=Duel.GetFieldGroupCount(tp,0,LOCATION_HAND)
		return count1>0 and count2>0
	end
end

-- Activation: Both players reveal hands and exchange 1 card
function c10000024.activate(e,tp,eg,ep,ev,re,r,rp)
	-- Both players reveal their hands
	local h1=Duel.GetFieldGroup(tp,LOCATION_HAND,0)
	local h2=Duel.GetFieldGroup(tp,0,LOCATION_HAND)
	
	-- Reveal hands
	Duel.ConfirmCards(1-tp,h1)
	Duel.ConfirmCards(tp,h2)
	
	-- Each player selects 1 card from their hand to exchange
	if #h1>0 and #h2>0 then
		Duel.Hint(HINT_SELECTMSG,tp,HINTMSG_TOHAND)
		local g1=h1:Select(tp,1,1,nil)
		Duel.Hint(HINT_SELECTMSG,1-tp,HINTMSG_TOHAND)
		local g2=h2:Select(1-tp,1,1,nil)
		
		if #g1>0 and #g2>0 then
			local tc1=g1:GetFirst()
			local tc2=g2:GetFirst()
			
			-- Exchange cards by swapping control
			Duel.SwapControl(tc1,tc2)
		end
	end
end
