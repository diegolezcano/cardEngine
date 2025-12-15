-- Googly Eyes
-- Card ID: 10000028
-- Card Name: Googly Eyes
-- Effect: Your opponent reveals their hand. You can pay 500 LP; send 1 card from your opponent's hand to the GY.

function c10000028.initial_effect(c)
	-- Reveal opponent's hand and optionally discard 1 card
	local e1=Effect.CreateEffect(c)
	e1:SetCategory(CATEGORY_HANDES)
	e1:SetType(EFFECT_TYPE_ACTIVATE)
	e1:SetCode(EVENT_FREE_CHAIN)
	e1:SetTarget(c10000028.target)
	e1:SetOperation(c10000028.activate)
	c:RegisterEffect(e1)
end

-- Target: Check if opponent has cards in hand
function c10000028.target(e,tp,eg,ep,ev,re,r,rp,chk)
	if chk==0 then return Duel.GetFieldGroupCount(tp,0,LOCATION_HAND)>0 end
	Duel.SetOperationInfo(0,CATEGORY_HANDES,nil,0,1-tp,1)
end

-- Activation: Reveal opponent's hand, optionally pay 500 LP to discard 1 card
function c10000028.activate(e,tp,eg,ep,ev,re,r,rp)
	local g=Duel.GetFieldGroup(tp,0,LOCATION_HAND)
	if #g>0 then
		-- Reveal opponent's hand
		Duel.ConfirmCards(tp,g)
		
		-- Ask if player wants to pay 500 LP to discard
		if Duel.CheckLPCost(tp,500) and Duel.SelectYesNo(tp,aux.Stringid(10000028,0)) then
			Duel.PayLPCost(tp,500)
			
			-- Select 1 card from opponent's hand to send to GY
			Duel.Hint(HINT_SELECTMSG,tp,HINTMSG_TOGRAVE)
			local sg=g:Select(tp,1,1,nil)
			if #sg>0 then
				Duel.SendtoGrave(sg,REASON_EFFECT)
			end
		end
		
		Duel.ShuffleHand(1-tp)
	end
end
