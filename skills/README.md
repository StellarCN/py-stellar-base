# Agent Skill for `stellar-sdk`

This directory contains an [Agent Skills](https://agentskills.io/) compatible skill for
developers building Stellar applications in Python with the `stellar-sdk` package.

**Audience: SDK users, not py-stellar-base contributors.** The skill is a portable
artifact that can be installed in another project so coding agents have concise,
Stellar-specific guidance while generating application code.

## Contents

```text
skills/py-stellar-base/
  SKILL.md            # entry point: install, conventions, critical rules, examples
  references/         # topic-specific reference files loaded on demand
```

The skill is self-contained: examples are embedded directly, and external pointers use
absolute URLs such as the SDK documentation and GitHub. It should continue to work after
being copied into a project that does not contain this repository.

## Installation options

| Environment | How to use this skill |
| --- | --- |
| Claude Code plugin | Add this repository as a plugin marketplace and install the `py-stellar-base` plugin. The marketplace manifest lives at `.claude-plugin/marketplace.json`. |
| Claude Code project skill | Copy `skills/py-stellar-base/` into your project at `.claude/skills/py-stellar-base/`. |
| Claude Code personal skill | Copy `skills/py-stellar-base/` into `~/.claude/skills/py-stellar-base/`. |
| Other Agent Skills compatible tools | Copy `skills/py-stellar-base/SKILL.md` and its `references/` directory into the location your tool uses for skills or reusable instructions. |
| Generic coding agents | Point your agent instructions file at `SKILL.md`, or paste the relevant reference file into the agent context. |

For Claude Code's skill and plugin behavior, see the Claude Code documentation for
[skills](https://docs.anthropic.com/en/docs/claude-code/skills) and
[plugin marketplaces](https://docs.anthropic.com/en/docs/claude-code/plugin-marketplaces).

## Discovery and marketplaces

This repository is set up for two broad distribution paths:

- **Claude Code marketplaces:** `.claude-plugin/marketplace.json` describes this repository
  as a Claude Code plugin source.
- **Agent Skills indexes and registries:** public directories or aggregators may discover
  repositories containing `SKILL.md` files. Examples include community indexes such as
  [skillsmp.com](https://skillsmp.com/) and any future Agent Skills compatible catalogs.

Third-party indexes are convenience discovery channels only. They are not required to use
the skill, and their indexing behavior, ranking, and update schedule are outside this
project's control.

## Not shipped via pip

`pip install stellar-sdk` installs the SDK package only. It does **not** install this
skill. Install the skill through a plugin marketplace, by copying this directory, or by
cloning this repository.

## Maintenance

The skill is maintained alongside the SDK so examples and API references can stay in sync.
Keep embedded examples small, explicit, and aligned with the SDK documentation. When SDK
APIs change, review `SKILL.md` and the files under `references/` as part of the same
change.
