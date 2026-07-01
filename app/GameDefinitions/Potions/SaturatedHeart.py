from app.GameDefinitions.Potion import Potion
from app.Registries.PotionRegistry import PotionRegistry

SATURATED_HEART = Potion(
    name="Saturated heart",
    label="Saturated heart",
    magic_percentage=0.10, magic_flat=4,
    aliases=["saturated heart", "sat heart"],
)
PotionRegistry.register(SATURATED_HEART)
