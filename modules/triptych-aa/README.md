# AA and archery fixes

A set of AA and ranged combat changes, several ported from the Triptych server.

## AA damage stacking (from Triptych)

Stock code takes only the single highest AA for each spell focus and for SPA 294 (critical spell damage). With these
rules every AA line adds up instead, under a cap.

| Rule | Default | What it does |
|---|---|---|
| `Custom:AAFocusEffectsStack` | true | AA focus effects (spell damage, crit damage and the like) sum across AA lines |
| `Custom:AACritDmgNoStackComponentsStack` | true | Every AA's SPA 294 critical damage part sums, instead of the highest one counting |
| `Custom:DoTCritsShareNoStackPool` | true | DoT critical hits also get that summed SPA 294 pool |
| `Custom:MaxAACritDmgFocus` | 500 | Cap in percent on the summed AA damage focus and on the SPA 294 pool; 0 for no cap |

Turn the three switches off for stock behaviour.

## Combat

- Ranger and Rogue innate critical hits on every skill (stock: Rangers on Archery, Rogues on Throwing).
- Throwing gets the archery hit bonuses, and Headshot works on thrown weapons as well as arrows.
- A critical hit never does less than a normal hit (the crit modifier is at least 100%).
- Beastlord Warder Form (Bestial Alignment, spells 30738 and 16443) gives each target the warder model for its own race
  from `pets_beastlord_data`, falling back to the stock wolf.
- A character owning more AA ranks than the player profile holds is cut off at the limit with an error in the log,
  instead of writing past the end of the AA array.

## NMS only

- Destruction, Frantic Infusion and Cataclysm can be bought (NMS made them grant-only with multiclassing on).
- Fury of Magic past rank 5 stays pure-caster only at every rank, not only up to rank 4751.
- Directional AA cones with no target fire from the caster instead of being refused.
- Kick, Bash and other skill attacks keep their base damage with `Character:ItemExtraSkillDamageCalcAsPercent` (NMS
  dropped it; stock EQEmu already has this).
- Throwing damage halving checks Berserker with `HasClass`, so multiclass Berserkers skip it.

## Commands and database

None.

## Credits

AA stacking from Triptych. Written for Voidforged.
