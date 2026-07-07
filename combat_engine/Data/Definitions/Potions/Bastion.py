from combat_engine.Domain.Potion import Potion
from combat_engine.Data.Registries.PotionRegistry import PotionRegistry

BASTION = Potion(
    name="Bastion potion",
    label="Bastion potion",
    defence_percentage=0.15,
    defence_flat=5,
    ranged_percentage=0.10,
    ranged_flat=4,
    aliases=["bastion", "bastion pot"],
)
PotionRegistry.register(BASTION)
