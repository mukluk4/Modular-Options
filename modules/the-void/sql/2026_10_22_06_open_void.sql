-- The Void (thevoida) is GM-only in stock PEQ (min_status 255). Open it to players. On NMS the access gate in
-- global_player.pl (this module's NMS patch) still keeps out accounts without Plane of Time access.
-- To close it again: UPDATE zone SET min_status = 255 WHERE short_name = 'thevoida' AND version = 0;
UPDATE zone SET min_status = 0 WHERE short_name = 'thevoida' AND version = 0 AND min_status = 255;
