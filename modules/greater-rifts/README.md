# Greater Rifts

Timed, randomized instances in classic dungeons. A player hails Zebuxoruk in The Void, picks a tier, and is sent into
a random rift zone (26 to choose from) with 15 minutes to fill the progress bar and kill the Rift Guardian.

- **Tiers 1 to 500.** A character can open any tier up to one past its deepest clear. Each tier scales the NPCs'
  hit points, damage, armor class and resists, and their spell and melee penetration (`rift_config.lua`).
- **Progress:** trash is worth 1%, elites 4%. Pylons appear at 25%, 50% and 75% (fire nuke, group heal and cure,
  absorb shield, or speed).
- **Champions:** 15% of trash gets affixes (molten pulses, arcane bolts, a vortex pull).
- **Guardian:** spawns at 100%, enrages after two minutes, and wipes hate every third pulse.
- **Clear reward:** Chronal Shards (alternate currency 2: 5 + 2 per tier, +25% under 10 minutes) and 1,000 platinum
  per tier, to every player in the rift.
- **Milestones:** a new deepest clear at a multiple of 25 is announced to the whole server.
- **Crash recovery:** progress is saved in a data bucket, so a zone crash doesn't reset the rift.
- The deepest clear is kept in the character bucket `rift_deepest`, which tier gear vendors check (`tier-gear`).

## Files

| Where | What |
|---|---|
| `quests/lua_modules/rift_config.lua` | Every setting: hub, time limit, tier cap, progress, rewards, NPC ids, pylons, champion and Guardian spells. HP and damage multipliers for servers whose characters are weaker than NMS's three-class ones. |
| `quests/lua_modules/rift_core.lua`, `champion_affixes.lua` | The rift logic |
| `quests/lua_modules/rift_zones.lua` | The rift zone pool and each zone's entry point (per base) |
| `quests/lua_modules/rift_appearances.lua` | Per zone, the looks of the creatures that normally live there, so rift trash looks like it belongs (per base, generated) |
| `quests/global/Rift_*.lua` | The controller, Guardian, pylons, trash and exit portal |
| `quests/thevoida/459000.lua` | Zebuxoruk: the story, the tier menu, re-enter and close |

The server loads `lua_modules` from its runtime folder: copy the quests folder's `lua_modules` there if your setup
keeps them apart.

## Database

- Rift NPCs 1200000-1200023, spawn groups 5003834-5003835, the Chronal Shard (item 800002, alternate currency 2), and
  Zebuxoruk (459000) as the keeper, moved to where players return.
- Each rift zone gets an instance version (1, or the next free version) copied from the normal zone: a rift spawn at
  every spawn point, the controller at the entry, doors unlocked, zone points and ground spawns, and a zone row with
  no flag, level or status requirement.

The zone SQL reads each zone's own spawns, so it fits whatever content your database has. To add a zone, put it in
`tools/gen_rift_zones.py`, run it against your database, apply the SQL and deploy the new `rift_zones.lua`.
`tools/gen_rift_appearances.py` rebuilds the appearance list. Both read the database settings from
`eqemu_config.json`.

## Client

The client only draws models loaded for the current zone. The pylon, the exit portal and the Rift Guardian's looks
need their models loaded in every zone: add the lines in `tools/GlobalLoad_rift.txt` to the client's
`Resources/GlobalLoad.txt` (before the `4,0` lines) and to your patcher. Without them those NPCs show as default
models. Rift trash only uses looks from its own zone, so it needs nothing.

## Bases

Stock EQEmu and NMS. NMS's `global_player.pl` refuses zones from expansions the account hasn't reached; the NMS patch
lets players into rift instances anyway, since the rift is the gate. Stock PEQ has no such check.

## Credits

Written for Voidforged; the stock EQEmu files come from the Singlevoid port.
