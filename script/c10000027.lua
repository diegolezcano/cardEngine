-- Huntrix Return
-- Card ID: 10000027
-- Card Name: Huntrix Return
-- Effect: Target 1 Demon Hunter monster in your GY; Special Summon it.

function c10000027.initial_effect(c)
	-- Special Summon Demon Hunter from GY
	local e1=Effect.CreateEffect(c)
	e1:SetCategory(CATEGORY_SPECIAL_SUMMON)
	e1:SetType(EFFECT_TYPE_ACTIVATE)
	e1:SetProperty(EFFECT_FLAG_CARD_TARGET)
	e1:SetCode(EVENT_FREE_CHAIN)
	e1:SetTarget(c10000027.target)
	e1:SetOperation(c10000027.activate)
	c:RegisterEffect(e1)
end

-- Check if target is valid
function c10000027.filter(c,e,tp)
	return c:IsRace(RACE_DEMON_HUNTER) and c:IsCanBeSpecialSummoned(e,0,tp,false,false)
end

-- Target: Select 1 Demon Hunter monster in GY
function c10000027.target(e,tp,eg,ep,ev,re,r,rp,chk,chkc)
	if chkc then return chkc:IsLocation(LOCATION_GRAVE) and chkc:IsControler(tp) and c10000027.filter(chkc,e,tp) end
	if chk==0 then return Duel.GetLocationCount(tp,LOCATION_MZONE)>0
		and Duel.IsExistingTarget(c10000027.filter,tp,LOCATION_GRAVE,0,1,nil,e,tp) end
	Duel.Hint(HINT_SELECTMSG,tp,HINTMSG_SPSUMMON)
	local g=Duel.SelectTarget(tp,c10000027.filter,tp,LOCATION_GRAVE,0,1,1,nil,e,tp)
	Duel.SetOperationInfo(0,CATEGORY_SPECIAL_SUMMON,g,1,0,0)
end

-- Activation: Special Summon the targeted monster
function c10000027.activate(e,tp,eg,ep,ev,re,r,rp)
	local tc=Duel.GetFirstTarget()
	if tc and tc:IsRelateToEffect(e) then
		Duel.SpecialSummon(tc,0,tp,tp,false,false,POS_FACEUP)
	end
end
