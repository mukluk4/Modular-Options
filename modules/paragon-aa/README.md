# Paragon AAs

Twelve long AA lines with rising costs, as a sink for AA points once a character has bought what they need. Each needs
level 51.

| Line | Per rank | Ranks | Total cost |
|---|---|---:|---:|
| Paragon of Vitality | +25 hit points | 50 | 1,475 |
| Paragon of the Mind | +25 mana | 50 | 1,475 |
| Paragon of Stamina | +25 endurance | 50 | 1,475 |
| Paragon of Fortitude | +1 armor class | 50 | 1,475 |
| Paragon of Might | +1 attack | 50 | 1,475 |
| Paragon of Ferocity | +1% melee damage | 10 | 700 |
| Paragon of Strength, Endurance, Agility, Dexterity, Intellect, Wisdom | +1 of that heroic stat | 50 each | 4,425 each |

The client has no spell effect for heroic stats, so the six heroic lines use effect IDs only this server knows
(9001-9006). The server adds them to the character's item heroics, which every heroic stat formula reads, and leaves
them out of the AA window packets so the client never sees an effect it doesn't understand.

## Client strings

The AA window shows each line's name and description from the client's `dbstr_us.txt`. Append
`client/dbstr_paragon.txt` to `dbstr_us.txt` in the client folder (and in your patcher, if you have one). Without it
the lines still work but show no name.

## Rules and commands

None. Remove the SQL rows to take the lines away.

## Database

AA abilities 17800-17811 and ranks 19000-19559. The SQL deletes that ID range first, so it can be run again; check
that your database doesn't already use those IDs. Restart zones after applying it.

## Bases

Stock EQEmu and NMS. On NMS, a Paragon line the player has switched off (NMS AA toggles) gives no heroic stats; stock
EQEmu has no AA toggles.

## Credits

Written for Voidforged.
