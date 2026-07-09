from CombatSim.CombatEngine.Domain.Potion import Potion
from CombatSim.CombatEngine.Data.Registries.PotionRegistry import PotionRegistry

ATTACK = Potion(
    name="Attack potion",
    label="Attack potion",
    attack_percentage=0.10,
    attack_flat=3,
    aliases=["attack", "attack pot"],
)
PotionRegistry.register(ATTACK)
