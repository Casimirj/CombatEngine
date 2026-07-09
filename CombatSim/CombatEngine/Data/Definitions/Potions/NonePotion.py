from CombatSim.CombatEngine.Domain.Potion import Potion
from CombatSim.CombatEngine.Data.Registries.PotionRegistry import PotionRegistry

NONE = Potion(
    name="None",
    label="None",
    aliases=["none", "no potion"],
)
PotionRegistry.register(NONE)
