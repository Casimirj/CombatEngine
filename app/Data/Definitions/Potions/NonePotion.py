from app.Domain.Potion import Potion
from app.Data.Registries.PotionRegistry import PotionRegistry

NONE = Potion(
    name="None",
    label="None",
    aliases=["none", "no potion"],
)
PotionRegistry.register(NONE)
