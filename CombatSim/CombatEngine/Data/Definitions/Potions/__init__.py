"""Potion game definitions — imported to register all potions with PotionRegistry."""

# We use local imports so the registry is populated in a known order.
from .NonePotion import NONE      # noqa: F401
from .Attack import ATTACK        # noqa: F401
from .Strength import STRENGTH    # noqa: F401
from .SuperAttack import SUPER_ATTACK        # noqa: F401
from .SuperStrength import SUPER_STRENGTH    # noqa: F401
from .SuperDefence import SUPER_DEFENCE      # noqa: F401
from .SuperCombat import SUPER_COMBAT        # noqa: F401
from .ZamorakBrew import ZAMORAK_BREW       # noqa: F401
from .BlackWarlock import BLACK_WARLOCK     # noqa: F401
from .Ranging import RANGING               # noqa: F401
from .Bastion import BASTION               # noqa: F401
from .Magic import MAGIC                   # noqa: F401
from .Battlemage import BATTLEMAGE          # noqa: F401
from .ImbuedHeart import IMBUED_HEART      # noqa: F401
from .SaturatedHeart import SATURATED_HEART # noqa: F401
from .AncientBrew import ANCIENT_BREW      # noqa: F401
