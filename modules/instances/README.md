# Instance times

Changes to the NMS instance system (`NMS_instance_utils.pl`):

| Setting | NMS | With this module |
|---|---|---|
| Non-respawning instance lockout | 14 hours | 6 hours |
| Respawning instance lockout | 30 minutes | 5 minutes |
| Plane of Time replay lockout (`potimea/player.lua`) | 14 hours | 6 hours |
| NPC scaling per member past the second | on | off |

The scaling switch is `$SCALE_INSTANCE_NPCS` at the top of `NMS_instance_utils.pl`: set it to 1 to scale instance NPCs by
member count again. With it off, the "instances will become more difficult" notice is gone from the instance offer.

To use other lockout times, edit `$non_respawning_duration` and `$respawning_duration` in the same file.

## Rules, commands and database

None. Needs the plugins and quests folders (`--plugins`, `--quests`).

## Bases

NMS only: stock EQEmu has no NMS instance system.

## Credits

Written for Voidforged.
