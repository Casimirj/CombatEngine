"""Gear package."""

from app.GearItem import Gear                   # noqa: F401
from app.Registries.GearRegistry import GearRegistry  # noqa: F401

# Import gear modules so they self‑register
from . import Salve               # noqa: F401
from . import TorvaFullHelm       # noqa: F401
from . import TorvaPlatebody      # noqa: F401
from . import TorvaPlatelegs      # noqa: F401
from . import OathplateHelm       # noqa: F401
from . import OathplateBody       # noqa: F401
from . import OathplateLegs       # noqa: F401
from . import AncestralHat        # noqa: F401
from . import AncestralRobeTop    # noqa: F401
from . import AncestralRobeBottom # noqa: F401
from . import MasoriMask          # noqa: F401
from . import MasoriBody          # noqa: F401
from . import MasoriChaps         # noqa: F401
from . import AmuletOfRancour     # noqa: F401
from . import NecklaceOfAnguish   # noqa: F401
from . import OccultNecklace      # noqa: F401
from . import FerociousGloves     # noqa: F401
from . import ZaryteVambraces     # noqa: F401
from . import UltorRing           # noqa: F401
from . import MagusRing           # noqa: F401
from . import VenatorRing         # noqa: F401
from . import AvernicTreads       # noqa: F401
from . import BandosChestplate    # noqa: F401
from . import BandosTassets       # noqa: F401
from . import AvernicDefender     # noqa: F401
from . import FireCape            # noqa: F401
from . import InfernalCape        # noqa: F401
from . import DizanasQuiver       # noqa: F401
from . import ImbuedSaradominCape # noqa: F401
from . import EliteVoidTop        # noqa: F401
from . import EliteVoidRobe       # noqa: F401
from . import VoidKnightGloves    # noqa: F401
from . import VoidRangerHelm      # noqa: F401
from . import VoidMageHelm        # noqa: F401
from . import VoidMeleeHelm       # noqa: F401
from . import AmuletOfTorture     # noqa: F401
from . import BerserkerRingI      # noqa: F401
from . import PrimordialBoots     # noqa: F401
from . import AmuletOfFury        # noqa: F401
from . import AmuletOfStrength    # noqa: F401


__all__ = [
    "Gear",
    "GearRegistry",
    "Salve",
    "TorvaFullHelm",
    "TorvaPlatebody",
    "TorvaPlatelegs",
    "OathplateHelm",
    "OathplateBody",
    "OathplateLegs",
    "AncestralHat",
    "AncestralRobeTop",
    "AncestralRobeBottom",
    "MasoriMask",
    "MasoriBody",
    "MasoriChaps",
    "AmuletOfRancour",
    "NecklaceOfAnguish",
    "OccultNecklace",
    "FerociousGloves",
    "ZaryteVambraces",
    "UltorRing",
    "MagusRing",
    "VenatorRing",
    "AvernicTreads",
    "BandosChestplate",
    "BandosTassets",
    "AvernicDefender",
    "FireCape",
    "InfernalCape",
    "DizanasQuiver",
    "ImbuedSaradominCape",
    "EliteVoidTop",
    "EliteVoidRobe",
    "VoidKnightGloves",
    "VoidRangerHelm",
    "VoidMageHelm",
    "VoidMeleeHelm",
    "AmuletOfTorture",
    "BerserkerRingI",
    "PrimordialBoots",
    "AmuletOfFury",
    "AmuletOfStrength",
]
