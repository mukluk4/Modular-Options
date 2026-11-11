-- Every item is usable at any level: required and recommended levels cleared. On Voidforged this cleared 84,263
-- required levels (66,077 of them above 65) and 60,614 recommended levels. Item data loads through shared memory:
-- restart the server after applying. There is no undo in this file; back up the items table first if you may want
-- the old values back.
UPDATE items SET reqlevel = 0 WHERE reqlevel <> 0;
UPDATE items SET reclevel = 0 WHERE reclevel <> 0;
