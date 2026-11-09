# Personal loot offers (/nmsloot)

When an NPC dies, its loot tables are rolled again for the killer and for each group or raid member in the same zone.
Each player's roll is offered to them alone in a personal loot window, and they choose what to do with each item from
anywhere in the zone:

- **Keep**: into their inventory.
- **Sell**: for the item's merchant price.
- **Tribute**: for tribute points.
- **Bank**, **Vault**: straight into the bank or the Nautilus Vault.
- **Destroy**.
- **Pass**: offer it to another group or raid member, who can send it back.

Unclaimed offers expire after `Custom:NmsLootOfferExpireSeconds`. Offers survive zoning back in while they last.
Opening the corpse only resends the window.

The corpse still drops its normal loot as well, unless the rules below empty it. Items added by quests always stay on
the corpse.

## Client

Two loot windows are supported:

- The NMS client add-on (`dinput8.dll`, RoF2), through `OP_NmsLootOffer` and `OP_NmsLootDecision`.
- Hailstone's personal loot window. A Hailstone client says Hello when it zones in, and from then on gets its offers
  in that window's protocol (`OP_PersonalLoot*`).

Players without either add-on can't see their offers, so the module ships off.

## Rules

| Rule | Default | What it does |
|---|---|---|
| `Custom:NmsLootOffers` | false | Turns personal loot offers on. Off = corpse loot only. |
| `Custom:NmsLootOfferExpireSeconds` | 300 | Seconds before an unclaimed offer expires. |
| `Custom:NmsLootEmptyGroupCorpse` | true | With offers going to 2 or more players, the corpse's loot table items are removed and an emptied corpse decays at once. |
| `Custom:NmsLootEmptySoloCorpse` | false | The same for a lone player, so only the personal roll remains. |

## Commands

`#nmsloot_decide offer_id action [pass_to]` (GM Admin) applies a decision by hand, for testing: action 1 Keep, 2 Sell,
3 Tribute, 4 Bank, 5 Vault, 6 Destroy, 7 Pass, 9 return a passed item.

## Database

`character_nms_loot_offers`: open offers, one row per item. Rows clear when decided or expired, so removing the module
loses only the offers open at the time.

## Requires

`vault`, for the Vault action and the shared vault item code.

## Bases

Stock EQEmu and NMS, with separate core patches. On NMS, personal rolls also get the NMS loot buff upgrade roll
(`DoUpgradeLoot`), and loot-table items a full corpse emptying would remove are not upgraded or announced. Stock EQEmu
has no loot buff, so that code is left out there (`EQMOD_BASE_NMS`).

## Credits

The /nmsloot window and protocol come from Rockin-Vik's NMS-Release. The independent rolls, passing, corpse emptying,
and Hailstone window support were written for Voidforged.
