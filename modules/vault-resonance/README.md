# Vault Resonance

The Nautilus Vault (`vault` module) keeps clicky buffs up while their items sit in the vault's clicky slots, one buff
slot per clicky. With this module, every clicky whose spell only changes stats shares a single buff, **Vault
Resonance**, so a full clicky page no longer fills the buff window.

- A clicky folds in when every effect of its spell is a plain stat: hit points, mana and endurance (and their regen),
  armor class, attack, the base stats, resists, haste, damage shield, crit chances, accuracy, avoidance, mitigation,
  strikethrough and damage modifiers. Anything else (movement, see invisible, illusions, runes, procs, focus effects,
  songs, limited-hit buffs) keeps its own buff as before.
- Only the strongest copy of each stat counts. Folded spells are checked against each other and against your real
  buffs with the stock stacking rules, exactly as if each were its own buff: a stronger real buff wins, and a weaker
  buff cast on you doesn't take hold.
- Casting one of the folded spells on yourself still works: it lands as a normal timed buff, and the vault's copy
  steps aside until it wears off, then quietly takes over again.
- Vault Resonance can't be dispelled or clicked off. It comes back after a death, and goes away when nothing folds.
- The class and level gates of the vault still apply: a clicky the character can't use doesn't fold.

Vault Resonance has no effects of its own, so the client's buff window shows no stats for it. The folded clickies'
bonuses are applied by the server and show in the stats the client is sent.

## Client

The buff needs spell 44690 in the client's `spells_us.txt` (and in your patcher, if you have one): append the line in
`client/spells_us_vault_resonance.txt`. It is a copy of Koadic's Expansive Mind (2970) for the glowing-eyes icon, with
no effects and no description.

## Rules

| Rule | Default | What it does |
|---|---|---|
| `Custom:VaultResonance` | true | Turns folding on. False: one buff per clicky, as without the module. |
| `Custom:VaultResonanceSpell` | 44690 | The Vault Resonance spell. Folding stays off until this spell exists in `spells_new`. |

## Database

Spell 44690, Vault Resonance (`sql/2026_11_22_01_vault_resonance.sql`). It deletes that ID first, so it can be run
again; check that your database doesn't already use it. Restart after applying it: spells load at server start.

## Bases

Stock EQEmu and NMS. The two differ only in spell effect names (`SE_*` on NMS, `SpellEffect::` on stock EQEmu), which
`nms_vault.cpp` handles with one macro, and in the include style of `spells.cpp` (separate patches).

## Credits

Voidforged.
