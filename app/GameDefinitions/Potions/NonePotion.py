from app.GameDefinitions.Potion import Potion
from app.Registries.PotionRegistry import PotionRegistry

NONE = Potion(
    name="None",
    label="None",
    aliases=["none", "no potion"],
)
PotionRegistry.register(NONE)
