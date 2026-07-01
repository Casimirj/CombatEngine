from app.GameDefinitions.Potion import Potion
from app.Registries.PotionRegistry import PotionRegistry

BATTLEMAGE = Potion(
    name="Battlemage potion",
    label="Battlemage potion",
    defence_percentage=0.15, defence_flat=5,
    magic_percentage=0.04, magic_flat=4,
    aliases=["battlemage", "battlemage pot"],
)
PotionRegistry.register(BATTLEMAGE)
