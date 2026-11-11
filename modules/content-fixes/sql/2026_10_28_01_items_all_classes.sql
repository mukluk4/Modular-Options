-- Items with no classes (0) or the old all-classes mask (32767) become usable by every class (65535). On Voidforged
-- this opened 9,645 items. Item data loads through shared memory: restart the server after applying.
UPDATE items SET classes = 65535 WHERE classes IN (0, 32767);
