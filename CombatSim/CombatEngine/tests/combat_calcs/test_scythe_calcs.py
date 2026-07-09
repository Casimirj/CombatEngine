"""Melee damage and accuracy tests for Scythe-based setups.

Add new setups by appending a dict to SETUPS with:
    name                   — snake_case identifier for generated test names
    gear_names             — list of gear registry keys
    weapon                 — weapon registry key
    attack_style_override  — (optional) override weapon attack style
    prayer                 — (optional) Prayer enum; default PIETY
    boosts                 — (optional) list of Potion enums; default [SUPER_COMBAT]
    expected_accuracy_roll — expected player.attack_roll
    expected_max_hit       — expected player.max_hit (base, before Scythe splatting)

Scythe splats: max_hit + floor(max_hit/2) + floor(max_hit/4) = total.
"""

import unittest

from CombatSim.CombatEngine.Domain.Loadout import Loadout
from CombatSim.CombatEngine.Data.Registries.WeaponRegistry import WeaponRegistry
from CombatSim.CombatEngine.Data.Registries.PrayerRegistry import PrayerRegistry
from CombatSim.CombatEngine.Data.Registries.PotionRegistry import PotionRegistry

SETUPS = [
    # ── Basic Setup ───────────────────────────────────────────────────
    {
        "name": "TOO_setup",
        "prayer": "piety",
        "boosts": ["super combat"],
        "gear_names": [
            "torva full helm",
            "oathplate body",
            "oathplate legs",
            "amulet of rancour",
            "ultor ring",
            "avernic treads",
            "ferocious gloves",
            "infernal cape",
        ],
        "weapon": "scythe",
        "expected_accuracy_roll": 39783,
        "expected_max_hit": 50,  # scythe total: 50 + 25 + 12 = 87
    },
    # ── Basic + oathplate helm ────────────────────────────────────────
    {
        "name": "OOO_oathplate_helm",
        "prayer": "piety",
        "boosts": ["super combat"],
        "gear_names": [
            "oathplate helm",
            "oathplate body",
            "oathplate legs",
            "amulet of rancour",
            "ultor ring",
            "avernic treads",
            "ferocious gloves",
            "infernal cape",
        ],
        "weapon": "scythe",
        "expected_accuracy_roll": 41273,
        "expected_max_hit": 49,  # scythe total: 49 + 24 + 12 = 85
    },
    # ── Basic + fire cape ─────────────────────────────────────────────
    {
        "name": "TOO_fire_cape",
        "prayer": "piety",
        "boosts": ["super combat"],
        "gear_names": [
            "torva full helm",
            "oathplate body",
            "oathplate legs",
            "amulet of rancour",
            "ultor ring",
            "avernic treads",
            "ferocious gloves",
            "fire cape",
        ],
        "weapon": "scythe",
        "expected_accuracy_roll": 39336,
        "expected_max_hit": 49,  # scythe total: 49 + 24 + 12 = 85
    },
    # ── Basic + no piety ──────────────────────────────────────────────
    {
        "name": "TOO_no_piety",
        "gear_names": [
            "torva full helm",
            "oathplate body",
            "oathplate legs",
            "amulet of rancour",
            "ultor ring",
            "avernic treads",
            "ferocious gloves",
            "infernal cape",
        ],
        "weapon": "scythe",
        "prayer": "none",
        "boosts": ["super combat"],
        "expected_accuracy_roll": 33642,
        "expected_max_hit": 41,  # scythe total: 41 + 20 + 10 = 71
    },
    # ── Basic + accurate style ────────────────────────────────────────
    {
        "name": "TOO_accurate_style",
        "prayer": "piety",
        "boosts": ["super combat"],
        "gear_names": [
            "torva full helm",
            "oathplate body",
            "oathplate legs",
            "amulet of rancour",
            "ultor ring",
            "avernic treads",
            "ferocious gloves",
            "infernal cape",
        ],
        "weapon": "scythe",
        "attack_style_override": "Accurate",
        "expected_accuracy_roll": 40584,
        "expected_max_hit": 49,  # scythe total: 49 + 24 + 12 = 85
    },
    # ── Basic + no supercombat ────────────────────────────────────────
    {
        "name": "TOO_no_supercombat",
        "prayer": "piety",
        "gear_names": [
            "torva full helm",
            "oathplate body",
            "oathplate legs",
            "amulet of rancour",
            "ultor ring",
            "avernic treads",
            "ferocious gloves",
            "infernal cape",
        ],
        "weapon": "scythe",
        "boosts": ["none"],
        "expected_accuracy_roll": 33642,
        "expected_max_hit": 42,  # scythe total: 42 + 21 + 10 = 73
    },
    # ── Basic + no supercombat + no piety ─────────────────────────────
    {
        "name": "TOO_no_scb_no_piety",
        "gear_names": [
            "torva full helm",
            "oathplate body",
            "oathplate legs",
            "amulet of rancour",
            "ultor ring",
            "avernic treads",
            "ferocious gloves",
            "infernal cape",
        ],
        "weapon": "scythe",
        "prayer": "none",
        "boosts": ["none"],
        "expected_accuracy_roll": 28569,
        "expected_max_hit": 35,  # scythe total: 35 + 17 + 8 = 60
    },
    # ── Basic + torva body + torva legs ───────────────────────────────
    {
        "name": "TTT_torva_body_legs",
        "prayer": "piety",
        "boosts": ["super combat"],
        "gear_names": [
            "torva full helm",
            "torva platebody",
            "torva platelegs",
            "amulet of rancour",
            "ultor ring",
            "avernic treads",
            "ferocious gloves",
            "infernal cape",
        ],
        "weapon": "scythe",
        "expected_accuracy_roll": 35611,
        "expected_max_hit": 51,  # scythe total: 51 + 25 + 12 = 88
    },
    # ── Basic + bandos + no necklace ──────────────────────────────────
    {
        "name": "TOO_bandos_no_neck",
        "prayer": "piety",
        "boosts": ["super combat"],
        "gear_names": [
            "torva full helm",
            "bandos chestplate",
            "bandos tassets",
            "ultor ring",
            "avernic treads",
            "ferocious gloves",
            "infernal cape",
        ],
        "weapon": "scythe",
        "expected_accuracy_roll": 31886,
        "expected_max_hit": 47,  # scythe total: 47 + 23 + 11 = 81
    },
    # ── Basic + bandos + no necklace + no gloves ──────────────────────
    {
        "name": "TOO_bandos_no_neck_no_gloves",
        "prayer": "piety",
        "boosts": ["super combat"],
        "gear_names": [
            "torva full helm",
            "bandos chestplate",
            "bandos tassets",
            "ultor ring",
            "avernic treads",
            "infernal cape",
        ],
        "weapon": "scythe",
        "expected_accuracy_roll": 29502,
        "expected_max_hit": 44,  # scythe total: 44 + 22 + 11 = 77
    },
    # ── OOO: oathplate helm/body/legs variants ─────────────────────────
    {
        "name": "OOO_torture",
        "prayer": "piety",
        "boosts": ["super combat"],
        "gear_names": [
            "oathplate helm",
            "oathplate body",
            "oathplate legs",
            "amulet of torture",
            "ultor ring",
            "avernic treads",
            "ferocious gloves",
            "infernal cape",
            "avernic defender",
        ],
        "weapon": "scythe",
        "expected_accuracy_roll": 44104,
        "expected_max_hit": 51,  # scythe total: 51 + 25 + 12 = 88
    },
    {
        "name": "OOO_fury",
        "prayer": "piety",
        "boosts": ["super combat"],
        "gear_names": [
            "oathplate helm",
            "oathplate body",
            "oathplate legs",
            "amulet of fury",
            "ultor ring",
            "avernic treads",
            "ferocious gloves",
            "infernal cape",
            "avernic defender",
        ],
        "weapon": "scythe",
        "expected_accuracy_roll": 43359,
        "expected_max_hit": 50,  # scythe total: 50 + 25 + 12 = 87
    },
    {
        "name": "OOO_strength",
        "prayer": "piety",
        "boosts": ["super combat"],
        "gear_names": [
            "oathplate helm",
            "oathplate body",
            "oathplate legs",
            "amulet of strength",
            "ultor ring",
            "avernic treads",
            "ferocious gloves",
            "infernal cape",
            "avernic defender",
        ],
        "weapon": "scythe",
        "expected_accuracy_roll": 41869,
        "expected_max_hit": 51,  # scythe total: 51 + 25 + 12 = 88
    },
    {
        "name": "OOO_bring",
        "prayer": "piety",
        "boosts": ["super combat"],
        "gear_names": [
            "oathplate helm",
            "oathplate body",
            "oathplate legs",
            "amulet of rancour",
            "berserker ring (i)",
            "avernic treads",
            "ferocious gloves",
            "infernal cape",
            "avernic defender",
        ],
        "weapon": "scythe",
        "expected_accuracy_roll": 45594,
        "expected_max_hit": 50,  # scythe total: 50 + 25 + 12 = 87
    },
    {
        "name": "OOO_prims",
        "prayer": "piety",
        "boosts": ["super combat"],
        "gear_names": [
            "oathplate helm",
            "oathplate body",
            "oathplate legs",
            "amulet of rancour",
            "ultor ring",
            "primordial boots",
            "ferocious gloves",
            "infernal cape",
            "avernic defender",
        ],
        "weapon": "scythe",
        "expected_accuracy_roll": 45147,
        "expected_max_hit": 51,  # scythe total: 51 + 25 + 12 = 88
    },
    {
        "name": "OOO_chivalry",
        "gear_names": [
            "oathplate helm",
            "oathplate body",
            "oathplate legs",
            "amulet of rancour",
            "ultor ring",
            "avernic treads",
            "ferocious gloves",
            "infernal cape",
            "avernic defender",
        ],
        "weapon": "scythe",
        "prayer": "chivalry",
        "boosts": ["super combat"],
        "expected_accuracy_roll": 43758,
        "expected_max_hit": 49,  # scythe total: 49 + 24 + 12 = 85
    },
    {
        "name": "OOO_ultimate_strength",
        "gear_names": [
            "oathplate helm",
            "oathplate body",
            "oathplate legs",
            "amulet of rancour",
            "ultor ring",
            "avernic treads",
            "ferocious gloves",
            "infernal cape",
            "avernic defender",
        ],
        "weapon": "scythe",
        "prayer": "ultimate strength",
        "boosts": ["super combat"],
        "expected_accuracy_roll": 38556,
        "expected_max_hit": 48,  # scythe total: 48 + 24 + 12 = 84
    },
    {
        "name": "OOO_burst_of_strength",
        "gear_names": [
            "oathplate helm",
            "oathplate body",
            "oathplate legs",
            "amulet of rancour",
            "ultor ring",
            "avernic treads",
            "ferocious gloves",
            "infernal cape",
            "avernic defender",
        ],
        "weapon": "scythe",
        "prayer": "BURST_OF_STRENGTH",
        "boosts": ["super combat"],
        "expected_accuracy_roll": 40086,
        "expected_max_hit": 44,  # scythe total: 44 + 22 + 11 = 77
    },
    {
        "name": "OOO_zamorak_brew",
        "prayer": "piety",
        "gear_names": [
            "oathplate helm",
            "oathplate body",
            "oathplate legs",
            "amulet of rancour",
            "ultor ring",
            "avernic treads",
            "ferocious gloves",
            "infernal cape",
            "avernic defender",
        ],
        "weapon": "scythe",
        "boosts": ["zamorak brew"],
        "expected_accuracy_roll": 43452,
        "expected_max_hit": 49,  # scythe total: 49 + 24 + 12 = 85
    },
    {
        "name": "OOO_ancient_brew",
        "prayer": "piety",
        "gear_names": [
            "oathplate helm",
            "oathplate body",
            "oathplate legs",
            "amulet of rancour",
            "ultor ring",
            "avernic treads",
            "ferocious gloves",
            "infernal cape",
            "avernic defender",
        ],
        "weapon": "scythe",
        "boosts": ["ancient brew"],
        "expected_accuracy_roll": 34578,
        "expected_max_hit": 39,  # scythe total: 39 + 19 + 9 = 67
    },
    {
        "name": "OOO_super_attack",
        "prayer": "piety",
        "gear_names": [
            "oathplate helm",
            "oathplate body",
            "oathplate legs",
            "amulet of rancour",
            "ultor ring",
            "avernic treads",
            "ferocious gloves",
            "infernal cape",
            "avernic defender",
        ],
        "weapon": "scythe",
        "boosts": ["SUPER_ATTACK"],
        "expected_accuracy_roll": 45594,
        "expected_max_hit": 44,  # scythe total: 44 + 22 + 11 = 77
    },
    {
        "name": "OOO_chivalry_zamorak",
        "gear_names": [
            "oathplate helm",
            "oathplate body",
            "oathplate legs",
            "amulet of rancour",
            "ultor ring",
            "avernic treads",
            "ferocious gloves",
            "infernal cape",
            "avernic defender",
        ],
        "weapon": "scythe",
        "prayer": "chivalry",
        "boosts": ["zamorak brew"],
        "expected_accuracy_roll": 41616,
        "expected_max_hit": 47,  # scythe total: 47 + 23 + 11 = 81
    },
    {
        "name": "OOO_no_piety_ancient",
        "gear_names": [
            "oathplate helm",
            "oathplate body",
            "oathplate legs",
            "amulet of rancour",
            "ultor ring",
            "avernic treads",
            "ferocious gloves",
            "infernal cape",
            "avernic defender",
        ],
        "weapon": "scythe",
        "prayer": "none",
        "boosts": ["ancient brew"],
        "expected_accuracy_roll": 29376,
        "expected_max_hit": 33,  # scythe total: 33 + 16 + 8 = 57
    },
    {
        "name": "OOO_burst_strength_no_pot",
        "gear_names": [
            "oathplate helm",
            "oathplate body",
            "oathplate legs",
            "amulet of rancour",
            "ultor ring",
            "avernic treads",
            "ferocious gloves",
            "infernal cape",
            "avernic defender",
        ],
        "weapon": "scythe",
        "prayer": "BURST_OF_STRENGTH",
        "boosts": ["none"],
        "expected_accuracy_roll": 33966,
        "expected_max_hit": 38,  # scythe total: 38 + 19 + 9 = 66
    },
    {
        "name": "OOO_accurate_style",
        "prayer": "piety",
        "boosts": ["super combat"],
        "gear_names": [
            "oathplate helm",
            "oathplate body",
            "oathplate legs",
            "amulet of rancour",
            "ultor ring",
            "avernic treads",
            "ferocious gloves",
            "infernal cape",
            "avernic defender",
        ],
        "weapon": "scythe",
        "attack_style_override": "Accurate",
        "expected_accuracy_roll": 46512,
        "expected_max_hit": 50,  # scythe total: 50 + 25 + 12 = 87
    },
    {
        "name": "OOO_fire_cape",
        "prayer": "piety",
        "boosts": ["super combat"],
        "gear_names": [
            "oathplate helm",
            "oathplate body",
            "oathplate legs",
            "amulet of rancour",
            "ultor ring",
            "avernic treads",
            "ferocious gloves",
            "fire cape",
            "avernic defender",
        ],
        "weapon": "scythe",
        "expected_accuracy_roll": 45147,
        "expected_max_hit": 50,  # scythe total: 50 + 25 + 12 = 87
    },
    {
        "name": "OOO_no_defender",
        "prayer": "piety",
        "boosts": ["super combat"],
        "gear_names": [
            "oathplate helm",
            "oathplate body",
            "oathplate legs",
            "amulet of rancour",
            "ultor ring",
            "avernic treads",
            "ferocious gloves",
            "infernal cape",
        ],
        "weapon": "scythe",
        "expected_accuracy_roll": 41273,
        "expected_max_hit": 49,  # scythe total: 49 + 24 + 12 = 85
    },
    {
        "name": "OOO_salve",
        "prayer": "piety",
        "boosts": ["super combat"],
        "gear_names": [
            "oathplate helm",
            "oathplate body",
            "oathplate legs",
            "salve",
            "ultor ring",
            "avernic treads",
            "ferocious gloves",
            "infernal cape",
            "avernic defender",
        ],
        "weapon": "scythe",
        "expected_accuracy_roll": 41869,
        "expected_max_hit": 49,  # scythe total: 49 + 24 + 12 = 85
    },
    {
        "name": "OOO_torture_bring_prims",
        "prayer": "piety",
        "boosts": ["super combat"],
        "gear_names": [
            "oathplate helm",
            "oathplate body",
            "oathplate legs",
            "amulet of torture",
            "berserker ring (i)",
            "primordial boots",
            "ferocious gloves",
            "infernal cape",
            "avernic defender",
        ],
        "weapon": "scythe",
        "expected_accuracy_roll": 43657,
        "expected_max_hit": 50,  # scythe total: 50 + 25 + 12 = 87
    },
    {
        "name": "OOO_fury_bandos",
        "prayer": "piety",
        "boosts": ["super combat"],
        "gear_names": [
            "oathplate helm",
            "bandos chestplate",
            "oathplate legs",
            "amulet of fury",
            "ultor ring",
            "avernic treads",
            "ferocious gloves",
            "infernal cape",
            "avernic defender",
        ],
        "weapon": "scythe",
        "expected_accuracy_roll": 40975,
        "expected_max_hit": 50,  # scythe total: 50 + 25 + 12 = 87
    },
    # ── TOO: torva helm + oath body/legs variants ──────────────────────
    {
        "name": "TOO_torture",
        "prayer": "piety",
        "boosts": ["super combat"],
        "gear_names": [
            "torva full helm",
            "oathplate body",
            "oathplate legs",
            "amulet of torture",
            "ultor ring",
            "avernic treads",
            "ferocious gloves",
            "infernal cape",
            "avernic defender",
        ],
        "weapon": "scythe",
        "expected_accuracy_roll": 42614,
        "expected_max_hit": 51,  # scythe total: 51 + 25 + 12 = 88
    },
    {
        "name": "TOO_fury",
        "prayer": "piety",
        "boosts": ["super combat"],
        "gear_names": [
            "torva full helm",
            "oathplate body",
            "oathplate legs",
            "amulet of fury",
            "ultor ring",
            "avernic treads",
            "ferocious gloves",
            "infernal cape",
            "avernic defender",
        ],
        "weapon": "scythe",
        "expected_accuracy_roll": 41869,
        "expected_max_hit": 51,  # scythe total: 51 + 25 + 12 = 88
    },
    {
        "name": "TOO_strength",
        "prayer": "piety",
        "boosts": ["super combat"],
        "gear_names": [
            "torva full helm",
            "oathplate body",
            "oathplate legs",
            "amulet of strength",
            "ultor ring",
            "avernic treads",
            "ferocious gloves",
            "infernal cape",
            "avernic defender",
        ],
        "weapon": "scythe",
        "expected_accuracy_roll": 40379,
        "expected_max_hit": 51,  # scythe total: 51 + 25 + 12 = 88
    },
    {
        "name": "TOO_bring",
        "prayer": "piety",
        "boosts": ["super combat"],
        "gear_names": [
            "torva full helm",
            "oathplate body",
            "oathplate legs",
            "amulet of rancour",
            "berserker ring (i)",
            "avernic treads",
            "ferocious gloves",
            "infernal cape",
            "avernic defender",
        ],
        "weapon": "scythe",
        "expected_accuracy_roll": 44104,
        "expected_max_hit": 51,  # scythe total: 51 + 25 + 12 = 88
    },
    {
        "name": "TOO_prims",
        "prayer": "piety",
        "boosts": ["super combat"],
        "gear_names": [
            "torva full helm",
            "oathplate body",
            "oathplate legs",
            "amulet of rancour",
            "ultor ring",
            "primordial boots",
            "ferocious gloves",
            "infernal cape",
            "avernic defender",
        ],
        "weapon": "scythe",
        "expected_accuracy_roll": 43657,
        "expected_max_hit": 52,  # scythe total: 52 + 26 + 13 = 91
    },
    {
        "name": "TOO_zamorak_brew",
        "prayer": "piety",
        "gear_names": [
            "torva full helm",
            "oathplate body",
            "oathplate legs",
            "amulet of rancour",
            "ultor ring",
            "avernic treads",
            "ferocious gloves",
            "infernal cape",
            "avernic defender",
        ],
        "weapon": "scythe",
        "boosts": ["zamorak brew"],
        "expected_accuracy_roll": 42032,
        "expected_max_hit": 49,  # scythe total: 49 + 24 + 12 = 85
    },
    {
        "name": "TOO_ancient_brew",
        "prayer": "piety",
        "gear_names": [
            "torva full helm",
            "oathplate body",
            "oathplate legs",
            "amulet of rancour",
            "ultor ring",
            "avernic treads",
            "ferocious gloves",
            "infernal cape",
            "avernic defender",
        ],
        "weapon": "scythe",
        "boosts": ["ancient brew"],
        "expected_accuracy_roll": 33448,
        "expected_max_hit": 40,  # scythe total: 40 + 20 + 10 = 70
    },
    {
        "name": "TOO_chivalry",
        "gear_names": [
            "torva full helm",
            "oathplate body",
            "oathplate legs",
            "amulet of rancour",
            "ultor ring",
            "avernic treads",
            "ferocious gloves",
            "infernal cape",
            "avernic defender",
        ],
        "weapon": "scythe",
        "prayer": "chivalry",
        "boosts": ["super combat"],
        "expected_accuracy_roll": 42328,
        "expected_max_hit": 50,  # scythe total: 50 + 25 + 12 = 87
    },
    {
        "name": "TOO_ultimate_strength",
        "gear_names": [
            "torva full helm",
            "oathplate body",
            "oathplate legs",
            "amulet of rancour",
            "ultor ring",
            "avernic treads",
            "ferocious gloves",
            "infernal cape",
            "avernic defender",
        ],
        "weapon": "scythe",
        "prayer": "ultimate strength",
        "boosts": ["super combat"],
        "expected_accuracy_roll": 37296,
        "expected_max_hit": 49,  # scythe total: 49 + 24 + 12 = 85
    },
    {
        "name": "TOO_fire_cape",
        "prayer": "piety",
        "boosts": ["super combat"],
        "gear_names": [
            "torva full helm",
            "oathplate body",
            "oathplate legs",
            "amulet of rancour",
            "ultor ring",
            "avernic treads",
            "ferocious gloves",
            "fire cape",
            "avernic defender",
        ],
        "weapon": "scythe",
        "expected_accuracy_roll": 43657,
        "expected_max_hit": 51,  # scythe total: 51 + 25 + 12 = 88
    },

    # ── Only Scythe ───────────────────────────────────────────────────
    {
        "name": "only_scythe",
        "prayer": "piety",
        "boosts": ["super combat"],
        "gear_names": [],
        "weapon": "scythe",
        "expected_accuracy_roll": 28161,
        "expected_max_hit": 34,  # scythe total: 34 + 17 + 8 = 59
    },
    # ── Only Scythe + ultor ───────────────────────────────────────────
    {
        "name": "only_ultor",
        "prayer": "piety",
        "boosts": ["super combat"],
        "gear_names": [
            "ultor ring",
        ],
        "weapon": "scythe",
        "expected_accuracy_roll": 28161,
        "expected_max_hit": 37,  # scythe total: 37 + 18 + 9 = 64
    },
    # ── New gear: single-item bare tests ────────────────────────────────
    {
        "name": "only_amulet_of_torture",
        "prayer": "piety",
        "boosts": ["super combat"],
        "gear_names": [
            "amulet of torture",
        ],
        "weapon": "scythe",
        "expected_accuracy_roll": 30396,
        "expected_max_hit": 36,  # scythe total: 36 + 18 + 9 = 63
    },
    {
        "name": "only_berserker_ring_i",
        "prayer": "piety",
        "boosts": ["super combat"],
        "gear_names": [
            "berserker ring (i)",
        ],
        "weapon": "scythe",
        "expected_accuracy_roll": 28161,
        "expected_max_hit": 36,  # scythe total: 36 + 18 + 9 = 63
    },
    {
        "name": "only_primordial_boots",
        "prayer": "piety",
        "boosts": ["super combat"],
        "gear_names": [
            "primordial boots",
        ],
        "weapon": "scythe",
        "expected_accuracy_roll": 28459,
        "expected_max_hit": 35,  # scythe total: 35 + 17 + 8 = 60
    },
    {
        "name": "only_amulet_of_fury",
        "prayer": "piety",
        "boosts": ["super combat"],
        "gear_names": [
            "amulet of fury",
        ],
        "weapon": "scythe",
        "expected_accuracy_roll": 29651,
        "expected_max_hit": 36,  # scythe total: 36 + 18 + 9 = 63
    },
    {
        "name": "only_amulet_of_strength",
        "prayer": "piety",
        "boosts": ["super combat"],
        "gear_names": [
            "amulet of strength",
        ],
        "weapon": "scythe",
        "expected_accuracy_roll": 28161,
        "expected_max_hit": 36,  # scythe total: 36 + 18 + 9 = 63
    },
    # ── New gear: pair combinations ─────────────────────────────────────
    {
        "name": "only_torture_bring",
        "prayer": "piety",
        "boosts": ["super combat"],
        "gear_names": [
            "amulet of torture",
            "berserker ring (i)",
        ],
        "weapon": "scythe",
        "expected_accuracy_roll": 30396,
        "expected_max_hit": 38,  # scythe total: 38 + 19 + 9 = 66
    },
    {
        "name": "only_torture_prims",
        "prayer": "piety",
        "boosts": ["super combat"],
        "gear_names": [
            "amulet of torture",
            "primordial boots",
        ],
        "weapon": "scythe",
        "expected_accuracy_roll": 30694,
        "expected_max_hit": 38,  # scythe total: 38 + 19 + 9 = 66
    },
    {
        "name": "only_fury_bring",
        "prayer": "piety",
        "boosts": ["super combat"],
        "gear_names": [
            "amulet of fury",
            "berserker ring (i)",
        ],
        "weapon": "scythe",
        "expected_accuracy_roll": 29651,
        "expected_max_hit": 38,  # scythe total: 38 + 19 + 9 = 66
    },
    {
        "name": "only_fury_prims",
        "prayer": "piety",
        "boosts": ["super combat"],
        "gear_names": [
            "amulet of fury",
            "primordial boots",
        ],
        "weapon": "scythe",
        "expected_accuracy_roll": 29949,
        "expected_max_hit": 37,  # scythe total: 37 + 18 + 9 = 64
    },
    {
        "name": "only_strength_bring",
        "prayer": "piety",
        "boosts": ["super combat"],
        "gear_names": [
            "amulet of strength",
            "berserker ring (i)",
        ],
        "weapon": "scythe",
        "expected_accuracy_roll": 28161,
        "expected_max_hit": 38,  # scythe total: 38 + 19 + 9 = 66
    },
    # ── New gear: mixed with old gear ────────────────────────────────────
    {
        "name": "only_torture_ferocious",
        "prayer": "piety",
        "boosts": ["super combat"],
        "gear_names": [
            "amulet of torture",
            "ferocious gloves",
        ],
        "weapon": "scythe",
        "expected_accuracy_roll": 32780,
        "expected_max_hit": 40,  # scythe total: 40 + 20 + 10 = 70
    },
    {
        "name": "only_fury_infernal",
        "prayer": "piety",
        "boosts": ["super combat"],
        "gear_names": [
            "amulet of fury",
            "infernal cape",
        ],
        "weapon": "scythe",
        "expected_accuracy_roll": 30247,
        "expected_max_hit": 38,  # scythe total: 38 + 19 + 9 = 66
    },
    {
        "name": "only_bring_ferocious",
        "prayer": "piety",
        "boosts": ["super combat"],
        "gear_names": [
            "berserker ring (i)",
            "ferocious gloves",
        ],
        "weapon": "scythe",
        "expected_accuracy_roll": 30545,
        "expected_max_hit": 39,  # scythe total: 39 + 19 + 9 = 67
    },
    {
        "name": "only_prims_rancour",
        "prayer": "piety",
        "boosts": ["super combat"],
        "gear_names": [
            "primordial boots",
            "amulet of rancour",
        ],
        "weapon": "scythe",
        "expected_accuracy_roll": 32184,
        "expected_max_hit": 38,  # scythe total: 38 + 19 + 9 = 66
    },
    {
        "name": "only_torture_infernal",
        "prayer": "piety",
        "boosts": ["super combat"],
        "gear_names": [
            "amulet of torture",
            "infernal cape",
        ],
        "weapon": "scythe",
        "expected_accuracy_roll": 30992,
        "expected_max_hit": 38,  # scythe total: 38 + 19 + 9 = 66
    },
    # ── New gear: three-item combos ──────────────────────────────────────
    {
        "name": "only_torture_bring_prims",
        "prayer": "piety",
        "boosts": ["super combat"],
        "gear_names": [
            "amulet of torture",
            "berserker ring (i)",
            "primordial boots",
        ],
        "weapon": "scythe",
        "expected_accuracy_roll": 30694,
        "expected_max_hit": 39,  # scythe total: 39 + 19 + 9 = 67
    },
    {
        "name": "only_fury_bring_prims",
        "prayer": "piety",
        "boosts": ["super combat"],
        "gear_names": [
            "amulet of fury",
            "berserker ring (i)",
            "primordial boots",
        ],
        "weapon": "scythe",
        "expected_accuracy_roll": 29949,
        "expected_max_hit": 39,  # scythe total: 39 + 19 + 9 = 67
    },
    # ── New gear: no piety / no scb variants ────────────────────────────
    {
        "name": "only_torture_bring_no_piety",
        "gear_names": [
            "amulet of torture",
            "berserker ring (i)",
        ],
        "weapon": "scythe",
        "prayer": "none",
        "boosts": ["super combat"],
        "expected_accuracy_roll": 25704,
        "expected_max_hit": 32,  # scythe total: 32 + 16 + 8 = 56
    },
    {
        "name": "only_fury_bring_no_scb",
        "prayer": "piety",
        "gear_names": [
            "amulet of fury",
            "berserker ring (i)",
        ],
        "weapon": "scythe",
        "boosts": ["none"],
        "expected_accuracy_roll": 25074,
        "expected_max_hit": 32,  # scythe total: 32 + 16 + 8 = 56
    },
    # ── Potion variants ────────────────────────────────────────────────────
    {
        "name": "TTT_super_combat",
        "prayer": "piety",
        "gear_names": [
            "torva full helm",
            "torva platebody",
            "torva platelegs",
            "amulet of rancour",
            "ultor ring",
            "avernic treads",
            "ferocious gloves",
            "infernal cape",
            "avernic defender",
        ],
        "weapon": "scythe",
        "boosts": ["super combat"],
        "expected_accuracy_roll": 39932,
        "expected_max_hit": 53,  # scythe total: 53 + 26 + 13 = 92
    },
    {
        "name": "TTT_super_atk_str",
        "prayer": "piety",
        "gear_names": [
            "torva full helm",
            "torva platebody",
            "torva platelegs",
            "amulet of rancour",
            "ultor ring",
            "avernic treads",
            "ferocious gloves",
            "infernal cape",
            "avernic defender",
        ],
        "weapon": "scythe",
        "boosts": ["SUPER_ATTACK", "SUPER_STRENGTH"],
        "expected_accuracy_roll": 39932,
        "expected_max_hit": 53,  # scythe total: 53 + 26 + 13 = 92
    },
    {
        "name": "TTT_zamorak_brew",
        "prayer": "piety",
        "gear_names": [
            "torva full helm",
            "torva platebody",
            "torva platelegs",
            "amulet of rancour",
            "ultor ring",
            "avernic treads",
            "ferocious gloves",
            "infernal cape",
            "avernic defender",
        ],
        "weapon": "scythe",
        "boosts": ["zamorak brew"],
        "expected_accuracy_roll": 38056,
        "expected_max_hit": 50,  # scythe total: 50 + 25 + 12 = 87
    },
    {
        "name": "TTT_ancient_brew",
        "prayer": "piety",
        "gear_names": [
            "torva full helm",
            "torva platebody",
            "torva platelegs",
            "amulet of rancour",
            "ultor ring",
            "avernic treads",
            "ferocious gloves",
            "infernal cape",
            "avernic defender",
        ],
        "weapon": "scythe",
        "boosts": ["ancient brew"],
        "expected_accuracy_roll": 30284,
        "expected_max_hit": 40,  # scythe total: 40 + 20 + 10 = 70
    },
    {
        "name": "TTT_attack_potion",
        "prayer": "piety",
        "gear_names": [
            "torva full helm",
            "torva platebody",
            "torva platelegs",
            "amulet of rancour",
            "ultor ring",
            "avernic treads",
            "ferocious gloves",
            "infernal cape",
            "avernic defender",
        ],
        "weapon": "scythe",
        "boosts": ["ATTACK"],
        "expected_accuracy_roll": 37788,
        "expected_max_hit": 45,  # scythe total: 45 + 22 + 11 = 78
    },
    {
        "name": "TTT_super_attack_only",
        "prayer": "piety",
        "gear_names": [
            "torva full helm",
            "torva platebody",
            "torva platelegs",
            "amulet of rancour",
            "ultor ring",
            "avernic treads",
            "ferocious gloves",
            "infernal cape",
            "avernic defender",
        ],
        "weapon": "scythe",
        "boosts": ["SUPER_ATTACK"],
        "expected_accuracy_roll": 39932,
        "expected_max_hit": 45,  # scythe total: 45 + 22 + 11 = 78
    },
    # ── Prayer variants ────────────────────────────────────────────────────
    {
        "name": "TTT_chivalry",
        "gear_names": [
            "torva full helm",
            "torva platebody",
            "torva platelegs",
            "amulet of rancour",
            "ultor ring",
            "avernic treads",
            "ferocious gloves",
            "infernal cape",
            "avernic defender",
        ],
        "weapon": "scythe",
        "prayer": "chivalry",
        "boosts": ["super combat"],
        "expected_accuracy_roll": 38324,
        "expected_max_hit": 51,  # scythe total: 51 + 25 + 12 = 88
    },
    {
        "name": "TTT_ultimate_strength",
        "gear_names": [
            "torva full helm",
            "torva platebody",
            "torva platelegs",
            "amulet of rancour",
            "ultor ring",
            "avernic treads",
            "ferocious gloves",
            "infernal cape",
            "avernic defender",
        ],
        "weapon": "scythe",
        "prayer": "ultimate strength",
        "boosts": ["super combat"],
        "expected_accuracy_roll": 33768,
        "expected_max_hit": 50,  # scythe total: 50 + 25 + 12 = 87
    },
    {
        "name": "TTT_incredible_reflexes",
        "gear_names": [
            "torva full helm",
            "torva platebody",
            "torva platelegs",
            "amulet of rancour",
            "ultor ring",
            "avernic treads",
            "ferocious gloves",
            "infernal cape",
            "avernic defender",
        ],
        "weapon": "scythe",
        "prayer": "INCREDIBLE_REFLEXES",
        "boosts": ["super combat"],
        "expected_accuracy_roll": 38324,
        "expected_max_hit": 44,  # scythe total: 44 + 22 + 11 = 77
    },
    {
        "name": "TTT_burst_of_strength",
        "gear_names": [
            "torva full helm",
            "torva platebody",
            "torva platelegs",
            "amulet of rancour",
            "ultor ring",
            "avernic treads",
            "ferocious gloves",
            "infernal cape",
            "avernic defender",
        ],
        "weapon": "scythe",
        "prayer": "BURST_OF_STRENGTH",
        "boosts": ["super combat"],
        "expected_accuracy_roll": 35108,
        "expected_max_hit": 45,  # scythe total: 45 + 22 + 11 = 78
    },
    {
        "name": "TTT_supernatural_strength",
        "gear_names": [
            "torva full helm",
            "torva platebody",
            "torva platelegs",
            "amulet of rancour",
            "ultor ring",
            "avernic treads",
            "ferocious gloves",
            "infernal cape",
            "avernic defender",
        ],
        "weapon": "scythe",
        "prayer": "SUPERNATURAL_STRENGTH",
        "boosts": ["super combat"],
        "expected_accuracy_roll": 33768,
        "expected_max_hit": 47,  # scythe total: 47 + 23 + 11 = 81
    },
    {
        "name": "TTT_clarity_of_thought",
        "gear_names": [
            "torva full helm",
            "torva platebody",
            "torva platelegs",
            "amulet of rancour",
            "ultor ring",
            "avernic treads",
            "ferocious gloves",
            "infernal cape",
            "avernic defender",
        ],
        "weapon": "scythe",
        "prayer": "CLARITY_OF_THOUGHT",
        "boosts": ["super combat"],
        "expected_accuracy_roll": 35108,
        "expected_max_hit": 44,  # scythe total: 44 + 22 + 11 = 77
    },
    {
        "name": "TTT_improved_reflexes",
        "gear_names": [
            "torva full helm",
            "torva platebody",
            "torva platelegs",
            "amulet of rancour",
            "ultor ring",
            "avernic treads",
            "ferocious gloves",
            "infernal cape",
            "avernic defender",
        ],
        "weapon": "scythe",
        "prayer": "IMPROVED_REFLEXES",
        "boosts": ["super combat"],
        "expected_accuracy_roll": 36716,
        "expected_max_hit": 44,  # scythe total: 44 + 22 + 11 = 77
    },
    # ── Prayer + potion combos ─────────────────────────────────────────────
    {
        "name": "TTT_chivalry_supercombat",
        "gear_names": [
            "torva full helm",
            "torva platebody",
            "torva platelegs",
            "amulet of rancour",
            "ultor ring",
            "avernic treads",
            "ferocious gloves",
            "infernal cape",
            "avernic defender",
        ],
        "weapon": "scythe",
        "prayer": "chivalry",
        "boosts": ["super combat"],
        "expected_accuracy_roll": 38324,
        "expected_max_hit": 51,  # scythe total: 51 + 25 + 12 = 88
    },
    {
        "name": "TTT_ultimate_strength_scb",
        "gear_names": [
            "torva full helm",
            "torva platebody",
            "torva platelegs",
            "amulet of rancour",
            "ultor ring",
            "avernic treads",
            "ferocious gloves",
            "infernal cape",
            "avernic defender",
        ],
        "weapon": "scythe",
        "prayer": "ultimate strength",
        "boosts": ["super combat"],
        "expected_accuracy_roll": 33768,
        "expected_max_hit": 50,  # scythe total: 50 + 25 + 12 = 87
    },
    {
        "name": "TTT_burst_strength_no_pot",
        "gear_names": [
            "torva full helm",
            "torva platebody",
            "torva platelegs",
            "amulet of rancour",
            "ultor ring",
            "avernic treads",
            "ferocious gloves",
            "infernal cape",
            "avernic defender",
        ],
        "weapon": "scythe",
        "prayer": "BURST_OF_STRENGTH",
        "boosts": ["none"],
        "expected_accuracy_roll": 29748,
        "expected_max_hit": 39,  # scythe total: 39 + 19 + 9 = 67
    },
    {
        "name": "TTT_incredible_reflexes_zammy",
        "gear_names": [
            "torva full helm",
            "torva platebody",
            "torva platelegs",
            "amulet of rancour",
            "ultor ring",
            "avernic treads",
            "ferocious gloves",
            "infernal cape",
            "avernic defender",
        ],
        "weapon": "scythe",
        "prayer": "INCREDIBLE_REFLEXES",
        "boosts": ["zamorak brew"],
        "expected_accuracy_roll": 36448,
        "expected_max_hit": 42,  # scythe total: 42 + 21 + 10 = 73
    },
    {
        "name": "TTT_no_piety_ancient_brew",
        "gear_names": [
            "torva full helm",
            "torva platebody",
            "torva platelegs",
            "amulet of rancour",
            "ultor ring",
            "avernic treads",
            "ferocious gloves",
            "infernal cape",
            "avernic defender",
        ],
        "weapon": "scythe",
        "prayer": "none",
        "boosts": ["ancient brew"],
        "expected_accuracy_roll": 25728,
        "expected_max_hit": 34,  # scythe total: 34 + 17 + 8 = 59
    },
    {
        "name": "TTT_chivalry_ancient_brew",
        "gear_names": [
            "torva full helm",
            "torva platebody",
            "torva platelegs",
            "amulet of rancour",
            "ultor ring",
            "avernic treads",
            "ferocious gloves",
            "infernal cape",
            "avernic defender",
        ],
        "weapon": "scythe",
        "prayer": "chivalry",
        "boosts": ["ancient brew"],
        "expected_accuracy_roll": 29212,
        "expected_max_hit": 39,  # scythe total: 39 + 19 + 9 = 67
    },
    # ── New gear + potion variants ─────────────────────────────────────────
    {
        "name": "only_torture_super_combat",
        "prayer": "piety",
        "gear_names": [
            "amulet of torture",
        ],
        "weapon": "scythe",
        "boosts": ["super combat"],
        "expected_accuracy_roll": 30396,
        "expected_max_hit": 36,  # scythe total: 36 + 18 + 9 = 63
    },
    {
        "name": "only_fury_ancient_brew",
        "prayer": "piety",
        "gear_names": [
            "amulet of fury",
        ],
        "weapon": "scythe",
        "boosts": ["ancient brew"],
        "expected_accuracy_roll": 22487,
        "expected_max_hit": 27,  # scythe total: 27 + 13 + 6 = 46
    },
    {
        "name": "only_strength_zamorak_brew",
        "prayer": "piety",
        "gear_names": [
            "amulet of strength",
        ],
        "weapon": "scythe",
        "boosts": ["zamorak brew"],
        "expected_accuracy_roll": 26838,
        "expected_max_hit": 34,  # scythe total: 34 + 17 + 8 = 59
    },
    {
        "name": "only_bring_zamorak_brew",
        "prayer": "piety",
        "gear_names": [
            "berserker ring (i)",
        ],
        "weapon": "scythe",
        "boosts": ["zamorak brew"],
        "expected_accuracy_roll": 26838,
        "expected_max_hit": 34,  # scythe total: 34 + 17 + 8 = 59
    },
    {
        "name": "only_prims_super_combat",
        "prayer": "piety",
        "gear_names": [
            "primordial boots",
        ],
        "weapon": "scythe",
        "boosts": ["super combat"],
        "expected_accuracy_roll": 28459,
        "expected_max_hit": 35,  # scythe total: 35 + 17 + 8 = 60
    },
    # ── New gear + prayer variants ─────────────────────────────────────────
    {
        "name": "only_torture_piety",
        "gear_names": [
            "amulet of torture",
        ],
        "weapon": "scythe",
        "prayer": "piety",
        "boosts": ["super combat"],
        "expected_accuracy_roll": 30396,
        "expected_max_hit": 36,  # scythe total: 36 + 18 + 9 = 63
    },
    {
        "name": "only_fury_chivalry",
        "gear_names": [
            "amulet of fury",
        ],
        "weapon": "scythe",
        "prayer": "chivalry",
        "boosts": ["super combat"],
        "expected_accuracy_roll": 28457,
        "expected_max_hit": 34,  # scythe total: 34 + 17 + 8 = 59
    },
    {
        "name": "only_strength_ultimate_strength",
        "gear_names": [
            "amulet of strength",
        ],
        "weapon": "scythe",
        "prayer": "ultimate strength",
        "boosts": ["super combat"],
        "expected_accuracy_roll": 23814,
        "expected_max_hit": 34,  # scythe total: 34 + 17 + 8 = 59
    },
    {
        "name": "only_bring_incredible_reflexes",
        "gear_names": [
            "berserker ring (i)",
        ],
        "weapon": "scythe",
        "prayer": "INCREDIBLE_REFLEXES",
        "boosts": ["super combat"],
        "expected_accuracy_roll": 27027,
        "expected_max_hit": 30,  # scythe total: 30 + 15 + 7 = 52
    },
    {
        "name": "only_prims_burst_of_strength",
        "gear_names": [
            "primordial boots",
        ],
        "weapon": "scythe",
        "prayer": "BURST_OF_STRENGTH",
        "boosts": ["super combat"],
        "expected_accuracy_roll": 25021,
        "expected_max_hit": 30,  # scythe total: 30 + 15 + 7 = 52
    },
    # ── New gear pairs + prayer/potion combos ──────────────────────────────
    {
        "name": "only_torture_bring_chivalry_scb",
        "gear_names": [
            "amulet of torture",
            "berserker ring (i)",
        ],
        "weapon": "scythe",
        "prayer": "chivalry",
        "boosts": ["super combat"],
        "expected_accuracy_roll": 29172,
        "expected_max_hit": 37,  # scythe total: 37 + 18 + 9 = 64
    },
    {
        "name": "only_fury_prims_super_combat",
        "prayer": "piety",
        "gear_names": [
            "amulet of fury",
            "primordial boots",
        ],
        "weapon": "scythe",
        "boosts": ["super combat"],
        "expected_accuracy_roll": 29949,
        "expected_max_hit": 37,  # scythe total: 37 + 18 + 9 = 64
    },
    {
        "name": "only_torture_prims_piety_scb",
        "gear_names": [
            "amulet of torture",
            "primordial boots",
        ],
        "weapon": "scythe",
        "prayer": "piety",
        "boosts": ["super combat"],
        "expected_accuracy_roll": 30694,
        "expected_max_hit": 38,  # scythe total: 38 + 19 + 9 = 66
    },
    {
        "name": "only_fury_bring_no_piety_zammy",
        "gear_names": [
            "amulet of fury",
            "berserker ring (i)",
        ],
        "weapon": "scythe",
        "prayer": "none",
        "boosts": ["zamorak brew"],
        "expected_accuracy_roll": 23880,
        "expected_max_hit": 30,  # scythe total: 30 + 15 + 7 = 52
    },
    {
        "name": "only_strength_bring_super_combat",
        "prayer": "piety",
        "gear_names": [
            "amulet of strength",
            "berserker ring (i)",
        ],
        "weapon": "scythe",
        "boosts": ["super combat"],
        "expected_accuracy_roll": 28161,
        "expected_max_hit": 38,  # scythe total: 38 + 19 + 9 = 66
    },
    # ── New + old gear + prayer/potion combos ──────────────────────────────
    {
        "name": "only_torture_ferocious_chivalry_scb",
        "gear_names": [
            "amulet of torture",
            "ferocious gloves",
        ],
        "weapon": "scythe",
        "prayer": "chivalry",
        "boosts": ["super combat"],
        "expected_accuracy_roll": 31460,
        "expected_max_hit": 38,  # scythe total: 38 + 19 + 9 = 66
    },
    {
        "name": "only_fury_infernal_ultimate_strength_scb",
        "gear_names": [
            "amulet of fury",
            "infernal cape",
        ],
        "weapon": "scythe",
        "prayer": "ultimate strength",
        "boosts": ["super combat"],
        "expected_accuracy_roll": 25578,
        "expected_max_hit": 35,  # scythe total: 35 + 17 + 8 = 60
    },
    {
        "name": "only_bring_ferocious_piety_scb",
        "gear_names": [
            "berserker ring (i)",
            "ferocious gloves",
        ],
        "weapon": "scythe",
        "prayer": "piety",
        "boosts": ["super combat"],
        "expected_accuracy_roll": 30545,
        "expected_max_hit": 39,  # scythe total: 39 + 19 + 9 = 67
    },
    {
        "name": "only_prims_rancour_no_piety_zammy",
        "gear_names": [
            "primordial boots",
            "amulet of rancour",
        ],
        "weapon": "scythe",
        "prayer": "none",
        "boosts": ["zamorak brew"],
        "expected_accuracy_roll": 25920,
        "expected_max_hit": 30,  # scythe total: 30 + 15 + 7 = 52
    },
    {
        "name": "only_torture_infernal_burst_strength_scb",
        "gear_names": [
            "amulet of torture",
            "infernal cape",
        ],
        "weapon": "scythe",
        "prayer": "BURST_OF_STRENGTH",
        "boosts": ["super combat"],
        "expected_accuracy_roll": 27248,
        "expected_max_hit": 33,  # scythe total: 33 + 16 + 8 = 57
    },

    # ── Only Scythe + avernic treads ──────────────────────────────────
    {
        "name": "only_avernic_treads",
        "prayer": "piety",
        "boosts": ["super combat"],
        "gear_names": [
            "avernic treads",
        ],
        "weapon": "scythe",
        "expected_accuracy_roll": 28906,
        "expected_max_hit": 35,  # scythe total: 35 + 17 + 8 = 60
    },
    # ── Only Scythe + ferocious gloves ────────────────────────────────
    {
        "name": "only_ferocious_gloves",
        "prayer": "piety",
        "boosts": ["super combat"],
        "gear_names": [
            "ferocious gloves",
        ],
        "weapon": "scythe",
        "expected_accuracy_roll": 30545,
        "expected_max_hit": 37,  # scythe total: 37 + 18 + 9 = 64
    },
            # ── Void Melee setups ────────────────────────────────────────────
    {
        "name": "VVV_nothing_else",
        "prayer": "piety",
        "boosts": ["super combat"],
        "gear_names": ['void melee helm', 'elite void top', 'elite void robe', 'void knight gloves'],
        "weapon": "scythe",
        "expected_accuracy_roll": 30807,
        "expected_max_hit": 37,  # scythe total: 37 + 18 + 9 = 64
    },
    {
        "name": "VVV_cape_only",
        "prayer": "piety",
        "boosts": ["super combat"],
        "gear_names": ['void melee helm', 'elite void top', 'elite void robe', 'void knight gloves', 'infernal cape'],
        "weapon": "scythe",
        "expected_accuracy_roll": 31459,
        "expected_max_hit": 39,  # scythe total: 39 + 19 + 9 = 67
    },
    {
        "name": "VVV_neck_only",
        "prayer": "piety",
        "boosts": ["super combat"],
        "gear_names": ['void melee helm', 'elite void top', 'elite void robe', 'void knight gloves', 'amulet of rancour'],
        "weapon": "scythe",
        "expected_accuracy_roll": 34882,
        "expected_max_hit": 40,  # scythe total: 40 + 20 + 10 = 70
    },
    {
        "name": "VVV_ring_only",
        "prayer": "piety",
        "boosts": ["super combat"],
        "gear_names": ['void melee helm', 'elite void top', 'elite void robe', 'void knight gloves', 'ultor ring'],
        "weapon": "scythe",
        "expected_accuracy_roll": 30807,
        "expected_max_hit": 40,  # scythe total: 40 + 20 + 10 = 70
    },
    {
        "name": "VVV_boots_only",
        "prayer": "piety",
        "boosts": ["super combat"],
        "gear_names": ['void melee helm', 'elite void top', 'elite void robe', 'void knight gloves', 'avernic treads'],
        "weapon": "scythe",
        "expected_accuracy_roll": 31622,
        "expected_max_hit": 39,  # scythe total: 39 + 19 + 9 = 67
    },
    {
        "name": "VVV_nothing_no_scb",
        "prayer": "piety",
        "gear_names": ['void melee helm', 'elite void top', 'elite void robe', 'void knight gloves'],
        "weapon": "scythe",
        "boosts": ["none"],
        "expected_accuracy_roll": 26082,
        "expected_max_hit": 31,  # scythe total: 31 + 15 + 7 = 53
    },
    {
        "name": "VVV_nothing_no_piety",
        "gear_names": ['void melee helm', 'elite void top', 'elite void robe', 'void knight gloves'],
        "weapon": "scythe",
        "prayer": "none",
        "boosts": ["super combat"],
        "expected_accuracy_roll": 26082,
        "expected_max_hit": 31,  # scythe total: 31 + 15 + 7 = 53
    },
    {
        "name": "VVV_nothing_no_scb_no_piety",
        "gear_names": ['void melee helm', 'elite void top', 'elite void robe', 'void knight gloves'],
        "weapon": "scythe",
        "boosts": ["none"],
        "prayer": "none",
        "expected_accuracy_roll": 22113,
        "expected_max_hit": 26,  # scythe total: 26 + 13 + 6 = 45
    },
    {
        "name": "VVV_setup",
        "prayer": "piety",
        "boosts": ["super combat"],
        "gear_names": ['void melee helm', 'elite void top', 'elite void robe', 'void knight gloves', 'amulet of rancour', 'ultor ring', 'avernic treads', 'infernal cape'],
        "weapon": "scythe",
        "expected_accuracy_roll": 36349,
        "expected_max_hit": 47,  # scythe total: 47 + 23 + 11 = 81
    },
    {
        "name": "VVV_setup_chivalry",
        "gear_names": ['void melee helm', 'elite void top', 'elite void robe', 'void knight gloves', 'amulet of rancour', 'ultor ring', 'avernic treads', 'infernal cape'],
        "weapon": "scythe",
        "prayer": "chivalry",
        "boosts": ["super combat"],
        "expected_accuracy_roll": 35011,
        "expected_max_hit": 46,  # scythe total: 46 + 23 + 11 = 80
    },
    {
        "name": "VVV_setup_ult_str",
        "gear_names": ['void melee helm', 'elite void top', 'elite void robe', 'void knight gloves', 'amulet of rancour', 'ultor ring', 'avernic treads', 'infernal cape'],
        "weapon": "scythe",
        "prayer": "ultimate strength",
        "boosts": ["super combat"],
        "expected_accuracy_roll": 30774,
        "expected_max_hit": 44,  # scythe total: 44 + 22 + 11 = 77
    },
    {
        "name": "VVV_setup_super_str",
        "gear_names": ['void melee helm', 'elite void top', 'elite void robe', 'void knight gloves', 'amulet of rancour', 'ultor ring', 'avernic treads', 'infernal cape'],
        "weapon": "scythe",
        "prayer": "SUPERNATURAL_STRENGTH",
        "boosts": ["super combat"],
        "expected_accuracy_roll": 30774,
        "expected_max_hit": 43,  # scythe total: 43 + 21 + 10 = 74
    },
    {
        "name": "VVV_setup_burst_str",
        "gear_names": ['void melee helm', 'elite void top', 'elite void robe', 'void knight gloves', 'amulet of rancour', 'ultor ring', 'avernic treads', 'infernal cape'],
        "weapon": "scythe",
        "prayer": "BURST_OF_STRENGTH",
        "boosts": ["super combat"],
        "expected_accuracy_roll": 32112,
        "expected_max_hit": 41,  # scythe total: 41 + 20 + 10 = 71
    },
    {
        "name": "VVV_setup_no_piety",
        "gear_names": ['void melee helm', 'elite void top', 'elite void robe', 'void knight gloves', 'amulet of rancour', 'ultor ring', 'avernic treads', 'infernal cape'],
        "weapon": "scythe",
        "prayer": "none",
        "boosts": ["super combat"],
        "expected_accuracy_roll": 30774,
        "expected_max_hit": 39,  # scythe total: 39 + 19 + 9 = 67
    },
    {
        "name": "VVV_setup_no_scb",
        "prayer": "piety",
        "gear_names": ['void melee helm', 'elite void top', 'elite void robe', 'void knight gloves', 'amulet of rancour', 'ultor ring', 'avernic treads', 'infernal cape'],
        "weapon": "scythe",
        "boosts": ["none"],
        "expected_accuracy_roll": 30774,
        "expected_max_hit": 40,  # scythe total: 40 + 20 + 10 = 70
    },
    {
        "name": "VVV_setup_no_scb_no_piety",
        "gear_names": ['void melee helm', 'elite void top', 'elite void robe', 'void knight gloves', 'amulet of rancour', 'ultor ring', 'avernic treads', 'infernal cape'],
        "weapon": "scythe",
        "boosts": ["none"],
        "prayer": "none",
        "expected_accuracy_roll": 26091,
        "expected_max_hit": 33,  # scythe total: 33 + 16 + 8 = 57
    },
    {
        "name": "VVV_setup_zammy",
        "prayer": "piety",
        "gear_names": ['void melee helm', 'elite void top', 'elite void robe', 'void knight gloves', 'amulet of rancour', 'ultor ring', 'avernic treads', 'infernal cape'],
        "weapon": "scythe",
        "boosts": ["zamorak brew"],
        "expected_accuracy_roll": 34788,
        "expected_max_hit": 45,  # scythe total: 45 + 22 + 11 = 78
    },
    {
        "name": "VVV_torture",
        "prayer": "piety",
        "boosts": ["super combat"],
        "gear_names": ['void melee helm', 'infernal cape', 'amulet of torture', 'elite void top', 'elite void robe', 'void knight gloves', 'avernic treads', 'ultor ring'],
        "weapon": "scythe",
        "expected_accuracy_roll": 34719,
        "expected_max_hit": 47,  # scythe total: 47 + 23 + 11 = 81
    },
    {
        "name": "VVV_fury",
        "prayer": "piety",
        "boosts": ["super combat"],
        "gear_names": ['void melee helm', 'infernal cape', 'amulet of fury', 'elite void top', 'elite void robe', 'void knight gloves', 'avernic treads', 'ultor ring'],
        "weapon": "scythe",
        "expected_accuracy_roll": 33904,
        "expected_max_hit": 46,  # scythe total: 46 + 23 + 11 = 80
    },
    {
        "name": "VVV_strength_ammy",
        "prayer": "piety",
        "boosts": ["super combat"],
        "gear_names": ['void melee helm', 'infernal cape', 'amulet of strength', 'elite void top', 'elite void robe', 'void knight gloves', 'avernic treads', 'ultor ring'],
        "weapon": "scythe",
        "expected_accuracy_roll": 32274,
        "expected_max_hit": 47,  # scythe total: 47 + 23 + 11 = 81
    },
    {
        "name": "VVV_bring",
        "prayer": "piety",
        "boosts": ["super combat"],
        "gear_names": ['void melee helm', 'infernal cape', 'amulet of rancour', 'elite void top', 'elite void robe', 'void knight gloves', 'avernic treads', 'berserker ring (i)'],
        "weapon": "scythe",
        "expected_accuracy_roll": 36349,
        "expected_max_hit": 46,  # scythe total: 46 + 23 + 11 = 80
    },
    {
        "name": "VVV_prims",
        "prayer": "piety",
        "boosts": ["super combat"],
        "gear_names": ['void melee helm', 'infernal cape', 'amulet of rancour', 'elite void top', 'elite void robe', 'void knight gloves', 'primordial boots', 'ultor ring'],
        "weapon": "scythe",
        "expected_accuracy_roll": 35860,
        "expected_max_hit": 47,  # scythe total: 47 + 23 + 11 = 81
    },
    {
        "name": "VVV_fire_cape",
        "prayer": "piety",
        "boosts": ["super combat"],
        "gear_names": ['void melee helm', 'fire cape', 'amulet of rancour', 'elite void top', 'elite void robe', 'void knight gloves', 'avernic treads', 'ultor ring'],
        "weapon": "scythe",
        "expected_accuracy_roll": 35860,
        "expected_max_hit": 46,  # scythe total: 46 + 23 + 11 = 80
    },
    {
        "name": "VVV_ferocious",
        "prayer": "piety",
        "boosts": ["super combat"],
        "gear_names": ['void melee helm', 'infernal cape', 'amulet of rancour', 'elite void top', 'elite void robe', 'ferocious gloves', 'avernic treads', 'ultor ring'],
        "weapon": "scythe",
        "expected_accuracy_roll": 35611,
        "expected_max_hit": 47,  # scythe total: 47 + 23 + 11 = 81
    },
    {
        "name": "VVV_torture_fire",
        "prayer": "piety",
        "boosts": ["super combat"],
        "gear_names": ['void melee helm', 'fire cape', 'amulet of torture', 'elite void top', 'elite void robe', 'void knight gloves', 'avernic treads', 'ultor ring'],
        "weapon": "scythe",
        "expected_accuracy_roll": 34230,
        "expected_max_hit": 46,  # scythe total: 46 + 23 + 11 = 80
    },
    {
        "name": "VVV_torture_prims",
        "prayer": "piety",
        "boosts": ["super combat"],
        "gear_names": ['void melee helm', 'infernal cape', 'amulet of torture', 'elite void top', 'elite void robe', 'void knight gloves', 'primordial boots', 'ultor ring'],
        "weapon": "scythe",
        "expected_accuracy_roll": 34230,
        "expected_max_hit": 46,  # scythe total: 46 + 23 + 11 = 80
    },
    {
        "name": "VVV_torture_prims_fire",
        "prayer": "piety",
        "boosts": ["super combat"],
        "gear_names": ['void melee helm', 'fire cape', 'amulet of torture', 'elite void top', 'elite void robe', 'void knight gloves', 'primordial boots', 'ultor ring'],
        "weapon": "scythe",
        "expected_accuracy_roll": 33741,
        "expected_max_hit": 45,  # scythe total: 45 + 22 + 11 = 78
    },
    {
        "name": "VVV_fury_fire",
        "prayer": "piety",
        "boosts": ["super combat"],
        "gear_names": ['void melee helm', 'fire cape', 'amulet of fury', 'elite void top', 'elite void robe', 'void knight gloves', 'avernic treads', 'ultor ring'],
        "weapon": "scythe",
        "expected_accuracy_roll": 33415,
        "expected_max_hit": 45,  # scythe total: 45 + 22 + 11 = 78
    },
    {
        "name": "VVV_fury_prims",
        "prayer": "piety",
        "boosts": ["super combat"],
        "gear_names": ['void melee helm', 'infernal cape', 'amulet of fury', 'elite void top', 'elite void robe', 'void knight gloves', 'primordial boots', 'ultor ring'],
        "weapon": "scythe",
        "expected_accuracy_roll": 33415,
        "expected_max_hit": 46,  # scythe total: 46 + 23 + 11 = 80
    },
    {
        "name": "VVV_bring_fire",
        "prayer": "piety",
        "boosts": ["super combat"],
        "gear_names": ['void melee helm', 'fire cape', 'amulet of rancour', 'elite void top', 'elite void robe', 'void knight gloves', 'avernic treads', 'berserker ring (i)'],
        "weapon": "scythe",
        "expected_accuracy_roll": 35860,
        "expected_max_hit": 45,  # scythe total: 45 + 22 + 11 = 78
    },
    {
        "name": "VVV_bring_prims",
        "prayer": "piety",
        "boosts": ["super combat"],
        "gear_names": ['void melee helm', 'infernal cape', 'amulet of rancour', 'elite void top', 'elite void robe', 'void knight gloves', 'primordial boots', 'berserker ring (i)'],
        "weapon": "scythe",
        "expected_accuracy_roll": 35860,
        "expected_max_hit": 46,  # scythe total: 46 + 23 + 11 = 80
    },
    {
        "name": "VVV_torture_ferocious",
        "prayer": "piety",
        "boosts": ["super combat"],
        "gear_names": ['void melee helm', 'infernal cape', 'amulet of torture', 'elite void top', 'elite void robe', 'ferocious gloves', 'avernic treads', 'ultor ring'],
        "weapon": "scythe",
        "expected_accuracy_roll": 34121,
        "expected_max_hit": 46,  # scythe total: 46 + 23 + 11 = 80
    },
    {
        "name": "VVV_torture_ferocious_fire",
        "prayer": "piety",
        "boosts": ["super combat"],
        "gear_names": ['void melee helm', 'fire cape', 'amulet of torture', 'elite void top', 'elite void robe', 'ferocious gloves', 'avernic treads', 'ultor ring'],
        "weapon": "scythe",
        "expected_accuracy_roll": 33674,
        "expected_max_hit": 45,  # scythe total: 45 + 22 + 11 = 78
    },
    {
        "name": "VVV_torture_chivalry",
        "gear_names": ['void melee helm', 'infernal cape', 'amulet of torture', 'elite void top', 'elite void robe', 'void knight gloves', 'avernic treads', 'ultor ring'],
        "weapon": "scythe",
        "prayer": "chivalry",
        "boosts": ["super combat"],
        "expected_accuracy_roll": 33441,
        "expected_max_hit": 45,  # scythe total: 45 + 22 + 11 = 78
    },
    {
        "name": "VVV_torture_ult_str",
        "gear_names": ['void melee helm', 'infernal cape', 'amulet of torture', 'elite void top', 'elite void robe', 'void knight gloves', 'avernic treads', 'ultor ring'],
        "weapon": "scythe",
        "prayer": "ultimate strength",
        "boosts": ["super combat"],
        "expected_accuracy_roll": 29394,
        "expected_max_hit": 44,  # scythe total: 44 + 22 + 11 = 77
    },
]

