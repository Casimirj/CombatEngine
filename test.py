import NPC
import Stats



bloat = npc = NPC(Stats({
    'hp_level': 100,
    'def_level': 50,
    'stab_def': 30  # Overrides default 20
}))


print(bloat.stats.get_stats())