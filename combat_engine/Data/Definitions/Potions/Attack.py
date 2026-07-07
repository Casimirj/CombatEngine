from combat_engine.Domain.Potion import Potion
from combat_engine.Data.Registries.PotionRegistry import PotionRegistry

ATTACK = Potion(
    name="Attack potion",
    label="Attack potion",
    attack_percentage=0.10,
    attack_flat=3,
    aliases=["attack", "attack pot"],
)
PotionRegistry.register(ATTACK)
