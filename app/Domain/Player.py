import json
import math
from beartype import beartype
from typing import Optional

from app.Domain.Monster import Monster
from app.Domain.Stats import Stats
from app.Domain.Weapon import Weapon
from app.Data.Definitions.Weapons.Fists import Fists
from app.Domain.Enums.GearSlot import GearSlot
from app.Domain.GearItem import Gear
from app.Data.Definitions.Gear import VoidRangerHelm, VoidMageHelm, VoidMeleeHelm
from app.Data.Definitions.Gear import EliteVoidTop, EliteVoidRobe, VoidKnightGloves
from app.Data.Definitions.Gear import Salve as SalveGear
from app.Data.Registries.GearRegistry import GearRegistry
from app.Domain.Exceptions.InvalidLoadoutException import InvalidLoadoutException
from app.Domain.Exceptions.InvalidAmmunitionException import InvalidAmmunitionException

from app.Domain.Enums import Potion, Prayer  # compat namespace (value lookups)
from app.Domain.Potion import Potion as PotionType
from app.Domain.Prayer import Prayer as PrayerType

class Player:

    def is_dead(self):
        return self.current_hp == 0
    def is_alive(self):
        return self.current_hp > 0
    
    @beartype
    def reduce_hp(self, amount:int):
        self.current_hp = self.current_hp - amount
        self.current_hp = self.current_hp if self.current_hp >= 0 else 0
        return self.current_hp
    
    @beartype
    def do_attack(self, monster:Monster, special_attack=False, always_hit: bool = False):
        if self.weapon is None:
            self.equip_weapon(Fists())
        self._validate_ammo()
        if special_attack and self.current_special_attack < self.weapon.special_attack_cost:
            print("We tried to use a special attack but did not have enough energy, so we did a normal attack")
            print(f"{self.weapon.name} requires {self.weapon.special_attack_cost} but we only had {self.current_special_attack}")

        self.calc_all_the_things(self.weapon.combat_style, self.weapon.attack_type, monster.is_weak_to_salve)
        monster.calc_def_roll(attack_type=self.weapon.attack_type, combat_style=self.weapon.combat_style)

        if special_attack and self.current_special_attack >= self.weapon.special_attack_cost:
            self.current_special_attack -= self.weapon.special_attack_cost
            return self.weapon.do_special_attack(
                max_hit=self.max_hit, 
                player_attack_roll=self.attack_roll, 
                npc_def_roll=monster.def_roll,
                monster=monster,
                always_hit=always_hit,
            )
        else:
            return self.weapon.do_attack(
                max_hit=self.max_hit, 
                player_attack_roll=self.attack_roll, 
                npc_def_roll=monster.def_roll,
                monster=monster,
                always_hit=always_hit,
            )


    @beartype
    def equip_weapon(self, weapon:Weapon):
        if self.weapon is not None:
            self.unequip_weapon(self.weapon)
        self.weapon = weapon
        self.compute_gear_stats()

    @beartype
    def unequip_weapon(self, weapon:Weapon):
        self.weapon = Fists()
        self.compute_gear_stats()


    def _validate_ammo(self):
        """Validate that equipped ammo matches the weapon's ammo_type.

        If a bow is equipped and darts are in the ammo slot, or vice versa,
        raise InvalidAmmunitionException.
        """
        if self.weapon is None or self.weapon.ammo_type is None:
            return

        ammo_gear = self.gear.get(GearSlot.AMMO)
        if ammo_gear is None:
            return

        ammo_category = getattr(ammo_gear, "ammo_category", None)
        if ammo_category is not None and ammo_category != self.weapon.ammo_type:
            raise InvalidAmmunitionException(
                f"Incompatible ammunition: '{ammo_gear.name}' ({ammo_category}) "
                f"cannot be used with '{self.weapon.name}' "
                f"which requires {self.weapon.ammo_type.value}."
            )

    # --- Gear system ---

    @beartype
    def equip_gear(self, gear: Gear):
        """Equip a piece of gear into the appropriate slot and recompute stats."""

        existing = self.gear.get(gear.slot)
        if existing is not None and existing.name != gear.name:
            raise InvalidLoadoutException(
                f"Slot conflict: '{gear.name}' and '{existing.name}' "
                f"both occupy the {gear.slot.name.lower()} slot."
            )

        self.gear[gear.slot] = gear

        self._detect_void_set()
        self._detect_salve()
        self.compute_gear_stats()

    @beartype
    def unequip_gear(self, slot: GearSlot):
        """Unequip whatever gear occupies *slot* and recompute stats."""
        old = self.gear.pop(slot, None)
        if old is None:
            return

        self._detect_void_set()
        self._detect_salve()
        self.compute_gear_stats()

    def compute_gear_stats(self):
        """Recompute self.stats from base_stats + all equipped gear + weapon."""
        self.stats = self.base_stats.copy()

        for gear in self.gear.values():
            gear_stats = gear.build()
            temp = Stats(gear_stats)
            self.stats.increase(temp)

        if self.weapon is not None:
            self.stats.increase(extra_stats=self.weapon.stats)

    def _detect_void_set(self):
        """Check the equipped gear for a complete void set and set flags."""
        _VOID_HELMS = {
            VoidRangerHelm.name: "ranged",
            VoidMageHelm.name:   "mage",
            VoidMeleeHelm.name:  "melee",
        }

        helm = self.gear.get(GearSlot.HEAD)
        body = self.gear.get(GearSlot.BODY)
        legs = self.gear.get(GearSlot.LEGS)
        hands = self.gear.get(GearSlot.HANDS)

        if (
            helm is not None and helm.name in _VOID_HELMS
            and body is not None and body.name == EliteVoidTop.name
            and legs is not None and legs.name == EliteVoidRobe.name
            and hands is not None and hands.name == VoidKnightGloves.name
        ):
            self.wearing_void = True
            self.void_style = _VOID_HELMS[helm.name]
        else:
            self.wearing_void = False
            self.void_style = None

    def _detect_salve(self):
        """Check the equipped gear for a salve amulet and set wearing_salve flag."""
        neck = self.gear.get(GearSlot.NECK)
        self.wearing_salve = neck is not None and neck.name == SalveGear.name


    #region Roll Calculation
    @beartype
    def calc_all_the_things(self, combat_style:str=None, attack_type:str=None, monster_weak_to_salve:Optional[bool]=False):
        self.compute_gear_stats()
        self._detect_void_set()
        self._detect_salve()

        if combat_style is not None and combat_style.capitalize() == "Ranged":
            self.effective_ranged_att_level = self.calc_eff_ranged_attack_level()
            self.effective_ranged_str_level = self.calc_eff_ranged_strength_level()
            self.max_hit = self.calc_ranged_max_hit(monster_weak_to_salve)
            self.attack_roll = self.calc_ranged_att_roll(monster_weak_to_salve)
        elif combat_style is not None and combat_style.capitalize() == "Mage":
            self.effective_magic_level = self.calc_eff_magic_level()
            self.max_hit = self.calc_magic_max_hit()
            self.attack_roll = self.calc_magic_att_roll()
        else:
            self.effective_att_level = self.calc_eff_attack_level()
            self.effective_str_level = self.calc_eff_strength_level()
            self.effective_def_level = self.calc_eff_defence_level()
            self.max_hit = self.calc_max_hit(monster_weak_to_salve)
            self.attack_roll = self.calc_att_roll(attack_type, monster_weak_to_salve)
            self.def_roll = self.calc_def_roll(attack_type)
    def calc_eff_attack_level(self):
        eff_att_level = self.stats.attack_level
        for potion in self.boosts:
            eff_att_level += Potion.compute_boost(self.stats.attack_level, potion.attack_percentage, potion.attack_flat)
        if(self.prayer.atk_mult > 0):
            eff_att_level *= self.prayer.atk_mult
            eff_att_level = math.floor(eff_att_level)
            
        if(self.weapon.attack_style == "Accurate"): eff_att_level += 3
        if(self.weapon.attack_style == "Controlled"): eff_att_level += 1
        
        eff_att_level += 8
        if(self.wearing_void and self.void_style == "melee"):
            eff_att_level = math.floor(eff_att_level * 1.10)
        return eff_att_level
    def calc_eff_strength_level(self):
        eff_str_level = self.stats.strength_level
        
        for potion in self.boosts:
            eff_str_level += Potion.compute_boost(self.stats.strength_level, potion.strength_percentage, potion.strength_flat)
        if(self.prayer.str_mult > 0):
            eff_str_level *= self.prayer.str_mult
            eff_str_level = math.floor(eff_str_level)
            
        if(self.weapon.attack_style == "Aggressive"): eff_str_level += 3
        if(self.weapon.attack_style == "Controlled"): eff_str_level += 1
        
        eff_str_level += 8
        if(self.wearing_void and self.void_style == "melee"):
            eff_str_level = math.floor(eff_str_level * 1.10)
        return eff_str_level
    def calc_eff_defence_level(self):
        eff_def_lvl = self.stats.def_level
        
        for potion in self.boosts:
            eff_def_lvl += Potion.compute_boost(self.stats.def_level, potion.defence_percentage, potion.defence_flat)
        if(self.prayer.def_mult > 0):
            eff_def_lvl *= self.prayer.def_mult
            eff_def_lvl = math.floor(eff_def_lvl)
            
        if(self.weapon.attack_style == "Defensive"): eff_def_lvl += 3
        if(self.weapon.attack_style == "Controlled"): eff_def_lvl += 1
        
        eff_def_lvl += 8
        return eff_def_lvl

    def calc_eff_ranged_attack_level(self):
        eff_ranged_atk = self.stats.ranged_level

        for potion in self.boosts:
            eff_ranged_atk += Potion.compute_boost(self.stats.ranged_level, potion.ranged_percentage, potion.ranged_flat)
        if(self.prayer.ranged_attack_multiplier > 0):
            eff_ranged_atk *= self.prayer.ranged_attack_multiplier
            eff_ranged_atk = math.floor(eff_ranged_atk)

        if(self.weapon.attack_style == "Accurate"): eff_ranged_atk += 3

        eff_ranged_atk += 8
        if(self.wearing_void and self.void_style == "ranged"):
            eff_ranged_atk = math.floor(eff_ranged_atk * 1.10)
        return eff_ranged_atk

    def calc_eff_ranged_strength_level(self):
        eff_ranged_str = self.stats.ranged_level

        for potion in self.boosts:
            eff_ranged_str += Potion.compute_boost(self.stats.ranged_level, potion.ranged_percentage, potion.ranged_flat)
        if(self.prayer.ranged_strength_multiplier > 0):
            eff_ranged_str *= self.prayer.ranged_strength_multiplier
            eff_ranged_str = math.floor(eff_ranged_str)

        if(self.weapon.attack_style == "Accurate"): eff_ranged_str += 3

        eff_ranged_str += 8
        return eff_ranged_str

    def calc_eff_magic_level(self):
        eff_magic = self.stats.magic_level

        for potion in self.boosts:
            eff_magic += Potion.compute_boost(self.stats.magic_level, potion.magic_percentage, potion.magic_flat)
        if(self.prayer.magic_attack_multiplier > 0):
            eff_magic *= self.prayer.magic_attack_multiplier
            eff_magic = math.floor(eff_magic)

        if(self.weapon.attack_style == "Accurate"): eff_magic += 3
        if(self.weapon.attack_style == "Long-Range"): eff_magic += 1

        eff_magic += 9
        return eff_magic

    def calc_ranged_att_roll(self, monster_weak_to_salve: bool = False):
        attack_roll = self.effective_ranged_att_level * (self.stats.ranged_attack_bonus + 64)
        if(self.wearing_salve and monster_weak_to_salve):
            attack_roll *= 1.20
        if(self.wearing_void and self.void_style == "ranged"):
            attack_roll *= 1.10
        return math.floor(attack_roll)

    def calc_ranged_max_hit(self, monster_weak_to_salve: bool = False):
        max_hit = self.effective_ranged_str_level * (self.stats.ranged_strength_bonus + 64)
        max_hit += 320
        max_hit /= 640
        max_hit = math.floor(max_hit)
        if(self.wearing_salve and monster_weak_to_salve):
            max_hit *= 1.2
        if(self.wearing_void and self.void_style == "ranged"):
            max_hit *= 1.125
        return math.floor(max_hit)

    def calc_magic_att_roll(self):
        attack_roll = self.effective_magic_level * (self.stats.magic_attack_bonus + 64)
        if(self.wearing_void and self.void_style == "mage"):
            attack_roll *= 1.45
        return math.floor(attack_roll)

    def calc_magic_max_hit(self):
        base = math.floor(self.effective_magic_level / 3) + 1
        magic_damage_pct = self.stats.magic_strength_bonus / 100.0
        base = math.floor(base * (1.0 + magic_damage_pct))
        if self.prayer.magic_damage_bonus > 0:
            base = math.floor(base * (1.0 + self.prayer.magic_damage_bonus))
        if(self.wearing_void and self.void_style == "mage"):
            base = math.floor(base * 1.025)
        return base

    @beartype
    def calc_att_roll(self, attack_style:str=None, monster_weak_to_salve:bool=False):
        if attack_style is None:
            raise ValueError("Attack style must be set to calc attack roll")
        attack_bonus = 0
        if attack_style.capitalize() == "Slash": attack_bonus = self.stats.slash_attack_bonus
        if attack_style.capitalize() == "Crush": attack_bonus = self.stats.crush_attack_bonus
        if attack_style.capitalize() == "Stab": attack_bonus = self.stats.stab_attack_bonus
        attack_roll = self.effective_att_level * (attack_bonus + 64)
        if(self.wearing_salve and monster_weak_to_salve):
            attack_roll *= 1.20
        return math.floor(attack_roll)
    @beartype
    def calc_def_roll(self, attack_style:str=None):
        if attack_style is None:
            raise ValueError("Attack style must be set to calc attack roll")
        
        def_bonus = 0
        if attack_style.capitalize() == "Slash": def_bonus = self.stats.slash_def
        if attack_style.capitalize() == "Crush": def_bonus = self.stats.crush_def
        if attack_style.capitalize() == "Stab": def_bonus = self.stats.stab_def

        def_roll = self.effective_def_level * (def_bonus + 64)
        return def_roll

    @beartype
    def calc_max_hit(self, monster_weak_to_salve:bool=False):
        max_hit = self.effective_str_level * (self.stats.melee_strength_bonus + 64)
        max_hit += 320
        max_hit /= 640
        max_hit = math.floor(max_hit)
        if(self.wearing_salve and monster_weak_to_salve): 
            max_hit *= 1.2
        return math.floor(max_hit)
    
    #endregion


    @beartype
    def __init__(self, 
        stats:          dict    = None,
        weapon:         Weapon  = None,
        loadout:        Optional[object] = None,
        boosts:         list    = [Potion.NONE],
        prayer:         PrayerType      = Prayer.NONE,
        wearing_salve:  bool    = False,
        wearing_void:   bool    = False,
        void_style:     Optional[str]     = None,
        ):
        if stats is None:
            raise ValueError("Stats cannot be null")

        self.base_stats = Stats(stats)
        self.stats = self.base_stats.copy()

        self.current_hp = self.stats.hp_level
        self.current_prayer = self.stats.prayer_level
        self.current_special_attack = 100
        self.current_run = 100

        self.wearing_salve = wearing_salve
        self.wearing_void = wearing_void
        self.void_style = void_style
        self.boosts = boosts
        self.prayer = prayer
        self.weapon = weapon

        self.gear: dict = {}

        if self.weapon is None:
            self.equip_weapon(Fists())
        else:
            self.weapon=weapon

        # Equip loadout gear if provided
        if loadout is not None:
            if loadout.gear_names is not None:
                for gear_name in loadout.gear_names:
                    gear = GearRegistry.get(gear_name)
                    if gear is None:
                        raise KeyError(f"Unknown gear: {gear_name}")
                    self.equip_gear(gear)