# Combat Engine

A FastAPI-based damage calculator and combat simulator for Old School RuneScape. Provides hit damage, accuracy calculations, and simulated fight tests.

## Getting Started

### Prerequisites

- Python 3.12+
- `requirements.txt` dependencies: `fastapi`, `uvicorn`, `beartype`

### Installation

```bash
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
```

### Running the Server

```bash
python run_damage_api.py
```

Defaults to port **8001**. Override with `DAMAGE_API_PORT`:

```bash
DAMAGE_API_PORT=8080 python run_damage_api.py
```

In non-production mode (`IsProd=false` in `.env`), Swagger docs are available at
[`http://127.0.0.1:8001/docs`](http://127.0.0.1:8001/docs).

---

## API Reference

All endpoints accept and return JSON. Field names use **PascalCase** (as shown in
the OpenAPI examples).

---

### `GET /test`

Health-check — returns `"hello world"`.

---

### `POST /calculate_hit`

Roll a single hit against a monster and return the resulting damage.

**Example request**

```json
{
  "Loadout": "OathTorvaRancour",
  "Weapon": "Scythe of Vitur",
  "Monster": {
    "Name": "Maiden",
    "ReduceDefense": true,
    "Defense": 80
  },
  "Scale": 3
}
```

**Response**

```json
{
  "damage": 42,
  "monster_defense": 80
}
```

**Fields**

| Field | Type | Required | Description |
|---|---|---|---|
| `Loadout` | `string` | yes | Named loadout, or `"Custom"` (then `Gear` is required) |
| `Weapon` | `string` | yes | Registered weapon name |
| `Monster.Name` | `string` | yes | Registered monster name |
| `Monster.ReduceDefense` | `bool` | yes | Whether to override monster defence level |
| `Monster.Defense` | `int` | only when `ReduceDefense` is `true` | Custom defence level |
| `Scale` | `int` | yes | Raid party scale (≥1) |
| `Gear.Pieces` | `string[]` | only when `Loadout` is `"Custom"` | List of gear piece names |
| `PlayerLevels` | `dict` | no | Override player combat levels |
| `AlwaysHit` | `bool` | no | Force the hit to always land (default `false`) |

---

### `POST /get_combat_calcs`

Produce a full breakdown of the player's combat stats, effective levels, max
hit, attack/defence rolls, and hit chance.

**Example request** (same shape as `/calculate_hit`, without `AlwaysHit`)

```json
{
  "Loadout": "OathTorvaRancour",
  "Weapon": "Scythe of Vitur",
  "Monster": {
    "Name": "Maiden",
    "ReduceDefense": true,
    "Defense": 80
  },
  "Scale": 3
}
```

**Response** (key fields)

```json
{
  "player": {
    "stats": { "attack_level": 99, "strength_level": 99 },
    "gear": { "weapon_name": "Scythe of Vitur" },
    "setup": { "prayer": "Piety", "boosts": ["Super combat"] }
  },
  "effective_attack_level": 118,
  "effective_strength_level": 118,
  "max_hit": 52,
  "player_attack_roll": 48000,
  "npc_defence_roll": 24000,
  "hit_chance": 0.75
}
```

---

### `POST /run_test`

Simulate a fight to the death — keep swinging until the monster dies and
report how many hits it took.

**Example request**

```json
{
  "Loadout": "OathTorvaRancour",
  "Weapon": "Scythe of Vitur",
  "Monster": {
    "Name": "Bloat",
    "ReduceDefense": false
  },
  "Scale": 5
}
```

**Response**

```json
{
  "message": "Killed Bloat in 14 swings",
  "monster_alive": false,
  "hits_to_kill": 14,
  "final_damage": -3
}
```

---

## Reference Data

### Named Loadouts

| Name | Gear pieces |
|---|---|
| `OathTorvaRancour` | Oathplate helm, Infernal cape, Amulet of rancour, Torva platebody, Torva platelegs, Ferocious gloves, Primordial boots, Berserker ring (i), Avernic defender |
| `OathTorvaSalve` | Oathplate helm, Infernal cape, Salve (e), Torva platebody, Torva platelegs, Ferocious gloves, Primordial boots, Berserker ring (i), Avernic defender |
| `OathFireRancour` | Oathplate helm, Fire cape, Amulet of rancour, Oathplate body, Oathplate legs, Ferocious gloves, Primordial boots, Berserker ring (i), Avernic defender |
| `OathFireSalve` | Oathplate helm, Fire cape, Salve (e), Oathplate body, Oathplate legs, Ferocious gloves, Primordial boots, Berserker ring (i), Avernic defender |
| `VoidRangedQuiverAnguish` | Void ranger helm, Dizana's quiver, Necklace of anguish, Elite void top, Elite void robe, Void knight gloves, Avernic treads |

Use `"Custom"` as the loadout name and supply a `Gear.Pieces` list to build
your own.

---

### Weapons

Scythe of Vitur, Twisted bow, Tumeken's shadow, Toxic blowpipe, Eye of Ayak,
Noxious halberd, Fists, Dragon claws, Bgs, Accursed sceptre, Crystal halberd,
Elder maul, Nightmare staff, Sulfur blades, DDS w/ avernic

---

### Monsters

Maiden, Bloat, Baba, P1Verzik, P2Verzik, P3Verzik, Sotetseg, Xarpus

---

### Gear Pieces (for Custom loadouts)

**Head** — Torva full helm, Oathplate helm, Ancestral hat, Masori mask,
Void mage helm, Void melee helm, Void ranger helm

**Cape** — Infernal cape, Fire cape, Imbued saradomin cape, Dizana's quiver

**Neck** — Amulet of rancour, Amulet of torture, Amulet of fury, Amulet of
strength, Necklace of anguish, Occult necklace, Salve (e)

**Body** — Torva platebody, Oathplate body, Bandos chestplate, Ancestral robe
top, Masori body, Elite void top

**Legs** — Torva platelegs, Oathplate legs, Bandos tassets, Ancestral robe
bottom, Masori chaps, Elite void robe

**Hands** — Ferocious gloves, Zaryte vambraces, Confliction gauntlets,
Void knight gloves

**Boots** — Primordial boots, Dragon boots, Avernic treads

**Ring** — Ultor ring, Berserker ring (i), Magus ring, Venator ring

**Offhand** — Avernic defender

**Ammo** — Dragon arrows, Amethyst arrows, Rune arrows, Adamant arrows,
Dragon darts, Amethyst darts, Rune darts, Adamant darts

---

## Combat Calculations

All damage, accuracy, and max-hit formulas are documented in
**[combat_calculations.md](combat_calculations.md)**.

---

## Project Structure

```text
.
├── run_damage_api.py              # FastAPI server entry point
├── requirements.txt               # Python dependencies
├── .env                           # IsProd flag
├── combat_calculations.md         # Formula reference
│
├── app/
│   ├── Api/
│   │   ├── Environment.py         # Config reader
│   │   └── Damage/
│   │       ├── Controller.py      # Route definitions
│   │       ├── Models/            # Pydantic request / response schemas
│   │       │   ├── calculate_hit/
│   │       │   ├── get_combat_calcs/
│   │       │   └── test/
│   │       └── Services/          # Business logic per endpoint
│   │
│   ├── Domain/                    # Core domain objects
│   │   ├── Player.py
│   │   ├── Weapon.py
│   │   ├── Monster.py
│   │   ├── Stats.py
│   │   ├── GearItem.py
│   │   ├── Loadout.py
│   │   ├── Potion.py
│   │   └── Prayer.py
│   │
│   ├── Data/
│   │   ├── Registries/            # Central lookups (monsters, weapons, gear, etc.)
│   │   └── Definitions/           # Concrete data modules
│   │       ├── Gear/              # Gear pieces grouped by slot
│   │       ├── Loadouts/          # Named loadout presets
│   │       ├── Monsters/          # Boss / NPC definitions
│   │       ├── Potions/           # Potion/boost definitions
│   │       ├── Prayers/           # Prayer definitions
│   │       └── Weapons/           # Weapon definitions
│   │
│   ├── Enums/                     # Shared enumerations
│   ├── Exceptions/                # Custom exception types
│   └── Factories/                 # Construction helpers (e.g. PlayerFactory)
│
└── tests/
    ├── unit/                      # Unit tests (domain, registries, enums, etc.)
    └── combat_calcs/              # Test suite for combat formula accuracy
```

**Pattern**

- **Domain** objects (`Player`, `Weapon`, `Monster`, `Stats`) hold all
  combat-state logic.
- **Registries** provide a single lookup point for every named entity.
- **Definitions** are declarative data modules that self-register at import
  time so the registries stay in sync.
- **API Services** wire the HTTP layer to the domain layer — they resolve
  names, build players, and delegate to domain methods.