def _make_test_classes():
    """Create one TestCase subclass per setup so VS Code groups accuracy/max hit."""

    for setup in SETUPS:
        setup_name = setup["name"]
        class_name = f"{setup_name}"

        def build_accuracy_test(setup=setup):
            def test(self):
                player = _build_player_from_setup(setup)
                player.calc_all_the_things(combat_style="Melee", attack_type="Slash")
                self.assertEqual(
                    player.attack_roll, setup["expected_accuracy_roll"],
                    f"\n setup={setup['name']!r}"
                    f"\n gear={setup.get('gear_names', [])}"
                    f"\n expected_accuracy_roll={setup['expected_accuracy_roll']}"
                    f"\n actual_accuracy_roll={player.attack_roll}"
                )
            return test

        def build_max_hit_test(setup=setup):
            def test(self):
                player = _build_player_from_setup(setup)
                player.calc_all_the_things(combat_style="Melee", attack_type="Slash")
                self.assertEqual(
                    player.max_hit, setup["expected_max_hit"],
                    f"\n setup={setup['name']!r}"
                    f"\n gear={setup.get('gear_names', [])}"
                    f"\n expected_max_hit={setup['expected_max_hit']}"
                    f"\n actual_max_hit={player.max_hit}"
                )
            return test

        TestCls = type(class_name, (unittest.TestCase,), {
            "test_accuracy_roll": build_accuracy_test(setup),
            "test_max_hit":      build_max_hit_test(setup),
        })
        globals()[class_name] = TestCls


def _build_player_from_setup(setup):
    player = Loadout(gear_names=setup["gear_names"]).build()

    weapon = WeaponRegistry.get(setup["weapon"])
    player.equip_weapon(weapon)

    if "attack_style_override" in setup:
        player.weapon.attack_style = setup["attack_style_override"]

    if "prayer" in setup:
        player.prayer = PrayerRegistry.get(setup["prayer"])

    if "boosts" in setup:
        player.boosts = [PotionRegistry.get(b) for b in setup["boosts"]]

    return player


_make_test_classes()


if __name__ == "__main__":
    unittest.main()
