# Module inventory (phase 1)

Everything Voidforged added on top of the NMS release (commit `4d9f2224`, "Initial commit of NMS-Release"), mapped
to the module it belongs to. Measured against the Voidforged repository at commit `0c897d30`: 67 commits, 259 files,
about 36,400 lines added. Nothing has been moved yet.

- **Core edits** are lines added inside files the NMS release already had. They become hooks behind each module's
  build option.
- **New files** are files the NMS release didn't have. A module owns these outright.
- Every added line was traced to the commit that wrote it. Commits that covered several features were split by what
  the lines mention, then checked by hand. The line-by-line list is `core_blocks.csv`; new files are in `new_files.csv`.

## Bases

Modules target plain EQEmu (what akk-stack builds) first, with NMS as a second supported base (decided
2026-11-09). Each module lists the bases it supports; NMS-only pieces (multiclass hooks, Echo of Memory) become
small NMS add-ons inside the module. Phase 2 checks every module on both bases.

"Runs on EQEmu today" means the module is already ported to the single-class server, which runs on stock EQEmu.

## Summary

| Module | What it is | Needs | Bases | Core edits | New files |
|---|---|---|---|---:|---:|
| `framework` | **Module framework.** Build options, the shared database version, and merchant rows gated by data buckets (used by tier gear and other unlocks). | — | EQEmu + NMS (runs on EQEmu today) | 33 lines, 4 files | 0 |
| `core-fixes` | **NMS bug fixes.** Fixes any NMS server wants: suppressed-buff dispel crash, target-of-target procs, zone-state loot tables, zone objects with no map floor, server buffs on zone boot, login lockout. | — | EQEmu + NMS | 21 lines, 5 files | 0 |
| `platform` | **Platform.** Docker packaging, nightly backups, VoidPatcher, content snapshot tools, Linux build fixes, client spell ID limit. | — | EQEmu + NMS, NMS-only parts | 20 lines, 3 files | 27 |
| `dynamic-items` | **Dynamic items.** Seeded random-stat items, class pools, item percent lines and caps, #dyninfo, #reforge. | `framework` | EQEmu + NMS (runs on EQEmu today) | 1774 lines, 21 files | 21 |
| `gear-sets` | **Armor and gear sets.** Armor set bonuses (stat and spell-granting), class set textures and icons, #gear saved gear sets. | `dynamic-items` | EQEmu + NMS (runs on EQEmu today) | 433 lines, 11 files | 8 |
| `glamour` | **Glamour vendors.** Glamour ornament vendors with tint sets; merchants refuse glamour resale. | — | EQEmu + NMS | 8 lines, 2 files | 7 |
| `greater-rifts` | **Greater Rifts.** Rift scripts, Guardians, pylons, champion affixes, rift zones, deepest-clear bucket, completion rewards, crash recovery. | `framework` | EQEmu + NMS (runs on EQEmu today) | 26 lines, 2 files | 26 |
| `tier-gear` | **Tiered rift gear.** Five tiers of armor, jewelry, Facet augments, weapons and ranger arrows on rift vendors. | `dynamic-items`, `gear-sets`, `greater-rifts` | EQEmu + NMS (runs on EQEmu today) | 0 lines, 0 files | 8 |
| `raid-portal` | **Raid portal.** Rift Raids: raid tiers, boss roster, raid instances (version 50), Prism Augmenter. | `greater-rifts` | EQEmu + NMS | 0 lines, 0 files | 60 |
| `the-void` | **The Void hub.** The Void opened as a hub: gate, waypoint, vendors, soulbinder, arrival point. | — | EQEmu + NMS, NMS-only parts | 0 lines, 0 files | 7 |
| `vault` | **Nautilus Vault.** Item vault, vault bags, proc locker, clicky buffs kept while vaulted. | `framework` | EQEmu + NMS (runs on EQEmu today) | 506 lines, 15 files | 4 |
| `loot-offers` | **Personal loot offers.** /nmsloot keep and sell rules, solo and group personal loot, group corpse emptying. | `framework` | EQEmu + NMS (runs on EQEmu today) | 144 lines, 11 files | 2 |
| `chronal-tribute` | **Chronal Tributes.** Tribute that scales with the rift band. | `greater-rifts` | EQEmu + NMS (runs on EQEmu today) | 26 lines, 2 files | 2 |
| `paragon-aa` | **Paragon AAs.** Toggleable Paragon AAs. | — | EQEmu + NMS (runs on EQEmu today) | 30 lines, 5 files | 3 |
| `triptych-aa` | **Triptych AA fixes.** Stacking spell damage AAs, Rogue and Ranger crits, buyable Glyphs, Throwing fixes. | — | EQEmu + NMS | 131 lines, 9 files | 0 |
| `strike-aa` | **Strike AAs to 70.** Headshot, Assassinate, Decapitation (Frenzy) and Dire Charm II ranks to level 70. | — | EQEmu + NMS | 55 lines, 3 files | 2 |
| `pet-power` | **Pet power.** Pet focus jewelry bonuses and excess pet power scaling. | — | EQEmu + NMS | 13 lines, 2 files | 0 |
| `multiclass-bard` | **Multiclass Bard disciplines.** Bards use disciplines from all their classes. | — | NMS only | 20 lines, 1 files | 0 |
| `qol` | **Quality of life.** Attack while casting, held group buffs and invisibility, rest regen, #zone and #mystats for players, auto train and scribe, Bazaar and Back. | — | EQEmu + NMS (runs on EQEmu today) | 137 lines, 12 files | 2 |
| `instances` | **Instance times.** Lockouts (non-respawning 6h, respawning 5m, Plane of Time 6h) and the expedition NPC scaling switch. | — | EQEmu + NMS | 9 lines, 2 files | 0 |
| `platinum-economy` | **Platinum economy.** Echo of Memory services paid in platinum, platinum AA sinks. | — | EQEmu + NMS, NMS-only parts | 372 lines, 9 files | 2 |
| `content-fixes` | **Content fixes.** Zone and NPC changes: Xeru and Sanctus Seru, Echo spells, Gut Punch, Bazaar tradeskill stations. | — | EQEmu + NMS | 0 lines, 0 files | 7 |
| `no-level-reqs` | **No item level requirements.** Every item usable at any level: required and recommended levels cleared. Database only. | — | EQEmu + NMS | 0 lines, 0 files | 0 |
| `hailstone` | **Hailstone client support.** Loot offers, vault bags and dynamic items for the Hailstone client. | `vault`, `loot-offers`, `dynamic-items` | EQEmu + NMS | 68 lines, 6 files | 3 |
| `docs` | **Documentation.** Player's Guide, README, design specs. | — | NMS only | 47 lines, 1 files | 3 |

