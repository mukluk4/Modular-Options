-- The Void on the Bazaar map ("Attune the Map", NMS Waypoints), under the Special tab. It lands where the rift
-- portal returns players. Like every waypoint it's greyed out until the character unlocks it; this module's
-- global_player.pl patch unlocks it for accounts with Plane of Time access.
INSERT INTO nms_waypoints (shortname, long_name, category, x, y, z, heading)
SELECT 'thevoida', 'The Void', 8, 25.33, 78.03, 1.21, 241.75 FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM nms_waypoints WHERE shortname = 'thevoida');
