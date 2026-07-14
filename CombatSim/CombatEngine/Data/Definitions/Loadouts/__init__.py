"""Loadout package."""

from CombatSim.CombatEngine.Domain.Loadout import Loadout
from CombatSim.CombatEngine.Data.Registries.LoadoutRegistry import LoadoutRegistry  # noqa: F401

# Import loadout modules so they self‑register
from . import OathTorvaRancour       # noqa: F401
from . import OathTorvaSalve         # noqa: F401
from . import OathFireRancour        # noqa: F401
from . import OathFireSalve          # noqa: F401
from . import VoidRangedQuiverAnguish  # noqa: F401
from . import VoidMage               # noqa: F401


__all__ = [
    "Loadout",
    "LoadoutRegistry",
    "OathTorvaRancour",
    "OathTorvaSalve",
    "OathFireRancour",
    "OathFireSalve",
    "VoidRangedQuiverAnguish",
    "VoidMage",
]
