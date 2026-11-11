# Raid Portal

A Raid Portal NPC in The Void sends a raid into a private instance (zone version 50) to fight one existing boss,
picked at random from the raid tier's pool and rescaled for the raid tier and raid size. There is no trash: the
instance holds only the boss. Each raid member in the instance earns Chronal Prisms, a new raid-only currency, when it
dies.

**Still in testing.** The portal answers GMs only (`thevoida/1200071.lua`, `event_say`). A GM can type
`test <boss> <size>` to skip the raid requirements. Remove the `GetGM()` line to open it to players.

## Access

- The player must lead a raid of 6 to 72 members. Size and membership lock when the instance opens.
- Raid tier N needs the leader's deepest Greater Rift clear to be at least N x 100. Only the leader needs it.
- An instance lasts 2 hours. After a wipe the boss resets and the raid can try again until it runs out.
- No lockouts; the Prism prices are the throttle.

| Raid tier | Leader's deepest clear | Boss pool | Prisms per player |
|---|---|---|---:|
| 1 | 100 | Classic and Kunark | 2 |
| 2 | 200 | Velious | 4 |
| 3 | 300 | Luclin | 8 |
| 4 | 400 | Planes of Power | 16 |
| 5 | 500 | Plane of Time and Gates of Discord | 32 |

## Scaling

Boss stats are set from the solo Rift Guardian at rift tier N x 100, then raised by raid size: +100% hit points and
+5% damage (up to +50%) per member past the first. Bosses with their own fight have a raid version of it under
`<zone>/v50/` (the Ancient Cragbeast Matriarch's is `txevu/encounters/acm_portal.lua`, with its timer names fixed);
the rest get one of the Rift Guardian's mechanics at random: AoE pulses, adds at 50%, or hate wipes.
`Raid_Controller.lua` spawns the instance's boss and puts it back after a wipe. Boss tables and tuning are in
`lua_modules/raid_portal.lua`.

When the boss dies, every member gets the character data bucket `raid_cleared` raised to that tier (members who
weren't in the zone get it on their next zone-in). The `tier-gear` module's Prism Augmenter uses it to unlock its raid
augments; without that module nothing reads it.

## Client strings

Append `client/dbstr_raid.txt` to the client's `dbstr_us.txt`. It names the Chronal Prism currency (types 17 and 18,
id 3); without it the currency shows no name.

## Database

Run in order (`modules.py sql` does):

1. `2026_11_02_01_raid_portal_test.sql`: version 50 rows for the first three zones, the controller (npc 1200070,
   copied from the Rift Controller) and portal (npc 1200071, copied from the Rift Portal), spawn group 5003895, and the
   Chronal Prism (item 800005, alternate currency 3).
2. `2026_11_02_02_raid_portal_spawn.sql`: the portal's spawn in The Void. Run `#zoneshutdown zone thevoida` first:
   with zone state saving on, a running zone restores its saved NPCs and ignores new spawn rows.
3. `2026_11_03_01_raid_portal_shared_bosses.sql` and `2026_11_08_01_raid_portal_own_bosses.sql`: the rest of the
   roster's zones.

The SQL adds rows only and is not rerunnable. Zone rows load at boot, so restart the server afterwards.

## Bases

NMS only for now. The Lua and SQL would need a port for stock EQEmu's zone table and boss scripts. Requires
`greater-rifts` (the controller and portal NPCs are copies of its NPCs, and the deepest-clear check is its).

## Credits

Written for Voidforged.
