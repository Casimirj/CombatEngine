from combat_engine.Domain.Potion import Potion
from combat_engine.Data.Registries.PotionRegistry import PotionRegistry

NONE = Potion(
    name="None",
    label="None",
    aliases=["none", "no potion"],
)
PotionRegistry.register(NONE)
