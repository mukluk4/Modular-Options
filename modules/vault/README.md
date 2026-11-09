# Nautilus Vault

A per-character item vault. Each character gets a Nautilus Vault key (item 9011009) on zone-in; right-clicking it
opens the vault window. The vault holds:

- **Storage pages**, including bags: a vaulted bag keeps its contents.
- **A bank and a merchant** that open from the vault, anywhere.
- **The Proc Locker** (slot 82, and 83 for ranged): the item there, and its augments, proc beside the weapon in your
  hand.
- **Mod slots** (84-87): items there lend their skill mods, instrument mods and focus effects, never stats or procs.
- **Clicky slots** (61-80): clicky buffs from items there are kept up while the item stays in the vault. Invisibility,
  Divine Aura and disciplines are skipped so they never interrupt you.

Items keep their full state through the vault: attunement, ornaments, augments, custom data (such as dynamic item
seeds) and their unique ID.

## Client

The vault window is drawn by the NMS client add-on (`dinput8.dll`). Without it, players can't see or use the vault, so
the module ships off: turn it on only when your players have the add-on.

## Rules

| Rule | Default | What it does |
|---|---|---|
| `Custom:NautilusVault` | false | Turns the vault on: the key item, the commands and the combat hooks. |
| `Custom:ProcLockerStacks` | true | The Proc Locker item procs on its own rolls beside your weapon and its augments. False: the locker item replaces your weapon's proc instead. |
| `Custom:ProcLockerModSlots` | true | Mod slots 84-87 lend their effects. |

## Commands

The client add-on sends these; players don't type them. All are Player level: `#vault_page`, `#vault_deposit`,
`#vault_withdraw`, `#vault_bank`, `#vault_merchant`, `#vault_deposit_bagitem_specific`, `#vault_withdraw_bagitem`.

## Database

- `character_nms_vault`: the vault contents. An older vault table from the original NMS vault port is brought up to
  date.
- Item 9011009, the vault key.

To remove the module, empty the vaults first: items left in `character_nms_vault` are not returned to anyone.

## Bases

Stock EQEmu and NMS. The two bases differ only in the core hooks (separate patches) and one spell effect name, which
`nms_vault.cpp` handles with `#ifdef SE_DivineAura`.

On NMS, the Proc Locker honours `Custom:MultipleTwoHandedProcs` (an NMS rule) for its augment procs. Voidforged also
capped pet proc rates there; that cap is left out because the locker only works for players, never pets.

## Credits

Ported from Triptych, which ported it from Rockin-Vik's NMS-Release. Voidforged added the kept clicky buffs, fixes,
and the stock EQEmu port.
