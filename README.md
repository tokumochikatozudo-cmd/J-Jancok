# Open.Jarvis

> **A Windows-first, local-first desktop AI assistant for automation, productivity, privacy-aware memory, optional AI fallback, and a cinematic cyber-style interface.**

Open.Jarvis is an open-source desktop assistant inspired by Iron Man's JARVIS. It supports voice and text commands, local command routing, desktop automation, optional Groq cloud fallback, memory privacy controls, plugin safety, provider fallback controls, diagnostics, release checks, and a cyber-style UI.

The project is designed to run in a **keyless degraded mode**. Local rules, the desktop UI, memory helpers, health checks, provider routing, and many system commands can work without API keys. Groq, Spotify, Gemini, and other cloud-backed capabilities are optional integrations.

---

## Version Status

Latest published release:

| Version | Focus |
|---|---|
| `v0.9.0` | Security hardening |
| `v0.8.1` | Provider fallback safety hardening |
| `v0.8.0` | Provider system and AI fallback control |
| `v0.7.0` | Memory privacy and data control |

`v0.9.0` hardens runtime safety, command/process execution, path validation, URL safety, plugin entrypoint boundaries, and release artifact protection before the `v1.0.0` stable release.

The GitHub Releases page is the source of truth for published release artifacts. The `main` branch may document features that are already merged but not yet included in a formal GitHub Release.

---

## Project Status

| Area | Status |
|---|---|
| Primary platform | Windows 10 / Windows 11 |
| Language | Python |
| Main interface | Cyber-style desktop UI |
| Command modes | Voice and text |
| Default AI posture | Local-first / free-first |
| Local provider | Enabled by default |
| Cloud fallback | Optional and disabled unless explicitly enabled |
| Groq provider | Optional cloud provider |
| Spotify | Optional integration |
| Memory | Local memory with privacy controls |
| Security posture | Hardened runtime/release safety checks |
| License | MIT |

---

## Highlights

- Voice and text command input
- Local-first command routing
- Optional Groq AI fallback
- Keyless degraded mode
- Cyber-style desktop UI
- Desktop automation helpers
- Optional Spotify control
- Local memory with privacy controls
- Provider fallback controls
- Plugin permission and boundary checks
- Safe URL handling
- Runtime command/process safety helpers
- Path safety helpers
- Release artifact and hygiene checks
- Public release validation tools
- Automated test coverage for security, release, config, UI, provider, and memory behavior

---

## Features

### Assistant Runtime

- Wake-word flow with `Jarvis`
- Text command input through the desktop UI
- Local-first command routing before optional AI fallback
- Rule parsing plus optional provider-backed AI fallback
- Runtime states for:
  - `BOOTING`
  - `STANDBY`
  - `LISTENING`
  - `PROCESSING`
  - `EXECUTING`
  - `SPEAKING`
  - `ERROR`
  - `OFFLINE`
- Structured command stream events for UI and diagnostics
- Live system status with time, CPU, memory, latency, uptime, AI status, permission mode, and posture

### Provider System

- Local-first provider routing
- Deterministic local provider for keyless behavior
- Optional Groq provider behind an isolated adapter
- Provider request and response models
- Redacted provider representations for safer logs and debugging
- Controlled provider failure responses instead of raw exception leakage
- Cloud fallback disabled unless explicitly enabled
- Groq disabled by default
- Missing Groq API key handled safely
- Provider cache and runtime artifacts blocked from release packages

Default provider posture:

```text
ai.local_provider_enabled = true
ai.cloud_fallback_enabled = false
ai.groq_enabled = false
ai.cloud_provider = none
```

### Desktop Automation

- Browser opening
- Website launching
- Normalized safe URL opening
- Google search
- App launching for common Windows tools and mapped desktop applications
- Screenshot capture
- Clipboard reading and summarization
- Keyboard shortcuts
- Mouse actions
- Scrolling and window control
- Timers and runtime workflow helpers

### Voice And Audio

- Optional microphone-based voice input
- Wake-word activation with `Jarvis`
- British-style voice responses with Edge TTS
- Optional offline STT planning with Vosk fallback support
- Push-to-talk fallback planning for systems where always-listening mode is disabled
- Microphone and audio readiness checks

