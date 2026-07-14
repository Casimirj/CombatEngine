from enum import Enum


class NyloBossPhase(Enum):
    MELEE = 1
    RANGED = 2
    MAGE = 3


_PHASE_OPTIONS = [NyloBossPhase.MELEE, NyloBossPhase.RANGED, NyloBossPhase.MAGE]


def next_nylo_phase(current: NyloBossPhase) -> NyloBossPhase:
    """Pick the next NyloBoss phase, never repeating the current one."""
    import random
    candidates = [p for p in _PHASE_OPTIONS if p != current]
    return random.choice(candidates)
