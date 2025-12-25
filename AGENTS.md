# AGENTS.md — AUTOBAYT

## Coding Style
- Keep code **simple, explicit, and easy to follow**.
- Avoid clever tricks, shortcuts, or **over-engineered patterns**.
- Follow Python's best practices and conventions.
- Prefer readability over compactness; clarity is more important than fewer lines.

## Scope of Changes
- Only modify the **files and sections I explicitly request**.
- Do **not** introduce features, refactors, or logic I did not ask for.
- Do not alter or “improve” working code outside the requested scope.
- When I ask for a change, focus only on that change and leave the rest untouched.

## Behavior
- Ask for clarification if instructions are not clear.
- Do not invent or weave in logic that has not been requested.
- Provide short, focused responses without unnecessary extra explanations.
- If multiple options exist, briefly list them and let me decide.

## Safety & Restrictions
- Never add, expose, or modify secrets, credentials, or sensitive settings.
- Do not change database configuration, migrations, or environment files unless I ask.
- Do not run optimization on queries or restructure models without explicit request.

## Testing & Documentation
- Provide tests only if I specifically request them.
- Do not enforce test coverage or CI/CD rules unless asked.
- Keep inline comments short and useful; avoid clutter.

## Don’ts
- Don’t rename variables, functions, or classes unless explicitly instructed.
- Don’t reformat unrelated files when editing one file.
- Don’t restructure templates, static assets, or app layout without my approval.
- Don’t suggest major architectural changes unless I directly ask for advice.


## git
**URL** https://github.com/RASBR/home-assistant-autobayt.git

## SUMMARY
- Keep it simple
- Stay within scope
- Don’t overthink or auto-refactor
- Ask before assuming

## References - Agent Instructions
- See [000-coding-conventions.md](docs/agent/000-coding-conventions.md) for style guidelines.
- See [040-api-usage.md](docs/agent/040-api-usage.md) for external API rules.
- See [050-api-response-samples.md](docs/agent/050-api-response-samples.md) for response sample.

## References — Project Documentation

- [000-project-info.md](docs/project/000-project-info.md) → General project overview and purpose.
- [010-architecture.md](docs/project/010-architecture.md) → System architecture and main components.
- [020-setup.md](docs/project/020-setup.md) → Installation, configuration, and local development setup.
- [040-roadmap.md](docs/project/040-roadmap.md) → Planned features, priorities, and future directions.
- [050-devices.md](docs/project/050-devices.md) → Device list and their availability status.
- [051-api-response-mapping.md](docs/project/051-api-response-mapping.md) → API endpoint definitions and field descriptions.
- [052-entities.md](docs/project/052-entities.md) → JSON field to entity mapping and categorization.
- [080-icon-logo-setup.md](docs/project/080-icon-logo-setup.md) → Icon and logo configuration.

---
