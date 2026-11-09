# EQEmu Modules

Optional features for EverQuest emulator servers, each one a module you can pick and build in: random-stat items,
armor set bonuses, Greater Rifts, tiered rift gear, a raid portal, an item vault, personal loot offers, AA and combat
additions, quality-of-life changes and fixes.

Modules support two bases:

- **EQEmu**: the stock [EQEmu server](https://github.com/EQEmu/Server), including servers run with akk-stack.
- **NMS**: the NMS release, an EQEmu-based server with multiclassing.

Most modules work on both. A few have parts only for NMS, such as multiclass hooks.

The modules come from Voidforged, an NMS-based server, and its single-class sibling on stock EQEmu.

## Status

Work in progress. Nothing here is installable yet.

1. **Inventory** (done): every Voidforged addition mapped to a module. See `docs/inventory/INVENTORY.md`.
2. **Database-only changes**: content that was changed in the live database but not in SQL files gets a module and an
   SQL file.
3. **Framework**: a build option per module, module folders, and an install script that checks dependencies and
   gathers each selected module's SQL, quests and Lua.
4. **Modules**: moved in one at a time, each checked on both bases.

## License

GPL-3.0, the same as EQEmu and the NMS release. See `LICENSE`.
