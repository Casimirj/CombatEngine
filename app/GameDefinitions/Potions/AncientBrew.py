from app.GameDefinitions.Potion import Potion
from app.Registries.PotionRegistry import PotionRegistry

ANCIENT_BREW = Potion(
    name="Ancient brew",
    label="Ancient brew",
    attack_percentage=-0.10, attack_flat=-2,
    strength_percentage=-0.10, strength_flat=-2,
    defence_percentage=-0.10, defence_flat=-2,
    magic_percentage=0.05, magic_flat=2,
    aliases=["ancient brew"],
)
PotionRegistry.register(ANCIENT_BREW)
