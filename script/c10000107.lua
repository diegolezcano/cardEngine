-- Jinu - The Demon
-- Fusion Effect Monster (Extra Deck)
-- Summoning: Banish 5 Demon-Type monsters from GY
-- Effect: After attacking, destroy this card

function c10000107.initial_effect(c)
	-- Fusion monster designation
	c:EnableReviveLimit()
	
	-- Special Summon condition: Banish 5 Demon-Type monsters from GY
	local e1=Effect.CreateEffect(c)
	e1:SetType(EFFECT_TYPE_FIELD)
	e1:SetCode(EFFECT_SPSUMMON_PROC)
	e1:SetProperty(EFFECT_FLAG_CANNOT_DISABLE+EFFECT_FLAG_UNCOPYABLE)
	e1:SetRange(LOCATION_EXTRA)
	e1:SetCondition(c10000107.spcon)
	e1:SetTarget(c10000107.sptg)
	e1:SetOperation(c10000107.spop)
	c:RegisterEffect(e1)
	
	-- Destroy after attacking
	local e2=Effect.CreateEffect(c)
	e2:SetType(EFFECT_TYPE_SINGLE+EFFECT_TYPE_TRIGGER_F)
	e2:SetCode(EVENT_BATTLE_DAMAGE)
	e2:SetCondition(c10000107.descon)
	e2:SetOperation(c10000107.desop)
	c:RegisterEffect(e2)
	
	-- Also destroy if attack is negated
	local e3=Effect.CreateEffect(c)
	e3:SetType(EFFECT_TYPE_SINGLE+EFFECT_TYPE_TRIGGER_F)
	e3:SetCode(EVENT_BATTLED)
	e3:SetCondition(c10000107.descon2)
	e3:SetOperation(c10000107.desop)
	c:RegisterEffect(e3)
end

-- Special Summon condition check
function c10000107.spfilter(c)
	return c:IsRace(RACE_DEMON) and c:IsAbleToRemoveAsCost()
end

function c10000107.spcon(e,c)
	if c==nil then return true end
	local tp=c:GetControler()
	local rg=Duel.GetMatchingGroup(c10000107.spfilter,tp,LOCATION_GRAVE,0,nil)
	return Duel.GetLocationCount(tp,LOCATION_MZONE)>0 and #rg>=5
end

function c10000107.sptg(e,tp,eg,ep,ev,re,r,rp,chk,c)
	local rg=Duel.GetMatchingGroup(c10000107.spfilter,tp,LOCATION_GRAVE,0,nil)
	Duel.Hint(HINT_SELECTMSG,tp,HINTMSG_REMOVE)
	local sg=rg:Select(tp,5,5,nil)
	if sg then
		sg:KeepAlive()
		e:SetLabelObject(sg)
		return true
	else
		return false
	end
end

function c10000107.spop(e,tp,eg,ep,ev,re,r,rp,c)
	local g=e:GetLabelObject()
	if not g then return end
	Duel.Remove(g,POS_FACEUP,REASON_COST)
	g:DeleteGroup()
end

-- Destroy after dealing battle damage
function c10000107.descon(e,tp,eg,ep,ev,re,r,rp)
	return e:GetHandler()==Duel.GetAttacker() and Duel.GetAttackTarget()~=nil
end

-- Destroy after attacking (even if no damage)
function c10000107.descon2(e,tp,eg,ep,ev,re,r,rp)
	local c=e:GetHandler()
	return c==Duel.GetAttacker()
end

function c10000107.desop(e,tp,eg,ep,ev,re,r,rp)
	local c=e:GetHandler()
	if c:IsRelateToEffect(e) and c:IsFaceup() then
		Duel.Destroy(c,REASON_EFFECT)
	end
end
