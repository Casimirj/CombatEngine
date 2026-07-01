from app.GameDefinitions.Potion import Potion
from app.Registries.PotionRegistry import PotionRegistry

STRENGTH = Potion(
    name="Strength potion",
    label="Strength potion",
    strength_percentage=0.10, strength_flat=3,
    aliases=["strength", "str pot", "strength pot"],
)
PotionRegistry.register(STRENGTH)
