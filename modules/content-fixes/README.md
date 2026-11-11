# Content fixes

Changes to game content, all in the database except Xeru's encounter script.

| Change | Bases | File |
|---|---|---|
| AA spells that were also flagged usable by a class at a normal level (Gut Punch, Area Taunt, Press the Attack, Grappling Strike, Bite of the Asp, Focus of Arcanum, Imperator's Command) can't be scribed any more, and are taken out of spell books and spell bars. The AAs still cast them. Matters most with automatic spell scribing (`qol`). | both | `sql/2026_11_08_02_gut_punch_unscribable.sql`, `sql/2026_11_10_01_aa_spells_unscribable.sql` |
| Open-world Lord Inquisitor Seru (leash form, 159691) drops from 1,201,500 hit points and 1,000 regen to 250,000 and 50. | both | `sql/2026_11_07_01_seru_hp.sql` |
| Two rows of tradeskill stations (forge, oven, brew barrel, loom, pottery wheel, kiln) by the Bazaar banks. | both | `sql/2026_11_08_05_bazaar_bank_tradeskills.sql` |
| Items NPCs drop that had no price sell for 1 copper (9,338 items), so loot can be vendored. | both | `sql/2026_11_07_01_drop_prices_1cp.sql` |
| Items with no classes or the old all-classes mask become usable by every class. | both | `sql/2026_10_28_01_items_all_classes.sql` |
| #Echo_of_Sebilis (level 69) no longer spawns in Sebilis. | NMS | `nms/sql/2026_11_07_02_remove_echo_of_sebilis.sql` |
| High Inquisitor Xeru, a Seru-clone bonus boss who spawns when either Seru form dies and calls in the four Praesertum lieutenants. His loot uses NMS item qualities. | NMS | `nms/sql/2026_11_06_01_xeru.sql`, `nms/files/quests/sseru/` |
| The seven NMS Echo server buffs can't be scribed and leave spell books (Apocrypha still casts them). | NMS | `nms/sql/2026_11_04_01_echo_spells_unscribable.sql` |
| Thirteen Echo of the Past NPCs that stood 500 to 7,500 units from the zone-in point move next to it. | NMS | `nms/sql/2026_11_10_02_echo_of_the_past_near_safe_point.sql` |

## Applying

- Spell and item changes load at server start, and spell books must not be in memory: apply with nobody online, then restart.
- The Echo of the Past move also updates saved zone state; apply it with the server stopped, or running zones save
  the old positions back when they shut down.
- The Bazaar stations load at zone boot (restart or `#repop` the Bazaar). That file adds rows each time it runs, so
  run it once; the module SQL tracking does that for you.

## Rules and commands

None.

## Credits

The Xeru encounter script is from the Triptych-Triumvirate server (saltamontes5k), ported unchanged. Written for
Voidforged.
