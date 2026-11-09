#include "../common/modules.h"
#include "../common/rulesys.h"
#include "../common/skill_caps.h"
#include "client.h"

// Highest cap for a skill at a level among the character's classes (all of them when multiclassing on NMS)
uint16 Client::GetHighestClassSkillCap(EQ::skills::SkillType skill, uint8 level)
{
#ifdef EQMOD_BASE_NMS
	const uint32 classes_bits = RuleB(Custom, MulticlassingEnabled) ? GetClassesBits() : (1u << (GetClass() - 1));

	uint16 cap = 0;
	for (uint8 class_id = 1; class_id <= Class::PLAYER_CLASS_COUNT; ++class_id) {
		if (classes_bits & (1u << (class_id - 1))) {
			cap = std::max<uint16>(cap, SkillCaps::Instance()->GetSkillCap(class_id, skill, level).cap);
		}
	}

	return cap;
#else
	return SkillCaps::Instance()->GetSkillCap(GetClass(), skill, level).cap;
#endif
}

// Level-up and login: skills (not tradeskills) to their caps for the current level, plus every spell and
// discipline the character's classes have up to it. Only raises / adds, so it's quiet once caught up.
void Client::AutoLearnForLevel()
{
	const uint8 level = GetLevel();

	if (RuleB(Custom, AutoTrainSkills)) {
		int trained = 0;
		for (const auto &s : EQ::skills::GetSkillTypeMap()) {
			if (EQ::skills::IsTradeskill(s.first)) {
				continue;
			}

			uint16 cap = GetHighestClassSkillCap(s.first, level);
			if (EQ::skills::IsSpecializedSkill(s.first)) {
				// What a guildmaster would train; going past it is still earned by casting
				cap = std::min<uint16>(cap, RuleI(Skills, MaxTrainSpecializations));
			}

			if (GetRawSkill(s.first) < cap) {
				SetSkill(s.first, cap);
				trained++;
			}
		}

		if (trained) {
			Message(Chat::White, fmt::format("Your skills have been trained to their limits for level {}.", level).c_str());
		}
	}

	if (RuleB(Custom, AutoScribeSpells)) {
		ScribeSpells(1, level);
	}

	if (RuleB(Custom, AutoLearnDisciplines)) {
		LearnDisciplines(1, level);
	}
}
