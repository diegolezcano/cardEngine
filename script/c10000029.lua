-- How it's Done, Done, Done
-- Card ID: 10000029
-- Card Name: How it's Done, Done, Done
-- Effect: Pay 500 LP; Special Summon up to 3 Demon Hunter monsters from your hand, Deck, and/or GY.

function c10000029.initial_effect(c)
	-- Pay 500 LP to Special Summon up to 3 Demon Hunter monsters
	local e1=Effect.CreateEffect(c)
	e1:SetCategory(CATEGORY_SPECIAL_SUMMON)
	e1:SetType(EFFECT_TYPE_ACTIVATE)
	e1:SetCode(EVENT_FREE_CHAIN)
	e1:SetCost(c10000029.cost)
	e1:SetTarget(c10000029.target)
	e1:SetOperation(c10000029.activate)
	c:RegisterEffect(e1)
end

-- Cost: Pay 500 LP
function c10000029.cost(e,tp,eg,ep,ev,re,r,rp,chk)
	if chk==0 then return Duel.CheckLPCost(tp,500) end
	Duel.PayLPCost(tp,500)
end

-- Filter: Demon Hunter monsters that can be special summoned
function c10000029.filter(c,e,tp)
	return c:IsRace(RACE_DEMON_HUNTER) and c:IsCanBeSpecialSummoned(e,0,tp,false,false)
end

-- Target: Check if there are Demon Hunter monsters available and monster zones
function c10000029.target(e,tp,eg,ep,ev,re,r,rp,chk)
	if chk==0 then
		local ft=Duel.GetLocationCount(tp,LOCATION_MZONE)
		if ft<=0 then return false end
		local loc=LOCATION_HAND+LOCATION_DECK+LOCATION_GRAVE
		return Duel.IsExistingMatchingCard(c10000029.filter,tp,loc,0,1,nil,e,tp)
	end
	Duel.SetOperationInfo(0,CATEGORY_SPECIAL_SUMMON,nil,1,tp,LOCATION_HAND+LOCATION_DECK+LOCATION_GRAVE)
end

-- Activation: Special Summon up to 3 Demon Hunter monsters
function c10000029.activate(e,tp,eg,ep,ev,re,r,rp)
	local ft=Duel.GetLocationCount(tp,LOCATION_MZONE)
	if ft<=0 then return end
	
	-- Limit to available monster zones and maximum of 3
	local ct=math.min(ft,3)
	local loc=LOCATION_HAND+LOCATION_DECK+LOCATION_GRAVE
	
	Duel.Hint(HINT_SELECTMSG,tp,HINTMSG_SPSUMMON)
	local g=Duel.SelectMatchingCard(tp,c10000029.filter,tp,loc,0,1,ct,nil,e,tp)
	
	if #g>0 then
		local tc=g:GetFirst()
		while tc do
			Duel.SpecialSummonStep(tc,0,tp,tp,false,false,POS_FACEUP)
			tc=g:GetNext()
		end
		Duel.SpecialSummonComplete()
	end
end
