from app.GameDefinitions.Potion import Potion
from app.Registries.PotionRegistry import PotionRegistry

RANGING = Potion(
    name="Ranging potion",
    label="Ranging potion",
    ranged_percentage=0.10, ranged_flat=4,
    aliases=["ranging", "range pot", "ranging pot"],
)
PotionRegistry.register(RANGING)
