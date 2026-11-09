-- Nautilus Vault storage. Item state is kept per slot, so a round trip returns the same item: attuned, ornaments,
-- custom_data (dynamic item seeds) and guid. The ALTERs bring an older vault table (from the original NMS vault
-- port) up to date; on a new table they do nothing.
CREATE TABLE IF NOT EXISTS character_nms_vault (
    character_id INT UNSIGNED NOT NULL,
    slot INT NOT NULL,
    bag_slot INT NOT NULL DEFAULT 0,
    item_id INT UNSIGNED NOT NULL,
    charges SMALLINT NOT NULL DEFAULT 1,
    aug1 INT UNSIGNED NOT NULL DEFAULT 0,
    aug2 INT UNSIGNED NOT NULL DEFAULT 0,
    aug3 INT UNSIGNED NOT NULL DEFAULT 0,
    aug4 INT UNSIGNED NOT NULL DEFAULT 0,
    aug5 INT UNSIGNED NOT NULL DEFAULT 0,
    aug6 INT UNSIGNED NOT NULL DEFAULT 0,
    instnodrop TINYINT UNSIGNED NOT NULL DEFAULT 0,
    custom_data TEXT DEFAULT NULL,
    ornament_icon INT UNSIGNED NOT NULL DEFAULT 0,
    ornament_idfile INT UNSIGNED NOT NULL DEFAULT 0,
    ornament_hero_model INT UNSIGNED NOT NULL DEFAULT 0,
    guid BIGINT UNSIGNED NOT NULL DEFAULT 0,
    PRIMARY KEY (character_id, slot, bag_slot),
    KEY idx_character_nms_vault_slot (character_id, slot)
);

ALTER TABLE character_nms_vault
    ADD COLUMN IF NOT EXISTS instnodrop TINYINT UNSIGNED NOT NULL DEFAULT 0 AFTER aug6,
    ADD COLUMN IF NOT EXISTS custom_data TEXT DEFAULT NULL AFTER instnodrop,
    ADD COLUMN IF NOT EXISTS ornament_icon INT UNSIGNED NOT NULL DEFAULT 0 AFTER custom_data,
    ADD COLUMN IF NOT EXISTS ornament_idfile INT UNSIGNED NOT NULL DEFAULT 0 AFTER ornament_icon,
    ADD COLUMN IF NOT EXISTS ornament_hero_model INT UNSIGNED NOT NULL DEFAULT 0 AFTER ornament_idfile,
    ADD COLUMN IF NOT EXISTS guid BIGINT UNSIGNED NOT NULL DEFAULT 0 AFTER ornament_hero_model;