## Modules

### `framework`: Module framework

Build options, the shared database version, and merchant rows gated by data buckets (used by tier gear and other unlocks).

Bases: EQEmu + NMS (runs on EQEmu today)

Core edits (lines added per file): `zone/client_process.cpp` 22, `zone/client_packet.cpp` 9, `common/version.h` 1, `zone/client.h` 1

### `core-fixes`: NMS bug fixes

Fixes any NMS server wants: suppressed-buff dispel crash, target-of-target procs, zone-state loot tables, zone objects with no map floor, server buffs on zone boot, login lockout.

Bases: EQEmu + NMS

Core edits (lines added per file): `zone/zone.cpp` 9, `zone/zone_save_state.cpp` 5, `zone/mob.cpp` 3, `zone/spell_effects.cpp` 3, `zone/zone.h` 1

### `platform`: Platform

Docker packaging, nightly backups, VoidPatcher, content snapshot tools, Linux build fixes, client spell ID limit.

Bases: EQEmu + NMS, NMS-only parts. On akk-stack, skip the Docker setup and backups (akk-stack has its own); VoidPatcher and the spell ID limit fix apply everywhere.

Core edits (lines added per file): `common/repositories/spells_new_repository.h` 10, `README.md` 8, `common/eqemu_logsys_log_aliases.h` 2

New files (27):

