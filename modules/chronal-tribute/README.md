# Chronal Tributes

Four personal tributes that only work inside a Greater Rift, as a favor sink for rift players. Each has five tiers, and
each tier covers one band of rift tiers: tier I works in rift tiers 1-100, tier II in 101-200, and so on up to tier V
(401-500). Tiers stack, so a character with tier III gets the benefit of whichever band the rift is in, up to III.

| Tribute | Per tier |
|---|---|
| Chronal Might | +5 attack, +3 heroic strength and dexterity, +50 hit points |
| Chronal Arcana | +10 spell damage and healing, +50 mana, +3 heroic intelligence and wisdom |
| Chronal Bulwark | +5 armor class, +75 hit points, +3 heroic stamina, +2 heroic resists |
| Chronal Fortune | +5% Chronal Shards from a rift clear |

Instead of the usual cost every 10 minutes, a Chronal Tribute takes favor once per rift run, on entering the rift (or
on turning it on inside one): `Custom:ChronalTributeFavorPerTier` x the rift's tier. Outside a rift, or above its
band, the tribute gives nothing and its benefit item is taken out of the tribute slot, so the client doesn't count it.

The zone writes the character's active Chronal Tributes to the `chronal_tributes` data bucket. The `greater-rifts`
Lua reads it for Chronal Fortune; its tribute ID is `Custom:ChronalTributeFirstID` + 3 unless `rift_config.lua` sets
`fortune_tribute_id`.

## Rules

| Rule | Default | |
|---|---:|---|
| `Custom:ChronalTributeFirstID` | 60 | First tribute ID that is a Chronal Tribute |
| `Custom:ChronalTributeLastID` | 69 | Last tribute ID that is a Chronal Tribute |
| `Custom:ChronalTributeBandSize` | 100 | Rift tiers per tribute tier |
| `Custom:ChronalTributeFavorPerTier` | 100 | Favor per rift run, x the rift's tier |

## Database

Tributes 60-63 on NMS, 90-93 on stock EQEmu (the stock SQL also sets the two ID rules to 90/99), and benefit items
980001-980035, copied from item 56300. The SQL deletes those IDs first, so it can be run again; check that your
database doesn't already use them. Run `shared_memory` and restart zones after applying it.

## Bases

Stock EQEmu and NMS. Requires `greater-rifts`.

## Credits

Written for Voidforged.
