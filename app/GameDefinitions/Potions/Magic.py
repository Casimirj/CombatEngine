from app.GameDefinitions.Potion import Potion
from app.Registries.PotionRegistry import PotionRegistry

MAGIC = Potion(
    name="Magic potion",
    label="Magic potion",
    magic_percentage=0.04, magic_flat=4,
    aliases=["magic", "mage pot", "magic pot"],
)
PotionRegistry.register(MAGIC)
