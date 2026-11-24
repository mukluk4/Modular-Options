# Vertical reach

Stock EQEmu measures melee range and proximity aggro on the flat: an NPC on a ledge, or on the floor above, can hit you
or notice you as if you stood beside it. This module adds a height limit to both.

- **Melee.** Melee, AE rampage and the skill attacks that use melee range (kick, bash, backstab and the like) fail when
  the height gap between the two is over `Combat:MeleeZReach` plus the bigger combatant's size, line of sight or not.
- **Aggro.** An NPC doesn't proximity aggro a target whose height gap is over `Aggro:MaxZDiff` plus the bigger one's
  size. `#aggro` explains it ("is on a different level") when this is why.

The gap is measured feet to feet (each model's z offset is taken off), and the size allowance lets large models reach
further. Spells were already measured in three dimensions and are not changed.

Watch for NPCs standing under or over a ledge they can't reach. Tune the rules rather than the code; summoning remains
the NPC's answer to a target it can't reach.

## Rules

Added to the stock `Combat` and `Aggro` categories, so they are not under `Custom`.

| Rule | Default | What it does |
|---|---|---|
| `Combat:MeleeZReach` | 15 | Height allowance for melee, in feet, before size. 0 = off (stock: height ignored). |
| `Aggro:MaxZDiff` | 35 | Height allowance for proximity aggro, in feet, before size. 0 = off (stock: only the aggro radius). |

## Bases

Stock EQEmu and NMS, the same change on both (separate patches, because `ruletypes.h` differs).

## Credits

Voidforged.
