MATH_EXPRESSION_REGEX = r"^\d+(\.\d+)?([-+/*]\d+(\.\d+)?)*"

MAGICAL = [
    "acid",
    "cold",
    "fire",
    "force",
    "lightning",
    "necrotic",
    "poison",
    "psychic",
    "radiant",
    "thunder"
]
NON_MAGICAL = [
    "bludgeoning",
    "slashing",
    "piercing"
]
ALL = MAGICAL + NON_MAGICAL
RESIST = ALL + ['magical', 'non-magical']

CAPITALISED_MAGICAL = [i.capitalize() for i in MAGICAL]
CAPITALISED_NON_MAGICAL = [i.capitalize() for i in NON_MAGICAL]
CAPITALISED_ALL = [i.capitalize() for i in ALL]
CAPITALISED_RESIST = [i.capitalize() for i in RESIST]

