# Multiclass disciplines

NMS stores every multiclass character with Bard as its base class. `Client::GetLearnableDisciplines` checked a
discipline's level for the base class only, so a multiclass character was offered Bard disciplines and none from its
other classes. With this module the check goes through every class the character has: a discipline is learnable when
any of them gets it within the level range asked for.

That covers discipline trainers and tomes, and learning disciplines on level-up (`Custom:AutoLearnDisciplines` in the
`qol` module).

## Rules, commands and database

None.

## Bases

NMS only. Stock EQEmu has no multiclassing, and its single-class check is already right.

## Credits

Written for Voidforged.