### Memory And Privacy

- Notes
- Habits
- Preferences
- Short-term context
- Memory health scoring
- Daily assistant summary helpers
- Privacy mode for sensitive sessions
- Secret masking before runtime events are written
- Local memory controls for:
  - viewing memory
  - listing memory
  - deleting notes
  - clearing memory
  - masked JSON export
- Privacy-aware provider memory context path

When privacy mode is enabled or memory is disabled, persisted memory context is prevented from being attached to provider prompts.

### Integrations

- Optional Groq cloud AI fallback
- Optional Spotify playback controls
- Optional Gemini key reserved for future vision and multimodal workflows
- Optional local/offline provider planning
- Model catalog verification helpers

---

## v0.9.0 Security Hardening

`v0.9.0` is focused on public-release security hardening before `v1.0.0`.

### Command And Process Safety

The runtime now uses stricter command/process validation.

The project hardens against unsafe patterns such as:

```text
raw shell-string execution
destructive shell command patterns
encoded PowerShell-style command patterns
curl-pipe-shell style patterns
unsafe command forwarding
```

Normal safe local app/process behavior is preserved.

### File And Path Safety

The project includes file/path safety helpers and expanded hygiene checks for private runtime files and cache/state paths.

Risky/private runtime paths are blocked or detected, including:

```text
.env
settings.json
memory.json
exports/
logs/
provider_cache/
provider_state/
plugin_cache/
plugin_state/
.provider*
.plugin*
groq_cache/
token files
credential files
secret files
API key files
runtime/cache artifacts
```

`.env.example` remains allowed as a safe template file.

### URL Safety

URL handling is restricted to safe web protocols.

Allowed:

```text
http
https
```

Rejected unsafe examples include:

```text
file://
javascript:
data:
powershell:
cmd:
UNC/backslash-style local paths
malformed unsafe URLs
```

### Plugin Safety

Plugin loader boundary validation was hardened so plugin entrypoints are revalidated before import.

This helps prevent unsafe plugin entrypoint path traversal and plugin files escaping the expected plugin directory boundary.

### Provider And Memory Regression Protection

`v0.9.0` preserves earlier provider and memory protections:

```text
cloud fallback disabled by default
Groq disabled by default
local-first provider behavior preserved
missing Groq key handled safely
provider boundary exceptions remain controlled
Groq client factory exceptions remain controlled
raw provider exception text is not exposed
privacy mode strips persisted memory context
memory_enabled=false strips persisted memory context
MemoryControlService admin actions remain available
```

---

## Security And Release Quality

Open.Jarvis includes multiple local quality and release-safety tools:

- Permission profiles and destructive-action safety gates
- Safe URL handling
- Command/process safety helpers
- Path safety helpers
- Plugin manifest and entrypoint checks
- Provider boundary hardening
- Safe Groq client initialization handling
- Weekly Groq evaluation safety hardening
- Health checker
- Project audit
- Repository hygiene checker
- Public release readiness checker
- Public source safety scanner
- Evaluation suite
- UI smoke tests
- Screenshot regression checks
- Source-release hygiene tooling

---

## Planned Or Experimental Features

These items are roadmap or experimental work. They may have planning helpers or configuration placeholders, but they are not guaranteed production-ready flows yet.

- Gemini-backed vision analysis and screen understanding
- OCR with local fallback
- Semantic memory search with local embeddings
- Persistent tasks, reminders, and local calendar scheduling
- Email draft creation
- Research, summarization, and fact-check workflows
- Developer agents for coding, debugging, testing, and improvement reviews
- Rich local LLM adapter for Ollama or LM Studio
- Remote signed plugin catalogs
- Installer-grade Windows release packaging
- Full OS-level sandboxing
- Signed installer support

---

## Screenshots

Screenshots should be stored under `docs/assets/`.

Recommended images:

| Screenshot | Purpose |
|---|---|
| `docs/assets/dashboard.png` | Main cyber cockpit UI |
| `docs/assets/system-status.png` | Live system status and runtime posture |
| `docs/assets/memory-panel.png` | Local memory and privacy controls |
| `docs/assets/security-center.png` | Permission profile, privacy mode, and safety status |
| `docs/assets/plugin-marketplace.png` | Local plugin trust and permission overview |

