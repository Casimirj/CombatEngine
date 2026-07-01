import math
from enum import Enum


class Potion(Enum):
    """Combat-relevant potions and their boost formulas.

    Each boost is calculated as ``floor(level × percentage) + flat``.
    Negative percentages reduce the stat.

    Properties
    ----------
    label : str
        Display name.
    attack_percentage : float
        Percentage of base Attack level added as a boost.
    attack_flat : int
        Flat Attack boost added after the percentage.
    strength_percentage : float
        Percentage of base Strength level added as a boost.
    strength_flat : int
        Flat Strength boost added after the percentage.
    defence_percentage : float
        Percentage of base Defence level added as a boost.
    defence_flat : int
        Flat Defence boost added after the percentage.
    ranged_percentage : float
        Percentage of base Ranged level added as a boost.
    ranged_flat : int
        Flat Ranged boost added after the percentage.
    magic_percentage : float
        Percentage of base Magic level added as a boost.
    magic_flat : int
        Flat Magic boost added after the percentage.
    """

    # ------------------------------------------------------------------
    # No boost
    # ------------------------------------------------------------------
    NONE = {
        "label":               "None",
        "attack_percentage":   0.0,  "attack_flat":   0,
        "strength_percentage": 0.0,  "strength_flat":  0,
        "defence_percentage":  0.0,  "defence_flat":   0,
        "ranged_percentage":   0.0,  "ranged_flat":    0,
        "magic_percentage":    0.0,  "magic_flat":     0,
    }

    # ------------------------------------------------------------------
    # Melee potions
    # ------------------------------------------------------------------
    ATTACK = {
        "label":               "Attack potion",
        "attack_percentage":   0.10, "attack_flat":   3,
        "strength_percentage": 0.0,  "strength_flat":  0,
        "defence_percentage":  0.0,  "defence_flat":   0,
        "ranged_percentage":   0.0,  "ranged_flat":    0,
        "magic_percentage":    0.0,  "magic_flat":     0,
    }
    STRENGTH = {
        "label":               "Strength potion",
        "attack_percentage":   0.0,  "attack_flat":   0,
        "strength_percentage": 0.10, "strength_flat":  3,
        "defence_percentage":  0.0,  "defence_flat":   0,
        "ranged_percentage":   0.0,  "ranged_flat":    0,
        "magic_percentage":    0.0,  "magic_flat":     0,
    }
    SUPER_ATTACK = {
        "label":               "Super attack",
        "attack_percentage":   0.15, "attack_flat":   5,
        "strength_percentage": 0.0,  "strength_flat":  0,
        "defence_percentage":  0.0,  "defence_flat":   0,
        "ranged_percentage":   0.0,  "ranged_flat":    0,
        "magic_percentage":    0.0,  "magic_flat":     0,
    }
    SUPER_STRENGTH = {
        "label":               "Super strength",
        "attack_percentage":   0.0,  "attack_flat":   0,
        "strength_percentage": 0.15, "strength_flat":  5,
        "defence_percentage":  0.0,  "defence_flat":   0,
        "ranged_percentage":   0.0,  "ranged_flat":    0,
        "magic_percentage":    0.0,  "magic_flat":     0,
    }
    SUPER_DEFENCE = {
        "label":               "Super defence",
        "attack_percentage":   0.0,  "attack_flat":   0,
        "strength_percentage": 0.0,  "strength_flat":  0,
        "defence_percentage":  0.15, "defence_flat":   5,
        "ranged_percentage":   0.0,  "ranged_flat":    0,
        "magic_percentage":    0.0,  "magic_flat":     0,
    }
    SUPER_COMBAT = {
        "label":               "Super combat",
        "attack_percentage":   0.15, "attack_flat":   5,
        "strength_percentage": 0.15, "strength_flat":  5,
        "defence_percentage":  0.15, "defence_flat":   5,
        "ranged_percentage":   0.0,  "ranged_flat":    0,
        "magic_percentage":    0.0,  "magic_flat":     0,
    }
    ZAMORAK_BREW = {
        "label":               "Zamorak brew",
        "attack_percentage":   0.12, "attack_flat":   2,
        "strength_percentage": 0.12, "strength_flat":  2,
        "defence_percentage":  -0.10,"defence_flat":   -2,
        "ranged_percentage":   0.0,  "ranged_flat":    0,
        "magic_percentage":    0.0,  "magic_flat":     0,
    }
    BLACK_WARLOCK = {
        "label":               "Black warlock",
        "attack_percentage":   0.0,  "attack_flat":   0,
        "strength_percentage": 0.15, "strength_flat":  4,
        "defence_percentage":  0.0,  "defence_flat":   0,
        "ranged_percentage":   0.0,  "ranged_flat":    0,
        "magic_percentage":    0.0,  "magic_flat":     0,
    }

    # ------------------------------------------------------------------
    # Ranged potions
    # ------------------------------------------------------------------
    RANGING = {
        "label":               "Ranging potion",
        "attack_percentage":   0.0,  "attack_flat":   0,
        "strength_percentage": 0.0,  "strength_flat":  0,
        "defence_percentage":  0.0,  "defence_flat":   0,
        "ranged_percentage":   0.10, "ranged_flat":    4,
        "magic_percentage":    0.0,  "magic_flat":     0,
    }
    BASTION = {
        "label":               "Bastion potion",
        "attack_percentage":   0.0,  "attack_flat":   0,
        "strength_percentage": 0.0,  "strength_flat":  0,
        "defence_percentage":  0.15, "defence_flat":   5,
        "ranged_percentage":   0.10, "ranged_flat":    4,
        "magic_percentage":    0.0,  "magic_flat":     0,
    }

    # ------------------------------------------------------------------
    # Magic potions
    # ------------------------------------------------------------------
    MAGIC = {
        "label":               "Magic potion",
        "attack_percentage":   0.0,  "attack_flat":   0,
        "strength_percentage": 0.0,  "strength_flat":  0,
        "defence_percentage":  0.0,  "defence_flat":   0,
        "ranged_percentage":   0.0,  "ranged_flat":    0,
        "magic_percentage":    0.04, "magic_flat":     4,
    }
    BATTLEMAGE = {
        "label":               "Battlemage potion",
        "attack_percentage":   0.0,  "attack_flat":   0,
        "strength_percentage": 0.0,  "strength_flat":  0,
        "defence_percentage":  0.15, "defence_flat":   5,
        "ranged_percentage":   0.0,  "ranged_flat":    0,
        "magic_percentage":    0.04, "magic_flat":     4,
    }
    IMBUED_HEART = {
        "label":               "Imbued heart",
        "attack_percentage":   0.0,  "attack_flat":   0,
        "strength_percentage": 0.0,  "strength_flat":  0,
        "defence_percentage":  0.0,  "defence_flat":   0,
        "ranged_percentage":   0.0,  "ranged_flat":    0,
        "magic_percentage":    0.10, "magic_flat":     1,
    }
    SATURATED_HEART = {
        "label":               "Saturated heart",
        "attack_percentage":   0.0,  "attack_flat":   0,
        "strength_percentage": 0.0,  "strength_flat":  0,
        "defence_percentage":  0.0,  "defence_flat":   0,
        "ranged_percentage":   0.0,  "ranged_flat":    0,
        "magic_percentage":    0.10, "magic_flat":     4,
    }
    ANCIENT_BREW = {
        "label":               "Ancient brew",
        "attack_percentage":   -0.10,"attack_flat":   -2,
        "strength_percentage": -0.10,"strength_flat":  -2,
        "defence_percentage":  -0.10,"defence_flat":   -2,
        "ranged_percentage":   0.0,  "ranged_flat":    0,
        "magic_percentage":    0.05, "magic_flat":     2,
    }

    def __init__(self, props):
        self.label               = props["label"]
        self.attack_percentage   = props["attack_percentage"]
        self.attack_flat         = props["attack_flat"]
        self.strength_percentage = props["strength_percentage"]
        self.strength_flat       = props["strength_flat"]
        self.defence_percentage  = props["defence_percentage"]
        self.defence_flat        = props["defence_flat"]
        self.ranged_percentage   = props["ranged_percentage"]
        self.ranged_flat         = props["ranged_flat"]
        self.magic_percentage    = props["magic_percentage"]
        self.magic_flat          = props["magic_flat"]


    @staticmethod
    def compute_boost(level, percentage, flat):
        """Compute the boost value for a given level.

        ``floor(level × percentage) + flat`` for positive percentages;
        ``-(floor(level × |percentage|)) + flat`` for negative.
        """
        if percentage >= 0:
            return math.floor(level * percentage) + flat
        else:
            return -math.floor(level * abs(percentage)) + flat