- `.dockerignore`
- `database/voidforged-content.zip`
- `docker/.env.example`
- `docker/.gitignore`
- `docker/Dockerfile`
- `docker/README.md`
- `docker/backup.sh`
- `docker/docker-compose.yml`
- `docker/start-login.sh`
- `docker/start.sh`
- `utils/patcher/.gitignore`
- `utils/patcher/README.md`
- `utils/patcher/VoidPatcher/MainForm.cs`
- `utils/patcher/VoidPatcher/Manifest.cs`
- `utils/patcher/VoidPatcher/Patcher.cs`
- `utils/patcher/VoidPatcher/Program.cs`
- `utils/patcher/VoidPatcher/VoidPatcher.csproj`
- `utils/patcher/VoidPatcher/app.manifest`
- `utils/patcher/build_manifest.py`
- `utils/patcher/patch_rules.txt`
- `utils/patcher/publish_box.sh`
- `utils/patcher/test_server.py`
- `utils/scripts/dump_content.py`
- `utils/scripts/rift/client/add_dbstr.py`
- `utils/scripts/rift/client/add_spells.py`
- `utils/scripts/rift/luacheck.py`
- `utils/scripts/rift/start_server.bat`

### `dynamic-items`: Dynamic items

Seeded random-stat items, class pools, item percent lines and caps, #dyninfo, #reforge.

Bases: EQEmu + NMS (runs on EQEmu today)

Needs: `framework`

Core edits (lines added per file): `common/database/database_update_manifest_custom.cpp` 1523, `zone/client_packet.cpp` 93, `common/item_instance.cpp` 29, `common/item_instance.h` 17, `zone/bonuses.cpp` 17, `zone/client.h` 16, `zone/effects.cpp` 16, `common/ruletypes.h` 15, `zone/client_mods.cpp` 9, `zone/main.cpp` 6, `zone/CMakeLists.txt` 5, `common/patches/rof.cpp` 3, `common/patches/rof2.cpp` 3, `common/patches/sod.cpp` 3, `common/patches/sof.cpp` 3, `common/patches/titanium.cpp` 3, `common/patches/uf.cpp` 3, `zone/client.cpp` 3, `zone/command.cpp` 3, `zone/command.h` 3, `common/CMakeLists.txt` 1

New files (21):

- `common/dynamic_item_structs.h`
- `docs/dynamic_items/README.md`
- `docs/dynamic_items/USER_GUIDE.md`
- `utils/scripts/dynamic_items/2026_10_22_berserker_no_1h.sql`
- `utils/scripts/dynamic_items/2026_10_22_heroics_base_rebalance.sql`
- `utils/scripts/dynamic_items/2026_10_22_hybrid_mana_endurance.sql`
- `utils/scripts/dynamic_items/2026_10_23_bis_rebalance.sql`
- `utils/scripts/dynamic_items/2026_10_23_hybrid_mana.sql`
- `utils/scripts/dynamic_items/2026_10_24_caster_rebalance.sql`
- `utils/scripts/dynamic_items/README.md`
- `utils/scripts/dynamic_items/blend_hybrids.py`
- `utils/scripts/dynamic_items/gen_v26_pool.py`
- `utils/scripts/dynamic_items/gen_v28_pool.py`
- `utils/scripts/dynamic_items/rebalance_casters.py`
- `utils/scripts/dynamic_items/rebalance_heroics.py`
- `utils/scripts/dynamic_items/rebalance_to_bis.py`
- `zone/dynamic_items.cpp`
- `zone/dynamic_items.h`
- `zone/dynamic_seed_parser.cpp`
- `zone/gm_commands/dynamic_items.cpp`
- `zone/gm_commands/reforge.cpp`

### `gear-sets`: Armor and gear sets

Armor set bonuses (stat and spell-granting), class set textures and icons, #gear saved gear sets.

Bases: EQEmu + NMS (runs on EQEmu today)

Needs: `dynamic-items`

Core edits (lines added per file): `zone/client.cpp` 285, `zone/spell_effects.cpp` 48, `zone/client.h` 46, `common/database/database_update_manifest_custom.cpp` 34, `zone/inventory.cpp` 8, `zone/zone.cpp` 6, `common/ruletypes.h` 2, `zone/CMakeLists.txt` 1, `zone/bonuses.cpp` 1, `zone/command.cpp` 1, `zone/command.h` 1

New files (8):