Do not add image links until the matching files exist. Broken image links make the public README look unfinished.

---

## Project Structure

```text
Open.Jarvis/
+-- .github/                         CI workflow and issue templates
+-- docs/                            Architecture, threat model, plugin security, offline STT, and release docs
+-- open_jarvis/                     Main source package
|   +-- app/                         Package entry point
|   +-- audio/                       Voice state, wake word, microphone diagnostics, TTS/STT helpers
|   +-- commands/                    Local router, Groq compatibility wrappers, action schema, dispatcher
|   |   `-- domains/                 Runtime, media, and memory action handlers
|   +-- config/                      Settings manager and non-secret configuration
|   +-- evaluation/                  Evaluation suite and weekly update helpers
|   +-- health/                      Health center, observability, and feature quality
|   +-- integrations/                Provider health, offline profile, URL safety, integration helpers
|   +-- memory/                      Memory modules, privacy mode, user profiles, compatibility re-exports
|   +-- plugins/                     Manifest, permissions, context, registry, loader, plugin helpers
|   +-- providers/                   Local-first AI provider system, Groq adapter, provider router
|   +-- release/                     Repo hygiene, project audit, release build, artifact policy
|   +-- runtime/                     Runtime loop, wake listener, timers, orchestration, UI bridge
|   +-- security/                    Command safety, path safety, release security helpers
|   +-- ui/                          Desktop UI, theme, components, memory panel, security center
|   `-- utils/                       Health launcher and logging helpers
+-- plugins/                         Reserved for local plugin packages
+-- tests/                           Automated tests
+-- arayuz.py                        Backward-compatible UI launcher
+-- jarvis.py                        Backward-compatible terminal launcher
+-- kontrol.py                       Backward-compatible health checker launcher
+-- repo_hygiene.py                  Backward-compatible hygiene checker launcher
+-- project_audit.py                 Backward-compatible static audit launcher
+-- public_release.py                Backward-compatible release readiness launcher
+-- eval_runner.py                   Backward-compatible eval CLI launcher
+-- release_build.py                 Backward-compatible release build launcher
+-- model_installer.py               Backward-compatible signed model catalog launcher
+-- .env.example                     API key and runtime settings template
+-- .gitignore                       Keeps secrets and generated files out of GitHub
+-- pyproject.toml                   Ruff, mypy, and coverage configuration
+-- requirements.txt                 Runtime dependencies
+-- requirements-dev.txt             Developer, lint, test, and build dependencies
+-- SECURITY.md                      Security policy
+-- CONTRIBUTING.md                  Contribution guide
+-- LICENSE                          MIT License
`-- README.md                        This file
```

Generated runtime output such as `logs/`, `exports/`, `memory.json`, caches, provider/plugin caches, build output, and release bundles should not be committed.

---

## Installation

### Requirements

- Windows 10 or Windows 11
- Python 3.11+
- Optional microphone for voice input
- Optional speakers or audio output for spoken responses
- Optional API keys for Groq, Spotify, or Gemini-backed future workflows

### Recommended Install

```powershell
python -m pip install -r requirements.txt
```

### Developer Install

```powershell
python -m pip install -r requirements.txt
python -m pip install -r requirements-dev.txt
```

### Manual Package Install

```powershell
python -m pip install -e .
```

---

## Configuration

Copy the example environment file if you want optional integrations:

```powershell
copy .env.example .env
```

Keep real credentials in local `.env` only.

Do not commit:

```text
.env
settings.json
memory.json
exports/
logs/
provider_cache/
provider_state/
plugin_cache/
plugin_state/
.provider*
.plugin*
groq_cache/
tokens
credentials
secret files
runtime cache/state
```

Optional integrations may require credentials or local setup, but the core assistant is designed to remain usable without API keys.

---

## Usage

### Terminal Entry Point

```powershell
python jarvis.py
```

### Package Entry Point

```powershell
python -m open_jarvis.app.main
```

### Desktop UI Launcher

```powershell
python arayuz.py
```

### Health Check

```powershell
python kontrol.py
```

### Release Readiness Check

```powershell
python public_release.py
```

### Repository Hygiene

```powershell
python repo_hygiene.py
```

### Project Audit

```powershell
python project_audit.py
```

---

## Validation

Common local validation commands:

```powershell
python scripts/public_release_check.py
python repo_hygiene.py
python project_audit.py
python -m ruff check .
python -m pytest
```

v0.9.0 validation included:

```text
python scripts/public_release_check.py -> PASS
python repo_hygiene.py -> PASS
python -m pytest tests/security -q -> 18 passed, 16 subtests passed
python -m pytest tests/release -q -> 19 passed, 14 subtests passed
python -m pytest tests/test_provider_system.py -q -> 15 passed, 2 warnings
python -m pytest tests/test_memory_privacy_controls.py -q -> 7 passed, 2 warnings
python -m ruff check . -> PASS
python -m pytest -> 384 passed, 2 warnings
python project_audit.py -> no static findings
CLI/help/dry-run smoke -> PASS
secret/runtime scan -> clean after approved hygiene cleanup
```

Known non-blocking warnings:

- `speech_recognition` Python deprecation warnings
- Pygame banner output during help commands
- Local-only Groq warning when no API key is configured

---

## Release Workflow

Typical release flow:

```text
1. Implement feature or fix
2. Run targeted tests
3. Run full quality gates
4. Run hygiene and public release checks
5. Commit locally
6. Run post-commit audit
7. Push main
8. Create and push tag
9. Create GitHub Release manually
10. Verify release title, tag, commit, latest badge, and assets
```

Source releases should not include generated runtime/private artifacts.

GitHub auto-generated source archives are expected. Do not manually upload private builds, logs, `.env`, caches, memory exports, or local config files.

---

## Security Notes

Open.Jarvis can listen to voice commands, open applications, control the desktop, read clipboard text, use API keys, and persist memory. Treat it as a local desktop automation tool with optional cloud integration.

Current safety defaults:

- Destructive runtime actions are blocked unless explicitly allowed.
- Process helpers run with `shell=False`.
- Shell strings and obvious destructive command patterns are rejected by default.
- Browser navigation is limited to `http` and `https`.
- File/path safety helpers reject traversal outside allowed roots.
- Plugin entrypoints are rechecked at load time.
- Unknown/high-risk plugin permissions are deny-by-default.
- Privacy mode can suppress normal memory personalization behavior.
- Cloud fallback is disabled unless explicitly enabled.
- Real credentials should live only in local `.env`.

Out of scope unless future releases explicitly implement them:

- Full OS-level sandboxing
- Kernel isolation
- Encrypted vault storage
- Signed installer guarantees
- Safety for user-modified plugins that bypass trust policy
- Safety when users intentionally disable safety gates

See `SECURITY.md` for the full security policy.

---

## Version History

| Version | Summary |
|---|---|
| `v0.9.0` | Security hardening for runtime, command/process, path, URL, plugin, and release safety |
| `v0.8.1` | Provider fallback safety hardening |
| `v0.8.0` | Local-first provider system and AI fallback control |
| `v0.7.0` | Memory privacy and data control |
| `v0.6.1` | Windows portable build smoke fixes |
| `v0.6.0` | Settings UI and configuration manager |
| `v0.5.0` | Windows portable build workflow |
| `v0.4.0` | Voice UX foundations |
| `v0.3.0` | Plugin improvements |
| `v0.2.1` | Test and CI cleanup |
| `v0.2.0` | Package/layout cleanup |
| `v0.1.0` | Initial public release |

---

## Contributing

Contributions are welcome.

Before opening a pull request:

```powershell
python -m pytest
python -m ruff check .
python repo_hygiene.py
python project_audit.py
python scripts/public_release_check.py
```

Do not include:

- API keys
- OAuth tokens
- `.env`
- runtime logs
- `memory.json`
- `settings.json`
- generated cache/state folders
- private plugin manifests
- release ZIP/EXE artifacts unless explicitly requested for a release workflow

See `CONTRIBUTING.md` for contribution guidance.

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

## Disclaimer

Open.Jarvis is a pre-1.0 desktop assistant project. It is designed for local-first operation and safer defaults, but it is not a full sandbox, not an encrypted vault, and not a signed installer distribution.

Use optional cloud providers only when you understand that prompt text may be sent to the configured provider.
