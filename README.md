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

Work in progress. Modules so far: `merchant-buckets`, `vault`, `loot-offers`, `paragon-aa`, `platinum-economy`,
`qol`, `core-fixes`, `strike-aa`, `triptych-aa`, `pet-power`, `instances`, `multiclass-bard`, `content-fixes`,
`drakkin` and `no-level-reqs`; the rest are being moved in.

1. **Inventory** (done): every Voidforged addition mapped to a module. See `docs/inventory/INVENTORY.md`.
2. **Database changes** (done): every content change compared with the NMS release database, by module. See
   `docs/inventory/DATABASE.md`.
3. **Framework** (done): module folders and `tools/modules.py`, which checks requirements, installs modules into a
   server source tree and applies their SQL. See `docs/FRAMEWORK.md`.
4. **Modules**: moved in one at a time, each installed and built on the bases it supports.

## Quick start

```
python tools/modules.py list
python tools/modules.py install --server <server source> --quests <quests folder> --plugins <plugins folder> <module> ...
python tools/modules.py sql --server <server source> --mysql "mysql peq"
```

## License

GPL-3.0, the same as EQEmu and the NMS release. See `LICENSE`.
