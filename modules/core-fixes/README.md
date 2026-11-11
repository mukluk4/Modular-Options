# Bug fixes

Fixes for bugs in the server code. None of them change how the game is meant to play.

| Fix | Bases | What went wrong |
|---|---|---|
| Zone objects with no map floor | both | An object (forge, ground spawn) placed where the map has no floor was moved to the invalid-z value and vanished. It now keeps its stored z. |
| Fallback heal message | both | "You have been healed for N points" tested the Heal Over Time filter with `!= SelfOnly \|\| != Hide`, which is always true, so the filter never hid it; and it called `CastToClient()` on any mob, so an NPC healed with no caster could crash the zone. Now only players get it, and only Hide hides it. |
| Suppressed buff wearing off | NMS | A suppressed buff (`SPELL_SUPPRESSED`) has no spell data; reading `spells[]` with it when the suppression ended crashed the zone. |
| Target's target procs | NMS | Implied targeting moved a beneficial target's-target proc (a remote heal) onto the mob's target first, so it landed on that player's target instead. |
| Zone-state loot | NMS | With `Custom:DoItemUpgrades`, loot restored from a saved zone state lost its loot table link, so personal loot rules treated it as quest-added. |
| Server buffs on zone boot | NMS | A zone booting with stale rules could wipe the NMS permanent server buffs for everyone. On boot they are now only ever added; removing them is left to a rules reload. |
| Feign death while moving | NMS | A multiclass player whose client class can't feign isn't stood up by their client when they move, so the server kept them feigned while they ran around. Moving now breaks feign death, as it breaks hide. |
| Server buff rule | NMS | `Custom:PermanentServerBuffsEnabled` was stored as `True`; rule booleans are case-sensitive, so zones read it as off. The SQL stores `true`. |
| Sleeper's Tomb warder flag | NMS | Instance IDs are reused, so a new instance could inherit an old one's warder flag and Kerafyrm's adds dropped no loot. The flag now stores the instance's end time and only counts when it matches. |

## Rules and commands

None. The server buff rule fix is `nms/sql`; the warder fix patches `sleeper/encounters/sleeper_custom.lua` in the quests
folder (`--quests`).

## Credits

Written for Voidforged.
