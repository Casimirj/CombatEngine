from CombatSim.CombatEngine.Domain.Potion import Potion
from CombatSim.CombatEngine.Data.Registries.PotionRegistry import PotionRegistry

IMBUED_HEART = Potion(
    name="Imbued heart",
    label="Imbued heart",
    magic_percentage=0.10,
    magic_flat=1,
    aliases=["imbued heart", "heart"],
)
PotionRegistry.register(IMBUED_HEART)
