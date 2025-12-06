"""
Yu-Gi-Oh! Game Constants
Based on the EDOPro/YGOPRO game engine constants
"""

# ============================================
# CARD TYPES
# ============================================
TYPE_MONSTER = 0x1
TYPE_SPELL = 0x2
TYPE_TRAP = 0x4
TYPE_NORMAL = 0x10
TYPE_EFFECT = 0x20
TYPE_FUSION = 0x40
TYPE_RITUAL = 0x80
TYPE_TRAPMONSTER = 0x100
TYPE_SPIRIT = 0x200
TYPE_UNION = 0x400
TYPE_DUAL = 0x800
TYPE_TUNER = 0x1000
TYPE_SYNCHRO = 0x2000
TYPE_TOKEN = 0x4000
TYPE_QUICKPLAY = 0x10000
TYPE_CONTINUOUS = 0x20000
TYPE_EQUIP = 0x40000
TYPE_FIELD = 0x80000
TYPE_COUNTER = 0x100000
TYPE_FLIP = 0x200000
TYPE_TOON = 0x400000
TYPE_XYZ = 0x800000
TYPE_PENDULUM = 0x1000000
TYPE_SPSUMMON = 0x2000000
TYPE_LINK = 0x4000000
TYPE_SKILL = 0x8000000
TYPE_ACTION = 0x10000000

# Common combinations
TYPE_MONSTER_NORMAL = TYPE_MONSTER | TYPE_NORMAL  # 0x11
TYPE_MONSTER_EFFECT = TYPE_MONSTER | TYPE_EFFECT  # 0x21
TYPE_SPELL_QUICKPLAY = TYPE_SPELL | TYPE_QUICKPLAY  # 0x10002
TYPE_SPELL_CONTINUOUS = TYPE_SPELL | TYPE_CONTINUOUS  # 0x20002
TYPE_SPELL_EQUIP = TYPE_SPELL | TYPE_EQUIP  # 0x40002
TYPE_SPELL_FIELD = TYPE_SPELL | TYPE_FIELD  # 0x80002
TYPE_TRAP_CONTINUOUS = TYPE_TRAP | TYPE_CONTINUOUS  # 0x20004
TYPE_TRAP_COUNTER = TYPE_TRAP | TYPE_COUNTER  # 0x100004

# ============================================
# ATTRIBUTES
# ============================================
ATTRIBUTE_EARTH = 0x01
ATTRIBUTE_WATER = 0x02
ATTRIBUTE_FIRE = 0x04
ATTRIBUTE_WIND = 0x08
ATTRIBUTE_LIGHT = 0x10
ATTRIBUTE_DARK = 0x20
ATTRIBUTE_DIVINE = 0x40

ATTRIBUTE_NAMES = {
    ATTRIBUTE_EARTH: "EARTH",
    ATTRIBUTE_WATER: "WATER",
    ATTRIBUTE_FIRE: "FIRE",
    ATTRIBUTE_WIND: "WIND",
    ATTRIBUTE_LIGHT: "LIGHT",
    ATTRIBUTE_DARK: "DARK",
    ATTRIBUTE_DIVINE: "DIVINE"
}

# ============================================
# RACES (Monster Types)
# ============================================
RACE_WARRIOR = 0x1
RACE_SPELLCASTER = 0x2
RACE_FAIRY = 0x4
RACE_FIEND = 0x8
RACE_ZOMBIE = 0x10
RACE_MACHINE = 0x20
RACE_AQUA = 0x40
RACE_PYRO = 0x80
RACE_ROCK = 0x100
RACE_WINDBEAST = 0x200
RACE_PLANT = 0x400
RACE_INSECT = 0x800
RACE_THUNDER = 0x1000
RACE_DRAGON = 0x2000
RACE_BEAST = 0x4000
RACE_BEASTWARRIOR = 0x8000
RACE_DINOSAUR = 0x10000
RACE_FISH = 0x20000
RACE_SEASERPENT = 0x40000
RACE_REPTILE = 0x80000
RACE_PSYCHO = 0x100000
RACE_DEVINE = 0x200000
RACE_CREATORGOD = 0x400000
RACE_WYRM = 0x800000
RACE_CYBERSE = 0x1000000
RACE_ILLUSION = 0x2000000

RACE_NAMES = {
    RACE_WARRIOR: "Warrior",
    RACE_SPELLCASTER: "Spellcaster",
    RACE_FAIRY: "Fairy",
    RACE_FIEND: "Fiend",
    RACE_ZOMBIE: "Zombie",
    RACE_MACHINE: "Machine",
    RACE_AQUA: "Aqua",
    RACE_PYRO: "Pyro",
    RACE_ROCK: "Rock",
    RACE_WINDBEAST: "Winged Beast",
    RACE_PLANT: "Plant",
    RACE_INSECT: "Insect",
    RACE_THUNDER: "Thunder",
    RACE_DRAGON: "Dragon",
    RACE_BEAST: "Beast",
    RACE_BEASTWARRIOR: "Beast-Warrior",
    RACE_DINOSAUR: "Dinosaur",
    RACE_FISH: "Fish",
    RACE_SEASERPENT: "Sea Serpent",
    RACE_REPTILE: "Reptile",
    RACE_PSYCHO: "Psychic",
    RACE_DEVINE: "Divine-Beast",
    RACE_CREATORGOD: "Creator God",
    RACE_WYRM: "Wyrm",
    RACE_CYBERSE: "Cyberse",
    RACE_ILLUSION: "Illusion"
}

