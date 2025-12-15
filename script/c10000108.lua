-- Your Idol
-- Normal Spell Card
-- Effect: Pay 300 LP; target up to 5 of your banished Demon-Type monsters; return those targets to your GY.

function c10000108.initial_effect(c)
	-- Activate
	local e1=Effect.CreateEffect(c)
	e1:SetCategory(CATEGORY_TOGRAVE)
	e1:SetType(EFFECT_TYPE_ACTIVATE)
	e1:SetCode(EVENT_FREE_CHAIN)
	e1:SetProperty(EFFECT_FLAG_CARD_TARGET)
	e1:SetCost(c10000108.cost)
	e1:SetTarget(c10000108.target)
	e1:SetOperation(c10000108.activate)
	c:RegisterEffect(e1)
end

-- Cost: Pay 300 LP
function c10000108.cost(e,tp,eg,ep,ev,re,r,rp,chk)
	if chk==0 then return Duel.CheckLPCost(tp,300) end
	Duel.PayLPCost(tp,300)
end

-- Target filter: Banished Demon-Type monsters
function c10000108.filter(c)
	return c:IsFaceup() and c:IsRace(RACE_DEMON) and c:IsAbleToGrave()
end

-- Targeting: Up to 5 banished Demon monsters
function c10000108.target(e,tp,eg,ep,ev,re,r,rp,chk,chkc)
	if chkc then return chkc:IsLocation(LOCATION_REMOVED) and chkc:IsControler(tp) and c10000108.filter(chkc) end
	if chk==0 then return Duel.IsExistingTarget(c10000108.filter,tp,LOCATION_REMOVED,0,1,nil) end
	Duel.Hint(HINT_SELECTMSG,tp,HINTMSG_TOGRAVE)
	local g=Duel.SelectTarget(tp,c10000108.filter,tp,LOCATION_REMOVED,0,1,5,nil)
	Duel.SetOperationInfo(0,CATEGORY_TOGRAVE,g,#g,0,0)
end

-- Activation operation: Return banished monsters to GY
function c10000108.activate(e,tp,eg,ep,ev,re,r,rp)
	local tg=Duel.GetChainInfo(0,CHAININFO_TARGET_CARDS)
	local sg=tg:Filter(Card.IsRelateToEffect,nil,e)
	if #sg>0 then
		Duel.SendtoGrave(sg,REASON_EFFECT+REASON_RETURN)
	end
end
