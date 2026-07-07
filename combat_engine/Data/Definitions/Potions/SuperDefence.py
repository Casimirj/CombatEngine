from combat_engine.Domain.Potion import Potion
from combat_engine.Data.Registries.PotionRegistry import PotionRegistry

SUPER_DEFENCE = Potion(
    name="Super defence",
    label="Super defence",
    defence_percentage=0.15,
    defence_flat=5,
    aliases=["super defence", "superdef"],
)
PotionRegistry.register(SUPER_DEFENCE)
