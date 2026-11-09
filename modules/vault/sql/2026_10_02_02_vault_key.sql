-- Nautilus Vault key (item 9011009). The zone gives it to every character on zone-in while Custom:NautilusVault is on;
-- right-clicking it opens the vault window of the NMS client add-on. The code only treats ids from 9011009 up as the
-- key, so stock items that share the low digits never count.
-- Every items column has a default, so the row is inserted directly and needs no other item to copy from.
-- clickeffect 1 is a client dummy: the zone catches the click and never casts it. nodrop = 0 is No Drop in this
-- schema, and norent = 1 keeps the key through long camps. Safe to run again: an existing key is updated in place.
INSERT IGNORE INTO items (id, Name) VALUES (9011009, 'Nautilus Vault');
UPDATE items SET
    Name = 'Nautilus Vault',
    lore = 'Your Nautilus Vault. Right-click to open storage, bank, merchant, Proc Locker.',
    icon = 6306, idfile = 'IT64',
    itemclass = 0, itemtype = 33, slots = 0, classes = 65535, races = 65535,
    bagsize = 0, bagslots = 0, bagtype = 0, bagwr = 0, book = 0,
    nodrop = 0, norent = 1, notransfer = 1, fvnodrop = 1, loregroup = -1, magic = 1,
    weight = 1, size = 1, price = 0, sellrate = 0, stackable = 0, potionbelt = 0, attuneable = 0,
    clicktype = 1, clickeffect = 1, clicklevel = 0, clicklevel2 = 0, clickname = 'Open Nautilus Vault',
    casttime = 0, casttime_ = 0, recastdelay = 0, recasttype = 0, maxcharges = -1
WHERE id = 9011009;
