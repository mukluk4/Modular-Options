-- Open #zone, #mystats and #find zone (#fz, #findzone) to every player. Players still need the key a zone's locked
-- entrance asks for, and always land at the safe spot (see the module's #zone change). Zones load command access at
-- boot (or #reload commands).
UPDATE `command_settings` SET `access` = 0 WHERE `command` IN ('zone', 'mystats');
UPDATE `command_subsettings` SET `access_level` = 0 WHERE `parent_command` = 'find' AND `sub_command` = 'zone';
