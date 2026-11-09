# Module framework

How modules are laid out, what installing them changes in a server source tree, and how their database changes are
applied. Everything here is done by `tools/modules.py` (Python 3, plus `git`).

## Installing

Start from a clean checkout of the server source: stock EQEmu (what akk-stack builds) or the NMS release.

```
python tools/modules.py list
python tools/modules.py install --server <server source> --quests <quests folder> merchant-buckets ...
```

- `--server` is the folder that holds `zone/` and `common/`. For the NMS release that is `Release-NMS-Server`.
- `--quests` is the quests folder (for NMS, `Release-NMS-Quests`). Without it, quest files are skipped with a warning.
- `--all` installs every module that supports the base.
- The base (EQEmu or NMS) is detected from the tree; `--base` overrides it.
- Requirements are added and ordered automatically: asking for `tier-gear` also installs what it needs.

Install refuses a tree with uncommitted changes, and a tree that already has modules (`modules.lock.json`). To change
the set of modules, go back to a clean tree (`git checkout . && git clean -fd`) and install again. Then build the server
as usual and apply the database changes:

```
python tools/modules.py sql --server <server source> --mysql "mysql peq"
```

`--mysql` is any shell command that runs SQL read from standard input against the server database: `mysql peq` on
akk-stack, or a `docker compose exec -T db ...` line in a Docker setup. Each module SQL file runs once; the database
records it in a `module_sql` table, so running `sql` again only applies new files. `--out <file>` writes every file into
one script instead, for a first install by hand.

## What install changes

1. **Hooks.** Four one-line includes, added once, each marked `eqemu-modules hook`:

   | File | Hook | Where |
   |---|---|---|
   | `zone/CMakeLists.txt` | `include(modules.cmake)` | before `add_library(gm_commands_zone ...)` |
   | `common/ruletypes.h` | `#include "modules_rules.h"` | inside the `Custom` rule category on NMS; after the last category on stock EQEmu, which has no `Custom` category |
   | `zone/command.h` | `#include "modules_commands.h"` | after `command_zone` |
   | `zone/command.cpp` | `#include "modules_commands.inc"` | in `command_init`, before `command_add("zone", ...)` |

2. **Generated files.** Built from every installed module's `module.json` and `rules.h`:

   | File | Holds |
   |---|---|
   | `zone/modules.cmake` | the modules' new source files, added to `zone_sources`, `zone_headers` and `gm_command_sources` |
   | `common/modules_rules.h` | the modules' rules, all in the `Custom` category, so rule names are `Custom:<Name>` on both bases |
   | `zone/modules_commands.h`, `zone/modules_commands.inc` | GM command declarations and `command_add` lines |
   | `common/modules.h` | `#define EQMOD_<MODULE> 1` for each installed module, for code that works with or without another module |
   | `modules.lock.json` | the base, this repository's version, and every file and patch each module installed |

   Shared lists (rules, commands, build sources) are generated rather than patched, because many modules add to the
   same lists and their patches would collide.

3. **Module files and patches**, module by module, requirements first: new files are copied in (install stops if one
   already exists), then the module's patches are applied with `git apply`. If a patch does not apply, install stops
   and names it.

## Module format

```
modules/<name>/
  module.json
  rules.h                  rules for the Custom category (optional)
  files/server/...         new files for the server source, on every base
  files/quests/...         new quest files, on every base
  sql/*.sql                database changes, on every base
  eqemu/                   stock EQEmu only: files/, patches/server/, patches/quests/, sql/
  nms/                     NMS only: the same folders
  README.md                what the module does, its rules and commands, and how to turn it off
```

`module.json`:

```json
{
	"name": "example",
	"title": "Example module",
	"description": "One or two sentences on what it does.",
	"bases": ["eqemu", "nms"],
	"requires": ["merchant-buckets"],
	"sources": {
		"zone": ["example.cpp"],
		"zone_headers": ["example.h"],
		"gm_commands": ["gm_commands/example.cpp"]
	},
	"commands": [
		{"name": "example", "access": "AccountStatus::Player", "function": "command_example",
		 "description": "Shown in #help"}
	]
}
```

- `bases` lists the bases the module supports. A module can't support a base that one of its requirements doesn't.
- `sources` paths are relative to `zone/`, as in `zone/CMakeLists.txt`. The files themselves go in
  `files/server/zone/...` (or under a base folder).
- Patches are applied in file name order, so name them `0001-...patch`, `0002-...patch`. Their paths are relative to the
  server source folder (`a/zone/client.h`), or to the quests folder for `patches/quests/`.
- SQL files run in file name order across the module's shared and base folders; name them by date as the server's own
  migrations are (`2026_11_09_01_...sql`). Write them so a second run does no harm where possible (`INSERT IGNORE`,
  `CREATE TABLE IF NOT EXISTS`), because `--out` scripts can be run by hand more than once.
- Rules in `rules.h` are plain `RULE_INT(Custom, ...)` lines. A rule in another category (for example a new `Pets`
  rule) goes in a patch instead.

## Checks

```
python tools/modules.py check
python tools/modules.py test --repo <git repo> --ref <base commit> --base nms --server-subdir Release-NMS-Server --quests-subdir Release-NMS-Quests
python tools/modules.py test --repo <EQEmu git repo> --ref <EQEmu commit> --base eqemu
```

`check` validates every `module.json`: required fields, known bases and requirements, no requirement loops, source files
present, command access levels. `test` makes a scratch worktree of the base commit, installs each module on its own and
then all of them together, and removes the worktree. Set `EQMOD_MODULES_DIR` to add module folders, as the tests do with
`tools/tests/modules` (an example module that uses every part of the format).

`test` checks that everything installs. Compiling is a separate step: configure the installed tree with CMake and
build `zone`, or compile just the files install touched.

## Developer tools

`tools/dev/extract_patch.py` cuts one module's lines out of a combined change (for example the Voidforged history) into
a patch against the base. Give it the head line ranges that belong to the module; `docs/inventory/core_blocks.csv`
lists them.