- `utils/scripts/dynamic_items/2026_11_02_armor_icons.sql`
- `utils/scripts/dynamic_items/class_sets.json`
- `utils/scripts/dynamic_items/gen_class_sets.py`
- `utils/scripts/rift/sql/class_sets_bonuses.sql`
- `utils/scripts/rift/sql/class_test_sets.sql`
- `zone/gear_sets.cpp`
- `zone/gear_sets.h`
- `zone/gm_commands/gear.cpp`

### `glamour`: Glamour vendors

Glamour ornament vendors with tint sets; merchants refuse glamour resale.

Bases: EQEmu + NMS

Core edits (lines added per file): `zone/client_packet.cpp` 7, `common/ruletypes.h` 1

New files (7):

- `utils/scripts/glamour/README.md`
- `utils/scripts/glamour/build_final_sheet.py`
- `utils/scripts/glamour/build_review_sheet.py`
- `utils/scripts/glamour/gen_glamour_vendors.py`
- `utils/scripts/glamour/glamour_final.xlsx`
- `utils/scripts/glamour/glamour_review.xlsx`
- `utils/scripts/glamour/sql/2026_10_24_glamour_vendors_ecommons.sql`

### `greater-rifts`: Greater Rifts

Rift scripts, Guardians, pylons, champion affixes, rift zones, deepest-clear bucket, completion rewards, crash recovery.

Bases: EQEmu + NMS (runs on EQEmu today)

Needs: `framework`

Core edits (lines added per file): `Release-NMS-Quests/sleeper/encounters/sleeper_custom.lua` 25, `README.md` 1

New files (26):

- `utils/scripts/rift/GlobalLoad.txt`
- `utils/scripts/rift/README.md`
- `utils/scripts/rift/gen_rift_appearances.py`
- `utils/scripts/rift/gen_rift_zones.py`
- `utils/scripts/rift/lua_modules/champion_affixes.lua`
- `utils/scripts/rift/lua_modules/rift_appearances.lua`
- `utils/scripts/rift/lua_modules/rift_config.lua`
- `utils/scripts/rift/lua_modules/rift_core.lua`
- `utils/scripts/rift/lua_modules/rift_zones.lua`
- `utils/scripts/rift/quests/global/Rift_Anachronism.lua`
- `utils/scripts/rift/quests/global/Rift_Controller.lua`
- `utils/scripts/rift/quests/global/Rift_Guardian.lua`
- `utils/scripts/rift/quests/global/Rift_Portal.lua`
- `utils/scripts/rift/quests/global/Rift_Pylon.lua`
- `utils/scripts/rift/quests/global/global_npc.pl`
- `utils/scripts/rift/quests/global/global_player.pl`
- `utils/scripts/rift/quests/txevu/encounters/acm_portal.lua`
- `utils/scripts/rift/sql/2026_10_22_01_vendor_zebuxoruk.sql`
- `utils/scripts/rift/sql/2026_10_22_02_archetypes_faction_rule.sql`
- `utils/scripts/rift/sql/2026_10_22_03_respawn.sql`
- `utils/scripts/rift/sql/2026_10_22_05_mob_levels.sql`
- `utils/scripts/rift/sql/2026_10_22_07_unlock_rift_doors.sql`
- `utils/scripts/rift/sql/2026_10_23_01_rift_npc_models.sql`
- `utils/scripts/rift/sql/2026_10_23_02_guardian_resists.sql`
- `utils/scripts/rift/sql/2026_10_23_03_rift_deepest_bucket.sql`
- `utils/scripts/rift/sql/rift_zones_setup.sql`

### `tier-gear`: Tiered rift gear

Five tiers of armor, jewelry, Facet augments, weapons and ranger arrows on rift vendors.

Bases: EQEmu + NMS (runs on EQEmu today)

Needs: `dynamic-items`, `gear-sets`, `greater-rifts`

New files (8):

- `docs/dynamic_items/TIERED_GEAR.md`
- `utils/scripts/dynamic_items/2026_10_23_tier_gear.sql`
- `utils/scripts/dynamic_items/gen_tier_gear.py`
- `utils/scripts/dynamic_items/tier_gear.json`
- `utils/scripts/rift/sql/2026_11_03_02_tier_facet_augments.sql`
- `utils/scripts/rift/sql/2026_11_03_03_tier_weapons_raid_augments.sql`
- `utils/scripts/rift/sql/2026_11_03_04_tier1_vendor_spots.sql`
- `utils/scripts/rift/sql/2026_11_09_03_tier_ranger_arrows.sql`

