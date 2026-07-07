from combat_engine.Domain.Potion import Potion
from combat_engine.Data.Registries.PotionRegistry import PotionRegistry

ZAMORAK_BREW = Potion(
    name="Zamorak brew",
    label="Zamorak brew",
    attack_percentage=0.12,
    attack_flat=2,
    strength_percentage=0.12,
    strength_flat=2,
    defence_percentage=-0.10,
    defence_flat=-2,
    aliases=["zamorak brew", "zammy brew"],
)
PotionRegistry.register(ZAMORAK_BREW)
