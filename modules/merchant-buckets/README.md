# Merchant bucket gates

A `merchantlist` row with `bucket_name` and `bucket_value` set only shows, and only sells, once the character's own data
bucket passes `bucket_comparison` against `bucket_value`. Rows without a bucket are not affected.

Stock EQEmu and NMS already check buckets when a regular merchant lists its items. This module moves that check into
one function and adds it where it was missing:

- alternate currency merchants, when they list their items
- alternate currency purchases, so a hidden item can't be bought by ID

Other modules use it to unlock vendor items as players progress. Rift tier gear and ranger arrows, for example, unlock
by the deepest rift a character has cleared (`bucket_name` `rift_deepest`, comparison 2).

## Example

```sql
-- Sell item 942900 for 15 of the merchant's currency once the character's rift_deepest bucket is at least 75
INSERT INTO merchantlist (merchantid, slot, item, alt_currency_cost, bucket_name, bucket_value, bucket_comparison)
VALUES (1200044, 144, 942900, 15, 'rift_deepest', '75', 2);
```

`bucket_comparison` takes the server's `ComparisonType` numbers (`common/emu_constants.h`): 0 equal, 1 not equal,
2 greater or equal, 3 lesser or equal, 4 greater, 5 lesser, and so on.

## Bases

Stock EQEmu and NMS. No rules, commands or database changes.
