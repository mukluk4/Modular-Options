-- Vault Resonance (vault-resonance module): the one buff that carries every stat-only vault clicky.
-- No effects of its own: the server applies the folded clickies' bonuses (zone/nms_vault.cpp).
-- Folding stays off until this row exists (Custom:VaultResonanceSpell 44690), so apply it together with the
-- client line in client/spells_us_vault_resonance.txt (see the module README),
-- then restart: spells load at server start.
-- Copied from Koadic's Expansive Mind (2970) for its icon 11; permanent, self, can't be dispelled or clicked off.

START TRANSACTION;

DELETE FROM spells_new WHERE id = 44690;
CREATE TEMPORARY TABLE vr SELECT * FROM spells_new WHERE id = 2970;
UPDATE vr SET id = 44690, name = 'Vault Resonance',
	effectid1 = 254, effect_base_value1 = 0, effect_limit_value1 = 0, max1 = 0, formula1 = 100,
	effectid2 = 254, effect_base_value2 = 0, effect_limit_value2 = 0, max2 = 0, formula2 = 100,
	effectid3 = 254, effect_base_value3 = 0, effect_limit_value3 = 0, max3 = 0, formula3 = 100,
	effectid4 = 254, effect_base_value4 = 0, effect_limit_value4 = 0, max4 = 0, formula4 = 100,
	effectid5 = 254, effect_base_value5 = 0, effect_limit_value5 = 0, max5 = 0, formula5 = 100,
	effectid6 = 254, effect_base_value6 = 0, effect_limit_value6 = 0, max6 = 0, formula6 = 100,
	effectid7 = 254, effect_base_value7 = 0, effect_limit_value7 = 0, max7 = 0, formula7 = 100,
	effectid8 = 254, effect_base_value8 = 0, effect_limit_value8 = 0, max8 = 0, formula8 = 100,
	effectid9 = 254, effect_base_value9 = 0, effect_limit_value9 = 0, max9 = 0, formula9 = 100,
	effectid10 = 254, effect_base_value10 = 0, effect_limit_value10 = 0, max10 = 0, formula10 = 100,
	effectid11 = 254, effect_base_value11 = 0, effect_limit_value11 = 0, max11 = 0, formula11 = 100,
	effectid12 = 254, effect_base_value12 = 0, effect_limit_value12 = 0, max12 = 0, formula12 = 100,
	new_icon = 11, targettype = 6, goodEffect = 1, buffduration = 9999, buffdurationformula = 50,
	short_buff_box = 0, nodispell = 1, field232 = 1, mana = 0, cast_time = 0, recast_time = 0,
	recovery_time = 0, RecourseLink = 0, descnum = 0, effectdescnum = 0, numhits = 0, numhitstype = 0,
	you_cast = '', other_casts = '', cast_on_you = 'Your vault resonates within you.',
	cast_on_other = '', spell_fades = 'Your vault falls silent.',
	classes1 = 255, classes2 = 255, classes3 = 255, classes4 = 255, classes5 = 255, classes6 = 255,
	classes7 = 255, classes8 = 255, classes9 = 255, classes10 = 255, classes11 = 255, classes12 = 255,
	classes13 = 255, classes14 = 255, classes15 = 255, classes16 = 255;
INSERT INTO spells_new SELECT * FROM vr;
DROP TEMPORARY TABLE vr;

COMMIT;
