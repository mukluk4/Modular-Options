-- Platinum economy: remove the Echo of Memory currency (alternate currency 6, item 46779).
-- Rerunnable. Needs a world and zone restart for the rules and the merchant.

-- Echoes stop dropping, and character slot and set unlocks at login are free (they cost Echoes).
-- Written for every rule set, since the stock rule defaults (200, 5 and 5) would otherwise apply.
INSERT INTO `rule_values` (`ruleset_id`, `rule_name`, `rule_value`, `notes`)
SELECT s.`ruleset_id`, r.`rule_name`, '0', 'platinum-economy: Echo of Memory removed'
FROM `rule_sets` s
JOIN (SELECT 'Custom:EventEOMDropChance' AS `rule_name`
      UNION ALL SELECT 'Custom:EoMUnlockCharacterSetCost'
      UNION ALL SELECT 'Custom:EoMUnlockCharacterSlotCost') r
ON DUPLICATE KEY UPDATE `rule_value` = '0';

-- The Echo of Memory merchant in the Bazaar becomes the Collector of Curios and sells the same goods for platinum:
-- each item is priced at 1,000 platinum per Echo it cost, before the merchant's 5% markup.
UPDATE `items` i
JOIN `merchantlist` m ON m.`item` = i.`id` AND m.`merchantid` = 1000023
SET i.`price` = ROUND(m.`alt_currency_cost` * 1000000 / 1.05)
WHERE m.`alt_currency_cost` > 0;

UPDATE `merchantlist` SET `alt_currency_cost` = 0 WHERE `merchantid` = 1000023;

UPDATE `npc_types`
SET `name` = 'Collector_of_Curios', `lastname` = 'Bags and Curios', `alt_currency_id` = 0
WHERE `id` = 1120001186 AND `alt_currency_id` = 6;

DELETE FROM `alternate_currency` WHERE `id` = 6;
