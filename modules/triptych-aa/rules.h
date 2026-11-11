// AA spell damage stacking. Ported from Triptych.
RULE_BOOL(Custom, AAFocusEffectsStack, true, "AA focus effects (damage, crit damage, etc.) sum additively across all AA lines instead of using only the highest single source")
RULE_BOOL(Custom, AACritDmgNoStackComponentsStack, true, "AA SPA 294 critical spell damage components sum additively across all AA lines instead of using only the highest single source")
RULE_BOOL(Custom, DoTCritsShareNoStackPool, true, "DoT critical damage ratio also receives the capped AA critical damage pool from SPA 294")
RULE_INT(Custom, MaxAACritDmgFocus, 500, "Maximum combined AA critical damage focus value in percent from stacked AA sources, 0 to disable cap")
