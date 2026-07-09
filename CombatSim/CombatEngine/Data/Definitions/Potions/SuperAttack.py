from CombatSim.CombatEngine.Domain.Potion import Potion
from CombatSim.CombatEngine.Data.Registries.PotionRegistry import PotionRegistry

SUPER_ATTACK = Potion(
    name="Super attack",
    label="Super attack",
    attack_percentage=0.15,
    attack_flat=5,
    aliases=["super attack", "superatt"],
)
PotionRegistry.register(SUPER_ATTACK)
