from app.Domain.Potion import Potion
from app.Data.Registries.PotionRegistry import PotionRegistry

BLACK_WARLOCK = Potion(
    name="Black warlock",
    label="Black warlock",
    strength_percentage=0.15,
    strength_flat=4,
    aliases=["black warlock"],
)
PotionRegistry.register(BLACK_WARLOCK)
