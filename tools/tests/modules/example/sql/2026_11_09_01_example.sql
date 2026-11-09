-- Example module: a rule row so the server and database agree
INSERT IGNORE INTO rule_values (ruleset_id, rule_name, rule_value, notes) VALUES (1, 'Custom:EqmodExampleEnabled', 'true', 'Example module test rule');
