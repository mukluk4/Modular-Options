# Drakkin in Freeport

The NMS release has no Drakkin character creation rows. This adds them, starting in Freeport (never Crescent Reach):

- Classes and deities match Humans. Each class and deity starts where a Human of it starts in Freeport; for deities
  a Human starts elsewhere, the class's usual Freeport spot is used. Rangers and Druids (no Human Freeport start)
  start at West Freeport's safe point with the West Freeport bind.
- Stats are the Drakkin base plus the class bonus, with the Human default point spend.
- Every item a Human can use becomes usable by Drakkin too (race bit 32768).

No zone access changes: NMS already has every expansion enabled.

## Applying

World reads creation data at startup and items load through shared memory, so restart the whole server after the SQL.
The SQL clears Drakkin's rows (race 522) and point allocations 109-121 first, so it can be run again; check that your
database doesn't use those allocation IDs.

## Bases

NMS only. Stock PEQ already has Drakkin, starting in Crescent Reach.

## Credits

Written for Voidforged.
