# Strike AAs to 70

Takes the level-capped "kill shot" AAs up to level 70.

| AA | Class | Change |
|---|---|---|
| Headshot | Ranger | Ranks for levels 64, 66, 68 and 70 after the 62 rank (stock PEQ has them switched off) |
| Assassinate | Rogue | The 68 and 70 ranks switched on |
| Dire Charm II | Enchanter, Druid, Necromancer | A second rank on each Dire Charm that charms up to level 70 instead of 46 |
| Decapitation | Berserker | Works like Headshot on Frenzy: six ranks, for targets up to level 60, 62, 64, 66, 68 and 70 |

Decapitation follows Headshot's rules: only on your target, only humanoids while `Combat:HeadshotOnlyHumanoids` is on,
and never on NPCs with Headshot immunity. The chance is Headshot's DEX formula. The client has no Decapitation spell
effect, so the level caps and damage (55,400 at rank 1 up to 82,600 at rank 6) are in the server code
(`Mob::TryDecapitation`). Rank 1 also loses the 50,000 damage spell PEQ gave it.

## Client files

- `client/spells_strike.txt`: append to the client's `spells_us.txt`. Without it Dire Charm II does nothing in the
  client.
- `client/dbstr_strike.txt`: replaces the `14200^1` and `14200^4` lines in `dbstr_us.txt` (Decapitation's name and
  description; PEQ calls it Cleaving Frenzy). The description starts with the NMS AA toggle hint; drop that part on
  stock EQEmu if you like.

## Rules and commands

None.

## Database

Spells 44030-44032 and AA ranks 19560-19567 (beside Paragon's 19000-19559). The SQL clears those IDs before adding
them, so it can be run again; check that your database doesn't already use them. AA and spell data load at server
start, so restart after applying.

## Bases

Stock EQEmu and NMS. On NMS any multiclass character with Berserker gets Decapitation on Frenzy; on stock EQEmu it's
the Berserker class.

## Credits

Written for Voidforged.