# ============================================
# SCOPES (Card Legality)
# ============================================
SCOPE_OCG = 0x1
SCOPE_TCG = 0x2
SCOPE_ANIME = 0x4
SCOPE_ILLEGAL = 0x8
SCOPE_VIDEO_GAME = 0x10
SCOPE_CUSTOM = 0x20
SCOPE_SPEED = 0x40
SCOPE_PRERELEASE = 0x100
SCOPE_RUSH = 0x200
SCOPE_LEGEND = 0x400
SCOPE_HIDDEN = 0x1000

SCOPE_OCG_TCG = SCOPE_OCG | SCOPE_TCG  # 0x3 - Shows by default
SCOPE_OFFICIAL = SCOPE_OCG | SCOPE_TCG | SCOPE_PRERELEASE  # 0x103

SCOPE_NAMES = {
    SCOPE_OCG: "OCG",
    SCOPE_TCG: "TCG",
    SCOPE_ANIME: "Anime",
    SCOPE_ILLEGAL: "Illegal",
    SCOPE_VIDEO_GAME: "Video Game",
    SCOPE_CUSTOM: "Custom",
    SCOPE_SPEED: "Speed Duel",
    SCOPE_PRERELEASE: "Pre-release",
    SCOPE_RUSH: "Rush Duel",
    SCOPE_LEGEND: "Legend",
    SCOPE_HIDDEN: "Hidden"
}

# ============================================
# CATEGORIES (Effect Categories)
# ============================================
CATEGORY_DESTROY = 0x1
CATEGORY_RELEASE = 0x2
CATEGORY_REMOVE = 0x4
CATEGORY_TOHAND = 0x8
CATEGORY_TODECK = 0x10
CATEGORY_TOGRAVE = 0x20
CATEGORY_DECKDES = 0x40
CATEGORY_HANDES = 0x80
CATEGORY_SUMMON = 0x100
CATEGORY_SPECIAL_SUMMON = 0x200
CATEGORY_TOKEN = 0x400
CATEGORY_FLIP = 0x800
CATEGORY_POSITION = 0x1000
CATEGORY_CONTROL = 0x2000
CATEGORY_DISABLE = 0x4000
CATEGORY_DRAW = 0x8000
CATEGORY_SEARCH = 0x10000
CATEGORY_EQUIP = 0x20000
CATEGORY_DAMAGE = 0x40000
CATEGORY_RECOVER = 0x80000
CATEGORY_COUNTER = 0x100000
CATEGORY_COIN = 0x200000
CATEGORY_DICE = 0x400000
CATEGORY_FUSION_SUMMON = 0x800000
CATEGORY_TUNER = 0x1000000
CATEGORY_XYZ = 0x2000000
CATEGORY_NEGATE = 0x4000000
CATEGORY_LEVEL = 0x8000000
CATEGORY_ATKDEF = 0x10000000
CATEGORY_LEAVE_GRAVE = 0x20000000
CATEGORY_TOEXTRA = 0x40000000
CATEGORY_TOGRAVE_ONFIELD = 0x80000000

# ============================================
# LINK MARKERS
# ============================================
LINK_MARKER_BOTTOM_LEFT = 0x01
LINK_MARKER_BOTTOM = 0x02
LINK_MARKER_BOTTOM_RIGHT = 0x04
LINK_MARKER_LEFT = 0x08
LINK_MARKER_RIGHT = 0x20
LINK_MARKER_TOP_LEFT = 0x40
LINK_MARKER_TOP = 0x80
LINK_MARKER_TOP_RIGHT = 0x100

# ============================================
# POSITIONS
# ============================================
POS_FACEUP_ATTACK = 0x1
POS_FACEDOWN_ATTACK = 0x2
POS_FACEUP_DEFENSE = 0x4
POS_FACEDOWN_DEFENSE = 0x8
POS_FACEUP = POS_FACEUP_ATTACK | POS_FACEUP_DEFENSE
POS_FACEDOWN = POS_FACEDOWN_ATTACK | POS_FACEDOWN_DEFENSE
POS_ATTACK = POS_FACEUP_ATTACK | POS_FACEDOWN_ATTACK
POS_DEFENSE = POS_FACEUP_DEFENSE | POS_FACEDOWN_DEFENSE

# ============================================
# HELPER FUNCTIONS
# ============================================
def get_attribute_name(attribute):
    """Get attribute name from attribute value"""
    return ATTRIBUTE_NAMES.get(attribute, "Unknown")

def get_race_name(race):
    """Get race name from race value"""
    return RACE_NAMES.get(race, "Unknown")

def get_scope_name(scope):
    """Get scope name from scope value"""
    return SCOPE_NAMES.get(scope, "Unknown")

def parse_attribute(attr_string):
    """Parse attribute string to attribute value"""
    attr_upper = attr_string.upper()
    for value, name in ATTRIBUTE_NAMES.items():
        if name == attr_upper:
            return value
    return None

def parse_race(race_string):
    """Parse race string to race value"""
    race_lower = race_string.lower()
    for value, name in RACE_NAMES.items():
        if name.lower() == race_lower or name.lower().replace('-', '') == race_lower:
            return value
    return None

def parse_scope(scope_string):
    """Parse scope string to scope value"""
    scope_upper = scope_string.upper()
    for value, name in SCOPE_NAMES.items():
        if name.upper() == scope_upper:
            return value
    # Handle special cases
    if scope_upper == "OCG_TCG" or scope_upper == "OCGTCG":
        return SCOPE_OCG_TCG
    if scope_upper == "OFFICIAL":
        return SCOPE_OFFICIAL
    return None

def is_monster(card_type):
    """Check if card type is a monster"""
    return bool(card_type & TYPE_MONSTER)

def is_spell(card_type):
    """Check if card type is a spell"""
    return bool(card_type & TYPE_SPELL)

def is_trap(card_type):
    """Check if card type is a trap"""
    return bool(card_type & TYPE_TRAP)

