from CombatSim.CombatEngine.Domain.Potion import Potion
from CombatSim.CombatEngine.Data.Registries.PotionRegistry import PotionRegistry

MAGIC = Potion(
    name="Magic potion",
    label="Magic potion",
    magic_percentage=0.04,
    magic_flat=4,
    aliases=["magic", "mage pot", "magic pot"],
)
PotionRegistry.register(MAGIC)