### `raid-portal`: Raid portal

Rift Raids: raid tiers, boss roster, raid instances (version 50), Prism Augmenter.

Bases: EQEmu + NMS. Lua and SQL on Greater Rifts; not yet tried on plain EQEmu.

Needs: `greater-rifts`

New files (60):

- `docs/raids/RAID_PORTAL.md`
- `utils/scripts/rift/client/dbstr_raid.txt`
- `utils/scripts/rift/lua_modules/raid_portal.lua`
- `utils/scripts/rift/plugins/raid_portal.pl`
- `utils/scripts/rift/quests/codecay/script_init_v50.lua`
- `utils/scripts/rift/quests/global/Raid_Controller.lua`
- `utils/scripts/rift/quests/growthplane/script_init_v50.lua`
- `utils/scripts/rift/quests/inktuta/script_init_v50.lua`
- `utils/scripts/rift/quests/mischiefplane/script_init_v50.lua`
- `utils/scripts/rift/quests/sebilis/script_init_v50.lua`
- `utils/scripts/rift/quests/sleeper/script_init_v50.lua`
- `utils/scripts/rift/quests/sseru/script_init_v50.lua`
- `utils/scripts/rift/quests/ssratemple/script_init_v50.lua`
- `utils/scripts/rift/quests/tacvi/script_init_v50.lua`
- `utils/scripts/rift/quests/txevu/script_init_v50.lua`
- `utils/scripts/rift/sql/2026_11_02_01_raid_portal_test.sql`
- `utils/scripts/rift/sql/2026_11_02_02_raid_portal_spawn.sql`
- `utils/scripts/rift/sql/2026_11_03_01_raid_portal_shared_bosses.sql`
- `utils/scripts/rift/sql/2026_11_08_01_raid_portal_own_bosses.sql`
- 41 raid instance quest files under `utils/scripts/rift/quests/*/v50/`

### `the-void`: The Void hub

The Void opened as a hub: gate, waypoint, vendors, soulbinder, arrival point.

Bases: EQEmu + NMS, NMS-only parts. The soulbinder already runs on EQEmu; the gate and waypoint use the NMS Waypoints map.

New files (7):

- `utils/scripts/rift/quests/thevoida/1200050.lua`
- `utils/scripts/rift/quests/thevoida/1200071.lua`
- `utils/scripts/rift/quests/thevoida/459000.lua`
- `utils/scripts/rift/quests/thevoida/Soulbinder_Ilsara.pl`
- `utils/scripts/rift/sql/2026_10_22_04_void_waypoint_buff_rule.sql`
- `utils/scripts/rift/sql/2026_10_22_06_open_void.sql`
- `utils/scripts/rift/sql/void_soulbinder.sql`

### `vault`: Nautilus Vault

Item vault, vault bags, proc locker, clicky buffs kept while vaulted.

Bases: EQEmu + NMS (runs on EQEmu today)

Needs: `framework`

Core edits (lines added per file): `common/database/database_update_manifest_custom.cpp` 250, `zone/attack.cpp` 74, `zone/inventory.cpp` 43, `zone/spell_effects.cpp` 38, `zone/client_packet.cpp` 31, `zone/client.h` 13, `common/inventory_profile.cpp` 10, `zone/client_process.cpp` 9, `zone/command.cpp` 8, `zone/command.h` 8, `common/inventory_profile.h` 6, `zone/client.cpp` 6, `zone/CMakeLists.txt` 5, `zone/bonuses.cpp` 3, `common/item_instance.cpp` 2

New files (4):

- `common/nms_vault_item.h`
- `zone/gm_commands/vault.cpp`
- `zone/nms_vault.cpp`
- `zone/nms_vault.h`

### `loot-offers`: Personal loot offers

/nmsloot keep and sell rules, solo and group personal loot, group corpse emptying.

Bases: EQEmu + NMS (runs on EQEmu today)

Needs: `framework`

