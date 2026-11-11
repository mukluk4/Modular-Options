-- #Echo_of_Sebilis (89139, level 69) out of its Sebilis spawn groups: it killed the level 50 players the zone is for.
-- It only dropped Essence of Old Sebilis for the Cipher of Veeshan, and Veeshan's Peak isn't locked by the Cipher.
-- Saved zone state keeps NPCs that are already up: apply with the server stopped, then clear Sebilis' saved spawns
-- (zone_state_spawns) if the Echo is still standing after a restart.
DELETE FROM spawnentry WHERE npcID = 89139;
