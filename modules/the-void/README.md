# The Void hub

Opens The Void (`thevoida`, zone 459) to players. Stock PEQ keeps it GM-only. `greater-rifts` uses it as the hub
where rifts are opened and where players return.

- **Open zone:** `min_status` 255 to 0.
- **Soulbinder:** Soulbinder_Ilsara (npc 1200060), a copy of PoK's Soulbinder_Jera, by Zebuxoruk. Her script uses the
  stock `plugin::soulbinder_say`.

## NMS only

- **Map:** The Void on the Bazaar map (NMS Waypoints), under the Special tab.
- **Access gate** (`global/global_player.pl`): an account needs Plane of Time access (the account bucket
  `pop.flags.maelin` = 1, set by defeating the four elemental gods) to stay in The Void. Anyone else is sent to the
  Bazaar. GMs always get in. Flagged characters get The Void unlocked on the map when they zone.

The gate's settings are at the top of `global_player.pl`: `$VOID_ACCESS_BUCKET` (set it to `''` for no gate) and
`@VOID_KICK_TO` (where others are sent).

## Applying

New spawns don't show in a zone that has saved state: with The Void down, delete its `zone_state_spawns` rows after
the SQL. The soulbinder SQL clears its own rows first, so it can be run again.

## Rules and commands

None.

## Credits

Written for Voidforged.
