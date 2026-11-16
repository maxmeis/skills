# Max’s Agent Skills

[![skills.sh](https://skills.sh/b/maxmeis/skills)](https://www.skills.sh/maxmeis/skills/t3-orchestrator)

Small, reusable skills for Claude Code, Codex, and other coding agents. The collection currently includes:

| Skill | What it does |
| --- | --- |
| [T3 Orchestrator](skills/t3-orchestrator/SKILL.md) | Coordinates T3 sessions, delegated engineering work, stacked pull requests, and resumable handoffs. |

Browse [T3 Orchestrator on skills.sh](https://www.skills.sh/maxmeis/skills/t3-orchestrator).

## Install

Install a skill from this GitHub repository with the [`skills` CLI](https://github.com/vercel-labs/skills/blob/main/docs/commands.md). It requires Node.js 22.20 or later.

### From this local checkout

Install from the root directory of this checkout:

```sh
pnpm dlx skills add . --skill t3-orchestrator -g -a claude-code
pnpm dlx skills add . --skill t3-orchestrator -g -a codex
```

To install it for both agents in one command:

```sh
pnpm dlx skills add . --skill t3-orchestrator -g -a claude-code codex
```

### From GitHub

Install from `maxmeis/skills` globally for either agent:

```sh
pnpm dlx skills add maxmeis/skills --skill t3-orchestrator -g -a claude-code
pnpm dlx skills add maxmeis/skills --skill t3-orchestrator -g -a codex
```

Or install for both at once:

```sh
pnpm dlx skills add maxmeis/skills --skill t3-orchestrator -g -a claude-code codex
```

Skills.sh discovers skills from GitHub repositories; users install with `skills add`, and aggregate install telemetry can make skills appear in its directory automatically. There is no separate submission step, and directory listing may take time. See the [skills.sh FAQ](https://www.skills.sh/docs/faq).

## Use

In Claude Code, invoke the skill with `/t3-orchestrator`. In Codex, invoke it with `$t3-orchestrator`. For example:

```text
Coordinate this task with delegated agents and stacked PRs.
```

T3 orchestration tools must be connected in the current session. Start a fresh agent session if the newly installed skill is not yet available.

To see skills available from this repository, run `pnpm dlx skills add . --list`. Update installed skills with `pnpm dlx skills update -g`.

## Add a skill

Create each skill under `skills/<skill-name>/SKILL.md`. Include `name` and `description` in its YAML frontmatter, then add any supporting files inside that skill's folder. The [skills.sh creation guide](https://github.com/vercel-labs/skills/blob/main/docs/creating-skills.md) describes repository discovery and the required format.
