"""Default NyloBoss player configurations."""

from CombatSim.Simulations.nyloboss.NyloBossAttackSchedule import NyloBossAttackSchedule
from CombatSim.Simulations.nyloboss.NyloRole import NyloRole
from CombatSim.Simulations.nyloboss.simulation import PlayerConfig

P1 = PlayerConfig(
    name="P1",
    attack_schedule=NyloBossAttackSchedule(role=NyloRole.BGS),
)
P2 = PlayerConfig(
    name="P2",
    attack_schedule=NyloBossAttackSchedule(role=NyloRole.BACKUP_BGS),
)
P3 = PlayerConfig(
    name="P3",
    attack_schedule=NyloBossAttackSchedule(role=NyloRole.CLAWS),
)

DEFAULT_PLAYER_CONFIGS = [P1, P2, P3]
