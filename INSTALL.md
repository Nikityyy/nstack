# Install or update nstack for a T3 Code user

1. Identify the T3 environment running the user's agents. Use T3's project and environment tools when available. Reuse the nstack checkout if this machine already has one. Otherwise clone `https://github.com/Nikityyy/nstack.git` to a stable directory on that machine. For updates, run `git pull --ff-only` from the checkout. Preserve any local edits and report a pull conflict or divergence.
2. Discover the enabled provider instances in that environment's **Settings → Providers** or its local server configuration. Read only provider names, enablement, and the fields needed to resolve their profile paths. Prefer configured homes and environment overrides to defaults. Some providers share a home across accounts. Install once per distinct destination. A client connected to another machine uses that machine's checkout and profiles.
3. Run `scripts/install.py` with Python 3.10 or newer and the resolved destinations. Use `--codex HOME` for a Codex home and `--claude HOME` for a Claude config directory. Repeat the flags for separate homes. Use the common home for Codex shadow accounts. These flags link the skills into each home's `skills` folder and add a reference to the current shared working rules in its global instructions.
4. Use `--skills-dir DIR` and, when appropriate, `--rules-file FILE` for another provider. The table gives common paths to verify. For an ACP wrapper, confirm the installed agent's supported paths or skill commands. The T3 environment's provider list identifies the wrapper. Follow its own installation rules.
5. Confirm the installed links point to the one shared checkout. Verify skill discovery per distinct profile using the T3 `$` picker or the provider's native discovery. Check that the configured instructions point to `rules/nstack.md`. For running sessions, use **Restart agent session** when appropriate or tell the user which session needs it. Report accounts that passed discovery and any you could only check on disk. Remove prior global guidance only when the user asked for a replacement, after verifying its successor in the same profile.

| Provider | Common skill directory | Global instructions |
| --- | --- | --- |
| Codex | `~/.codex/skills` or the configured Codex home's `skills` directory | `AGENTS.md` in the effective Codex home |
| Claude Code | `~/.claude/skills` or the configured Claude profile's `skills` directory | `CLAUDE.md` in the effective Claude config directory |
| Antigravity | `~/.gemini/config/skills` | Check the active Antigravity global rules file |
| Mistral Vibe | `~/.vibe/skills` or `$VIBE_HOME/skills` | `AGENTS.md` in the effective Vibe home |
| Cursor | `~/.cursor/skills` | Use the provider's global rules settings |
| Grok Build | `~/.grok/skills` | Check the configured global instructions |
| OpenCode | `~/.config/opencode/skills` | Check the configured global instructions |
| Pi | `~/.pi/agent/skills` | Check the effective Pi agent directory |

Rerun the installer after the checkout adds, renames, or removes a skill, or when the user adds an account. Existing skill files and the referenced working rules update through the shared checkout. When requested, enable **Automatically pull** for the nstack T3 project. It updates a clean default-branch checkout.

[T3 provider setup](https://github.com/pingdotgg/t3code/blob/v0.1.11/docs/user/install.md) · [T3 skill discovery and refresh](https://github.com/pingdotgg/t3code/blob/v0.1.11/docs/user/composer.md#commands-and-skills) · [Mistral Vibe skill discovery](https://github.com/mistralai/mistral-vibe/blob/main/README.md#skill-discovery)
