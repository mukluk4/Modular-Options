#include "../client.h"

void command_eqmodexample(Client *c, const Seperator *sep)
{
	c->Message(Chat::White, RuleB(Custom, EqmodExampleEnabled) ? "Example module: on" : "Example module: off");
}
