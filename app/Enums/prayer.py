from enum import Enum


class Prayer(Enum):
    """Prayers and their effect multipliers for each combat style.

    Melee / Ranged multipliers apply to the effective level calculation
    (multiplied then floored).  Magic damage bonuses are additive (e.g. 0.04
    = +4% added to the PrimaryMagicDamage phase).

    Properties
    ----------
    label : str
        Display name.
    attack_multiplier : float
        Melee.  0.0 = no effect.
    strength_multiplier : float
        Melee.  0.0 = no effect.
    defence_multiplier : float
        Melee & Ranged & Magic.  0.0 = no effect.
    ranged_attack_multiplier : float
        0.0 = no effect.
    ranged_strength_multiplier : float
        0.0 = no effect.
    magic_attack_multiplier : float
        0.0 = no effect.
    magic_damage_bonus : float
        Additive bonus applied during the PrimaryMagicDamage phase.
        0.0 = no effect.
    """

    # ------------------------------------------------------------------
    # Melee prayers
    # ------------------------------------------------------------------
    NONE = {
        "label":                      "None",
        "attack_multiplier":          0.0,
        "strength_multiplier":        0.0,
        "defence_multiplier":         0.0,
        "ranged_attack_multiplier":   0.0,
        "ranged_strength_multiplier": 0.0,
        "magic_attack_multiplier":    0.0,
        "magic_damage_bonus":         0.0,
    }
    BURST_OF_STRENGTH = {
        "label":                      "Burst of Strength",
        "attack_multiplier":          1.05,
        "strength_multiplier":        1.05,
        "defence_multiplier":         0.0,
        "ranged_attack_multiplier":   0.0,
        "ranged_strength_multiplier": 0.0,
        "magic_attack_multiplier":    0.0,
        "magic_damage_bonus":         0.0,
    }
    SUPERNATURAL_STRENGTH = {
        "label":                      "Superhuman Strength",
        "attack_multiplier":          0.0,
        "strength_multiplier":        1.10,
        "defence_multiplier":         0.0,
        "ranged_attack_multiplier":   0.0,
        "ranged_strength_multiplier": 0.0,
        "magic_attack_multiplier":    0.0,
        "magic_damage_bonus":         0.0,
    }
    ULTIMATE_STRENGTH = {
        "label":                      "Ultimate Strength",
        "attack_multiplier":          0.0,
        "strength_multiplier":        1.15,
        "defence_multiplier":         0.0,
        "ranged_attack_multiplier":   0.0,
        "ranged_strength_multiplier": 0.0,
        "magic_attack_multiplier":    0.0,
        "magic_damage_bonus":         0.0,
    }
    CLARITY_OF_THOUGHT = {
        "label":                      "Clarity of Thought",
        "attack_multiplier":          1.05,
        "strength_multiplier":        0.0,
        "defence_multiplier":         0.0,
        "ranged_attack_multiplier":   0.0,
        "ranged_strength_multiplier": 0.0,
        "magic_attack_multiplier":    0.0,
        "magic_damage_bonus":         0.0,
    }
    IMPROVED_REFLEXES = {
        "label":                      "Improved Reflexes",
        "attack_multiplier":          1.10,
        "strength_multiplier":        0.0,
        "defence_multiplier":         0.0,
        "ranged_attack_multiplier":   0.0,
        "ranged_strength_multiplier": 0.0,
        "magic_attack_multiplier":    0.0,
        "magic_damage_bonus":         0.0,
    }
    INCREDIBLE_REFLEXES = {
        "label":                      "Incredible Reflexes",
        "attack_multiplier":          1.15,
        "strength_multiplier":        0.0,
        "defence_multiplier":         0.0,
        "ranged_attack_multiplier":   0.0,
        "ranged_strength_multiplier": 0.0,
        "magic_attack_multiplier":    0.0,
        "magic_damage_bonus":         0.0,
    }
    CHIVALRY = {
        "label":                      "Chivalry",
        "attack_multiplier":          1.15,
        "strength_multiplier":        1.18,
        "defence_multiplier":         1.20,
        "ranged_attack_multiplier":   0.0,
        "ranged_strength_multiplier": 0.0,
        "magic_attack_multiplier":    0.0,
        "magic_damage_bonus":         0.0,
    }
    PIETY = {
        "label":                      "Piety",
        "attack_multiplier":          1.20,
        "strength_multiplier":        1.23,
        "defence_multiplier":         1.25,
        "ranged_attack_multiplier":   0.0,
        "ranged_strength_multiplier": 0.0,
        "magic_attack_multiplier":    0.0,
        "magic_damage_bonus":         0.0,
    }

    # ------------------------------------------------------------------
    # Ranged prayers
    # ------------------------------------------------------------------
    SHARP_EYE = {
        "label":                      "Sharp Eye",
        "attack_multiplier":          0.0,
        "strength_multiplier":        0.0,
        "defence_multiplier":         0.0,
        "ranged_attack_multiplier":   1.05,
        "ranged_strength_multiplier": 1.05,
        "magic_attack_multiplier":    0.0,
        "magic_damage_bonus":         0.0,
    }
    HAWK_EYE = {
        "label":                      "Hawk Eye",
        "attack_multiplier":          0.0,
        "strength_multiplier":        0.0,
        "defence_multiplier":         0.0,
        "ranged_attack_multiplier":   1.10,
        "ranged_strength_multiplier": 1.10,
        "magic_attack_multiplier":    0.0,
        "magic_damage_bonus":         0.0,
    }
    EAGLE_EYE = {
        "label":                      "Eagle Eye",
        "attack_multiplier":          0.0,
        "strength_multiplier":        0.0,
        "defence_multiplier":         0.0,
        "ranged_attack_multiplier":   1.15,
        "ranged_strength_multiplier": 1.15,
        "magic_attack_multiplier":    0.0,
        "magic_damage_bonus":         0.0,
    }
    DEADEYE = {
        "label":                      "Deadeye",
        "attack_multiplier":          0.0,
        "strength_multiplier":        0.0,
        "defence_multiplier":         0.0,
        "ranged_attack_multiplier":   1.18,
        "ranged_strength_multiplier": 1.18,
        "magic_attack_multiplier":    0.0,
        "magic_damage_bonus":         0.0,
    }
    RIGOUR = {
        "label":                      "Rigour",
        "attack_multiplier":          0.0,
        "strength_multiplier":        0.0,
        "defence_multiplier":         1.25,
        "ranged_attack_multiplier":   1.20,
        "ranged_strength_multiplier": 1.23,
        "magic_attack_multiplier":    0.0,
        "magic_damage_bonus":         0.0,
    }

    # ------------------------------------------------------------------
    # Magic prayers
    # ------------------------------------------------------------------
    MYSTIC_WILL = {
        "label":                      "Mystic Will",
        "attack_multiplier":          0.0,
        "strength_multiplier":        0.0,
        "defence_multiplier":         0.0,
        "ranged_attack_multiplier":   0.0,
        "ranged_strength_multiplier": 0.0,
        "magic_attack_multiplier":    1.05,
        "magic_damage_bonus":         0.0,
    }
    MYSTIC_LORE = {
        "label":                      "Mystic Lore",
        "attack_multiplier":          0.0,
        "strength_multiplier":        0.0,
        "defence_multiplier":         0.0,
        "ranged_attack_multiplier":   0.0,
        "ranged_strength_multiplier": 0.0,
        "magic_attack_multiplier":    1.10,
        "magic_damage_bonus":         0.01,
    }
    MYSTIC_MIGHT = {
        "label":                      "Mystic Might",
        "attack_multiplier":          0.0,
        "strength_multiplier":        0.0,
        "defence_multiplier":         0.0,
        "ranged_attack_multiplier":   0.0,
        "ranged_strength_multiplier": 0.0,
        "magic_attack_multiplier":    1.15,
        "magic_damage_bonus":         0.02,
    }
    MYSTIC_VIGOUR = {
        "label":                      "Mystic Vigour",
        "attack_multiplier":          0.0,
        "strength_multiplier":        0.0,
        "defence_multiplier":         0.0,
        "ranged_attack_multiplier":   0.0,
        "ranged_strength_multiplier": 0.0,
        "magic_attack_multiplier":    1.18,
        "magic_damage_bonus":         0.03,
    }
    AUGURY = {
        "label":                      "Augury",
        "attack_multiplier":          0.0,
        "strength_multiplier":        0.0,
        "defence_multiplier":         1.25,
        "ranged_attack_multiplier":   0.0,
        "ranged_strength_multiplier": 0.0,
        "magic_attack_multiplier":    1.25,
        "magic_damage_bonus":         0.04,
    }

    def __init__(self, props):
        self.label                     = props["label"]
        self.attack_multiplier         = props["attack_multiplier"]
        self.strength_multiplier       = props["strength_multiplier"]
        self.defence_multiplier        = props["defence_multiplier"]
        self.ranged_attack_multiplier  = props["ranged_attack_multiplier"]
        self.ranged_strength_multiplier = props["ranged_strength_multiplier"]
        self.magic_attack_multiplier   = props["magic_attack_multiplier"]
        self.magic_damage_bonus        = props["magic_damage_bonus"]

    # Backward-compatible shorthand aliases
    @property
    def atk_mult(self):
        return self.attack_multiplier

    @property
    def str_mult(self):
        return self.strength_multiplier

    @property
    def def_mult(self):
        return self.defence_multiplier
