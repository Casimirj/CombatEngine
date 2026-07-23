"""Backward-compatibility re-export of NyloRoom.

NyloRoomState was previously a standalone dataclass.  It has been replaced by
the ``NyloRoom`` subclass of ``Room``.  This module exists so existing imports
don't break; new code should import ``NyloRoom`` directly.
"""

from CombatSim.Simulations.nyloboss.NyloRoom import NyloRoom as NyloRoomState  # noqa: F401