Core edits (lines added per file): `zone/corpse.cpp` 45, `common/eq_packet_structs.h` 41, `zone/loot.cpp` 20, `zone/attack.cpp` 18, `zone/client_packet.cpp` 7, `zone/corpse.h` 4, `common/emu_oplist.h` 2, `common/ruletypes.h` 2, `utils/patches/patch_RoF2.conf` 2, `zone/npc.h` 2, `zone/client_packet.h` 1

New files (2):

- `zone/nms_loot_offers.cpp`
- `zone/nms_loot_offers.h`

### `chronal-tribute`: Chronal Tributes

Tribute that scales with the rift band.

Bases: EQEmu + NMS (runs on EQEmu today)

Needs: `greater-rifts`

Core edits (lines added per file): `zone/tribute.cpp` 17, `zone/bonuses.cpp` 9

New files (2):

- `zone/nms_chronal_tribute.cpp`
- `zone/nms_chronal_tribute.h`

### `paragon-aa`: Paragon AAs

Toggleable Paragon AAs.

Bases: EQEmu + NMS (runs on EQEmu today)

Core edits (lines added per file): `common/ruletypes.h` 12, `zone/aa.cpp` 8, `zone/CMakeLists.txt` 6, `zone/bonuses.cpp` 3, `zone/mob.h` 1

New files (3):

- `utils/scripts/rift/client/dbstr_paragon.txt`
- `zone/nms_paragon.cpp`
- `zone/nms_paragon.h`

### `triptych-aa`: Triptych AA fixes

Stacking spell damage AAs, Rogue and Ranger crits, buyable Glyphs, Throwing fixes.

Bases: EQEmu + NMS. Stock EQEmu combat and AA code; needs a careful merge.

Core edits (lines added per file): `zone/spell_effects.cpp` 41, `zone/aa.cpp` 35, `zone/effects.cpp` 24, `zone/attack.cpp` 10, `zone/special_attacks.cpp` 7, `common/ruletypes.h` 6, `zone/bonuses.cpp` 6, `zone/common.h` 1, `zone/mob.h` 1

### `strike-aa`: Strike AAs to 70

Headshot, Assassinate, Decapitation (Frenzy) and Dire Charm II ranks to level 70.

Bases: EQEmu + NMS

Core edits (lines added per file): `zone/special_attacks.cpp` 46, `zone/attack.cpp` 8, `zone/mob.h` 1

New files (2):

- `utils/scripts/rift/sql/2026_11_09_01_level_cap_aa_ranks.sql`
- `utils/scripts/rift/sql/2026_11_09_02_decapitation_ranks.sql`

### `pet-power`: Pet power

Pet focus jewelry bonuses and excess pet power scaling.

Bases: EQEmu + NMS

Core edits (lines added per file): `zone/pets.cpp` 12, `common/ruletypes.h` 1

### `multiclass-bard`: Multiclass Bard disciplines

Bards use disciplines from all their classes.

Bases: NMS only. Only meaningful with NMS multiclassing.

Core edits (lines added per file): `zone/client.cpp` 20

### `qol`: Quality of life

Attack while casting, held group buffs and invisibility, rest regen, #zone and #mystats for players, auto train and scribe, Bazaar and Back.

Bases: EQEmu + NMS (runs on EQEmu today)

Core edits (lines added per file): `zone/client.cpp` 56, `zone/gm_commands/zone.cpp` 39, `zone/command.cpp` 11, `common/ruletypes.h` 7, `zone/attack.cpp` 5, `zone/exp.cpp` 5, `Release-NMS-Quests/global/spells/5824.pl` 4, `zone/spell_effects.cpp` 4, `zone/client.h` 2, `zone/special_attacks.cpp` 2, `zone/client_packet.cpp` 1, `zone/client_process.cpp` 1

New files (2):

- `utils/scripts/rift/sql/2026_11_08_03_hub_fast_regen.sql`
- `utils/scripts/rift/sql/2026_11_08_04_mystats_for_players.sql`

### `instances`: Instance times

Lockouts (non-respawning 6h, respawning 5m, Plane of Time 6h) and the expedition NPC scaling switch.

Bases: EQEmu + NMS. Lockout times live in an NMS Perl plugin; on EQEmu they become rule settings.

Core edits (lines added per file): `Release-NMS-Plugins/NMS_instance_utils.pl` 7, `Release-NMS-Quests/potimea/player.lua` 2

