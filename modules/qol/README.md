# Quality of life

Small changes that save players time.

## What it does

- **Attack while casting.** Melee auto-attack, auto-fire, ranged and throwing attacks keep going while a spell is
  being cast, so hybrids don't lose their swings.
- **Automatic training.** On level-up and at login, skills (not tradeskills) are raised to their caps for the
  character's level. Specializations stop where a guildmaster would stop training them. Spells and disciplines can be
  scribed and learned the same way. On NMS, multiclass characters get the highest cap among their classes.
- **#zone for players.** Players can use `#zone`, `#mystats` and `#find zone` (`#fz`, `#findzone`). `#zone` checks
  for the key that the zone's locked entrance door asks for (Sleeper's Tomb, Vex Thal and the like), and players
  always land at the safe spot: coordinates are for Guides and up. A top-level alias of a sub command (`#fz`) now uses
  that sub command's access, not the parent command's.
- **Faster rest regen.** Resting (sitting or mounted, out of combat) refills health, mana and endurance in 60 seconds
  instead of 180, and in 15 seconds in the hub zones: the Bazaar, the Plane of Knowledge and the Guild Lobby (and
  Voidforged's `thevoida`, if you have it). Zones with their own regen times keep them.
- **Kill faction switch.** `Custom:KillFactionHits` off stops kills from changing faction; quest faction still works.

On NMS also:

- **Held group buffs.** A group member's held buff (NMS's group buff suspension) is now recognized when the caster is
  someone else in the group, not only the player. Held invisibility no longer starts fading, which used to leave it
  stuck at 3 ticks.
- **Bazaar and Back** (spell 5824) lands you at one arrival spot facing the market, not at one of ten random points.
- **Unused AA points.** `AA:UnusedAAPointCap` defaults to -1 (no cap), as on stock EQEmu, instead of NMS's 100.
- `#set skill_all_max` (and the quest `MaxSkills()`) works again: NMS's version worked out the caps and never set
  them.

## Rules

| Rule | Default | What it does |
|---|---|---|
| `Custom:AllowAttackWhileCasting` | true | Attacks continue while casting. |
| `Custom:AutoTrainSkills` | true | Skills trained to their caps on level-up and login. |
| `Custom:AutoScribeSpells` | false | Every spell up to the character's level scribed on level-up and login. |
| `Custom:AutoLearnDisciplines` | false | Every discipline up to the character's level learned on level-up and login. |
| `Custom:KillFactionHits` | true | Kills change faction as usual. False: they never do. |

## Database

- `zone`: rest regen times (`fast_regen_hp`, `fast_regen_mana`, `fast_regen_endurance`). Only zones at the stock 180
  seconds change. Restart zones afterwards.
- `command_settings`, `command_subsettings`: `#zone`, `#mystats` and `#find zone` opened to players (access 0).

To turn off a database change, set the values back: 180 for the regen times, and your old access levels (the NMS release
has 50 for all three).

## Bases

Stock EQEmu and NMS. The held buff fixes, Bazaar and Back and the AA cap are NMS only: stock EQEmu has no group buff
holding and its AA cap is already -1.
