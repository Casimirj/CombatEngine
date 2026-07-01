from app.GameDefinitions.Potion import Potion
from app.Registries.PotionRegistry import PotionRegistry

SUPER_COMBAT = Potion(
    name="Super combat",
    label="Super combat",
    attack_percentage=0.15, attack_flat=5,
    strength_percentage=0.15, strength_flat=5,
    defence_percentage=0.15, defence_flat=5,
    aliases=["super combat", "scp", "supercombat"],
)
PotionRegistry.register(SUPER_COMBAT)
