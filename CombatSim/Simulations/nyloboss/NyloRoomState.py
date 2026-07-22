from dataclasses import dataclass

from CombatSim.Simulations.nyloboss.phases import NyloBossPhase


@dataclass
class NyloRoomState:
    """Snapshot of the boss room state at a phase transition."""
    phase: NyloBossPhase
    first_melee: bool
    first_ranged: bool
    prev_phase: "NyloBossPhase | None"
    boss_defense: int = 0
