# Database changes (phase 1b)

Every content difference between the NMS release database (`database/release-peq.zip` in the NMS release) and the
live Voidforged database on 2026-11-09, by table, with the module each belongs to. Only content tables were compared
(105 tables, no player data). Rows were matched by primary key.

**Source** says where the change already lives:

- **SQL**: an SQL file in the Voidforged repository.
- **migration**: a migration in `database_update_manifest_custom.cpp`.
- **generator**: written by a generator script (tier gear, class sets, glamour vendors, rift zones).
- **live only**: made straight in the live database. These need an SQL file in their module.

## Not changed by us

| Table | Change | Why |
|---|---|---|
| `eqtime`, `spawn_events` | game clock and event schedule | The server writes these while it runs |
| `variables` row 4 | timestamp only | Server bookkeeping |
| `launcher` | `dynamics` 5 to 15 | Server setup, not content: the launcher starts 15 zones |

## New tables

| Table | Rows | Module | Source |
|---|---:|---|---|
| `dynamic_items` | 1,916 | `dynamic-items`, `tier-gear` | migration, generator |
| `dynamic_affix_pool` | 916 | `dynamic-items` | migration |
| `dynamic_affix_suffixes` | 43 | `dynamic-items` | migration |
| `armor_set_bonuses` | 884 | `gear-sets`, `tier-gear` | migration, generator |
| `armor_set_items` | 1,207 | `gear-sets`, `tier-gear` | migration, generator |

## Changed tables

| Table | Added | Removed | Changed | What it is | Module | Source |
|---|---:|---:|---:|---|---|---|
| `aa_ability` | 12 | | | Paragon AAs (17800-17811) | `paragon-aa` | SQL |
| `aa_ranks`, `aa_rank_effects` | 568, 560 | | 10, 4 | Paragon and NMS AA ranks; Headshot, Assassinate, Dire Charm II and Decapitation ranks | `paragon-aa`, `strike-aa` | SQL |
| `spells_new` | 37 | | 8 | NMS AA spells (Hail of Arrows and others), tier set spells 44001-44029, Dire Charm II 44030-44032; Echo spells and Gut Punch unscribable | `paragon-aa`, `tier-gear`, `strike-aa`, `content-fixes` | SQL |
| `db_str` | 28 | | 2 | AA and currency names (Chronal Prism, Paragon, raid); Decapitation rename | `paragon-aa`, `raid-portal`, `strike-aa` | SQL, **live only** (Chronal Prism rows) |
| `items` | 2,062 | | 155,139 | New: tier gear, glamour, vault and raid items (900000-965399). Changed: see below | several | generator, SQL, **live only** |
| `merchantlist` | 4,624 | | 51 | Tier, glamour, rift, Void and raid vendors; 51 Echo of Memory costs set to 0 | `tier-gear`, `glamour`, `greater-rifts`, `the-void`, `raid-portal`, `platinum-economy` | generator, SQL |
| `npc_types` | 53 | | 4 | Rift Controller, Guardians, Pylons, vendors (1200000+), raid bosses; Echo merchant became Collector of Curios; Seru HP; Zebuxoruk; Roosevelt's model | `greater-rifts`, `tier-gear`, `raid-portal`, `platinum-economy`, `content-fixes` | SQL, **live only** (Roosevelt) |
| `spawn2`, `spawngroup`, `spawnentry` | 8,023, 46, 49 | 2, 0, 40 | 1 | Rift and raid instance spawns, vendor spawns; Echo of Sebilis removed (40); 2 spawns removed | `greater-rifts`, `raid-portal`, `tier-gear`, `glamour`, `the-void`, `content-fixes` | SQL, **live only** (Echo of Sebilis) |
| `doors`, `zone_points`, `ground_spawns`, `zone` | 2,723, 251, 206, 58 | 0, 0, 0, 1 | 592 | Raid and rift instance versions of each zone (version 50); rest regen 180 to 60 in every zone | `raid-portal`, `greater-rifts`, `qol` | SQL |
| `object` | 12 | | | Bazaar tradeskill stations | `content-fixes` | SQL |
| `rule_values` | 33 | | 29 | Module rules (`Custom:*`) and changed caps (item ATK, combat effects, AA) | each module's own rules | migration, SQL, **live only** |
| `command_settings`, `command_subsettings` | 12 | | 3 | Module commands (#dyninfo, #gear, #vault, /nmsloot); #zone and #mystats for players | `dynamic-items`, `gear-sets`, `vault`, `loot-offers`, `qol` | migration, SQL |
| `tributes`, `tribute_levels` | 4, 20 | | | Chronal Tributes | `chronal-tribute` | SQL |
| `alternate_currency` | 2 | 1 | | Chronal Shards and the raid currency added; Echo of Memory (6) removed | `greater-rifts`, `raid-portal`, `platinum-economy` | SQL |
| `loottable`, `lootdrop`, `loottable_entries`, `global_loot` | 1 each | | | Global wearable pool | `dynamic-items` | migration |
| `nms_waypoints` | 1 | | | The Void waypoint | `the-void` | SQL |
| `variables` row 6 | | | 1 | Message of the day ("Welcome to Voidforged...") | `docs` (Voidforged only) | **live only** |

## Items

| Change | Items | Module | Source |
|---|---:|---|---|
| Price 0 to 1 copper (mob drops) | 9,340 | `content-fixes` | **live only** (backup `items_price_backup_20261107`) |
| Classes 0 or 32767 to 65535 (all classes) | 9,645 | `content-fixes` | **live only** (backup `items_backup_20261028_classes`) |
| Price 0 to a real price (every item can be sold): 35,605 at 1,000 platinum, 48 Echo merchant goods | 35,653 | `platinum-economy` | SQL (rebuilt from live) |
| Required level removed (`reqlevel` to 0) | 84,263, 66,077 of them above 65 | `no-level-reqs` | **live only** |
| Recommended level removed (`reclevel` to 0) | 60,614 | `no-level-reqs` | **live only** |

Both were done by hand on the live database, on purpose: Voidforged has no item level requirements, and every item
has a price. `no-level-reqs` is its own module so other servers can leave it out. The exact SQL was not kept, so the
module rebuilds it from the end state (every `reqlevel` and `reclevel` set to 0). The prices are rebuilt from the live
values in `platinum-economy`.
