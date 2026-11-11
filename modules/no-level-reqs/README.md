# No item level requirements

Clears every item's required level (`reqlevel`) and recommended level (`reclevel`), so any character can use any item
it can otherwise equip. On a server with a level cap below the content's, this is what lets high-level gear be worn
at all.

## Applying

Item data loads through shared memory, so restart the server after the SQL. The old levels aren't kept: back up the
`items` table first (`CREATE TABLE items_levels_backup SELECT id, reqlevel, reclevel FROM items;`) if you may want
them back.

## Rules and commands

None.

## Credits

Written for Voidforged.