### `platinum-economy`: Platinum economy

Echo of Memory services paid in platinum, platinum AA sinks.

Bases: EQEmu + NMS, NMS-only parts. The platinum sinks run on EQEmu; the Echo of Memory services are NMS NPCs and currency.

Core edits (lines added per file): `Release-NMS-Quests/cshome/Apocrypha.pl` 180, `Release-NMS-Quests/bazaar/Tearel.pl` 60, `Release-NMS-Quests/ecommons/Son_of_Tearel.pl` 60, `zone/loot.cpp` 24, `Release-NMS-Quests/bazaar/151061.pl` 14, `Release-NMS-Quests/bazaar/Apocrypha.pl` 12, `Release-NMS-Quests/bazaar/Vision_of_Ayonae.pl` 10, `Release-NMS-Plugins/SpendEOM.pl` 8, `Release-NMS-Quests/bazaar/Purveyor_of_Glamour.pl` 4

New files (2):

- `utils/scripts/rift/gen_sinks.py`
- `utils/scripts/rift/sql/2026_10_27_01_plat_aa_sinks.sql`

### `content-fixes`: Content fixes

Zone and NPC changes: Xeru and Sanctus Seru, Echo spells, Gut Punch, Bazaar tradeskill stations.

Bases: EQEmu + NMS

New files (7):

- `utils/scripts/rift/quests/sseru/encounters/xeru_custom.lua`
- `utils/scripts/rift/quests/sseru/script_init.lua`
- `utils/scripts/rift/sql/2026_11_04_01_echo_spells_unscribable.sql`
- `utils/scripts/rift/sql/2026_11_06_01_xeru.sql`
- `utils/scripts/rift/sql/2026_11_07_01_seru_hp.sql`
- `utils/scripts/rift/sql/2026_11_08_02_gut_punch_unscribable.sql`
- `utils/scripts/rift/sql/2026_11_08_05_bazaar_bank_tradeskills.sql`

### `no-level-reqs`: No item level requirements

Every item usable at any level: required and recommended levels cleared. Database only.

Bases: EQEmu + NMS

### `hailstone`: Hailstone client support

Loot offers, vault bags and dynamic items for the Hailstone client.

Bases: EQEmu + NMS

Needs: `vault`, `loot-offers`, `dynamic-items`

Core edits (lines added per file): `common/eq_packet_structs.h` 50, `zone/client_packet.cpp` 6, `common/emu_oplist.h` 4, `utils/patches/patch_RoF2.conf` 4, `zone/client.h` 3, `zone/client_packet.h` 1

New files (3):

- `utils/hailstone-dynitems/README.md`
- `utils/hailstone-dynitems/dynitems/init.lua`
- `utils/hailstone-dynitems/dynitems/ui/modern/dynitems.lua`

### `docs`: Documentation

Player's Guide, README, design specs.

Bases: NMS only

Core edits (lines added per file): `README.md` 47

New files (3):

- `docs/guild_halls/GUILD_HALLS.md`
- `docs/players/Voidforged_Players_Guide.pdf`
- `docs/players/make_players_guide.py`

## Not in git

Some changes were made straight to the live database and exist only there and in the content snapshot
(`database/voidforged-content.zip`): for example the 1 cp sell price on 0-price drops, removing Echo of Sebilis, and
the Chronal Prism db_str rows. Phase 1b compares the snapshot against stock PEQ so each of these gets a module and an
SQL file.

## Database baseline

The NMS release has no full database dump. It runs on a stock PEQ database plus its own migrations in
`common/database/database_update_manifest_custom.cpp`. Our migrations went into that same file (about 1,800 lines,
mostly dynamic items and the vault), so each module will carry its own migrations instead. The clean test baseline
is a stock PEQ dump from the release's date plus the NMS migrations.

## Next

1. Review this split: rename, merge or move anything.
2. Phase 1b: the database-only changes above.
3. Phase 2: the module framework (build options, module folders, the install script) and the checks:
   on NMS, everything on builds today's Voidforged and everything off builds the NMS release; on plain EQEmu,
   everything off builds stock EQEmu and each EQEmu-supported module builds and loads on its own.
