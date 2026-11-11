-- Custom:PermanentServerBuffsEnabled read 'True', and rule booleans are case-sensitive ("true"), so every zone boot
-- took the disabled branch and removed the NMS permanent server buffs.
UPDATE rule_values SET rule_value = 'true' WHERE rule_name = 'Custom:PermanentServerBuffsEnabled' AND BINARY rule_value = 'True';
