# Excess pet power

Pet power (from pet focus items and AAs) picks a row in the `pets` table for the pet type. Once the focus is stronger
than the strongest row, stock code gives the pet nothing more. With this module the power past that row scales the
row's pet the same way a `-1` (scaled) row does, counting only the excess:

- hit points and armor class × (1 + excess / 100)
- damage and size × (1 + excess / 200), size at most three times normal
- one level, plus one per 25 excess, up to `Pets:PetPowerLevelCap` levels

So a pet focus with power 75 on a pet type whose strongest row is 50 gives that row's pet 25% more hit points and
armor class and 12.5% more damage.

## Rules

| Rule | Default | What it does |
|---|---|---|
| `Pets:ScaleExcessPetPower` | true | Turn the excess scaling on or off |

The rule is in the `Pets` category, beside the stock pet rules.

## Database and commands

None.

## Bases

Stock EQEmu and NMS. Stock EQEmu caps the extra levels at 10 (`Pets:PetPowerLevelCap`); NMS sets 99.

## Credits

Written for Voidforged.
