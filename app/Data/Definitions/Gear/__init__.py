"""Gear package — all gear is registered by import-time side effects.

Subdirectories are organized by GearSlot for discoverability,
but all items share the ``app.Data.Definitions.Gear`` namespace.
"""

from app.Domain.GearItem import Gear                   # noqa: F401
from app.Data.Registries.GearRegistry import GearRegistry  # noqa: F401

from .Head   import *  # noqa: F401, F403
from .Neck   import *  # noqa: F401, F403
from .Cape   import *  # noqa: F401, F403
from .Body   import *  # noqa: F401, F403
from .Legs   import *  # noqa: F401, F403
from .Hands  import *  # noqa: F401, F403
from .Boot   import *  # noqa: F401, F403
from .Ring   import *  # noqa: F401, F403
from .Offhand import *  # noqa: F401, F403
from .Ammo   import *  # noqa: F401, F403
