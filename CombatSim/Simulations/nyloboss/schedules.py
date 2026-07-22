# Backwards-compatible re-exports (setup objects now live in NyloBossAttackSchedule)
from CombatSim.Simulations.nyloboss.NyloBossAttackSchedule import (
    MELEE_SETUP as melee_setup,
    RANGED_TBOW_SETUP as ranged_setup,
    RANGED_BLOWPIPE_SETUP as ranged_after_mage_setup,
    MAGE_SETUP as mage_setup,
    NyloBossAttackSchedule,
    NyloRole,
)
from CombatSim.Simulations.nyloboss.NyloRoomState import NyloRoomState
