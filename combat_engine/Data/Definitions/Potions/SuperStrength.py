from combat_engine.Domain.Potion import Potion
from combat_engine.Data.Registries.PotionRegistry import PotionRegistry

SUPER_STRENGTH = Potion(
    name="Super strength",
    label="Super strength",
    strength_percentage=0.15,
    strength_flat=5,
    aliases=["super strength", "superstr"],
)
PotionRegistry.register(SUPER_STRENGTH)
