# Platinum economy

NMS pays for its services in Echoes of Memory, an alternate currency that drops rarely from kills. This module takes
the Echoes out and charges platinum instead, at 1 Echo = 1,000 platinum, so every service can be bought with money
earned in game.

## What changes

Quests (patched into the quests folder):

| NPC | Service | Cost |
|---|---|---|
| Bazaar, 151061 | Name, race, deity, gender and pet name changes | 10,000 platinum each (was 10 Echoes or 25,000 platinum) |
| Vision of Ayonae (Bazaar) | AA reset | 5,000 platinum |
| Vision of Ayonae (Bazaar) | Class removal | 10,000 platinum |
| Purveyor of Glamour (Bazaar) | Random Glamour | 2,000 platinum |
| Apocrypha (Bazaar) | Worldwide buffs | 5,000 to 35,000 platinum |
| Apocrypha (cshome) | Worldwide buffs | 5,000 platinum each, 25,000 for all of them |
| Tearel (Bazaar), Son of Tearel (East Commons) | Group transport and instance return, for the whole account | 5,000 platinum |

A Fading Ally (cshome) loses its GM "eom" phrase that handed out 10 Echoes.

Plugins (patched into the plugins folder): `SpendEOM.pl` drops `SpendEOM`, `GetEOM`, `EOMLink` and `LootEOM` and gains
`plugin::SpendPlatinum($client, $platinum)` and `plugin::HasPlatinum($client, $platinum)`. Both count carried money
only, not the bank. Other quests that still call the old Echo functions stop working, so search your own quests for
them first.

Database (`nms/sql`):

- `Custom:EventEOMDropChance`, `Custom:EoMUnlockCharacterSetCost` and `Custom:EoMUnlockCharacterSlotCost` set to 0 in
  every rule set: Echoes stop dropping and the login screen unlocks are free (still capped by
  `Custom:EoMUnlockCharacterSets` and `Custom:EoMUnlockCharacterSlots`).
- The Echo of Memory merchant (npc 1120001186, merchant 1000023) becomes the Collector of Curios and sells its 51 items
  for platinum, priced at 1,000 platinum per Echo.
- Alternate currency 6 is removed.
- Every item can be sold: the 35,605 items that cost 0 in the NMS release are priced at 1,000 platinum. Only items
  still at price 0 change, so prices you set yourself are kept.

Echoes players already hold are left in the database but can no longer be spent. The drop code itself stays in the
server, turned off by the rule.

## Installing

```
python tools/modules.py install --server Release-NMS-Server --quests Release-NMS-Quests --plugins Release-NMS-Plugins platinum-economy
```

Without `--quests` and `--plugins` only the database part is installed. Run `sql` afterwards and restart world and
zone. The item prices also need `shared_memory` run first.

## Bases

NMS only: stock EQEmu has no Echo of Memory.
