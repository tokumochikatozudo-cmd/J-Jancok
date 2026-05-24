# J.A.R.V.I.S - Just A Rather Very Intelligent System

> "Sometimes you gotta run before you can walk." - Tony Stark

Open.Jarvis is a Windows-first open-source desktop AI assistant inspired by Iron Man's JARVIS. It combines voice and text commands, local-first command routing, optional Groq cloud fallback, desktop automation, memory controls, plugin safety, provider fallback safety, diagnostics, release checks, and a cinematic cyber-style UI.

Open.Jarvis is designed to run in a keyless degraded mode. Local rules, the desktop UI, memory helpers, health checks, provider routing, and many system commands can work without API keys. Groq, Spotify, Gemini, and other cloud-backed capabilities are optional integrations.

---

## Version Status

Latest published release:

| Version | Focus |
| --- | --- |
| `v0.8.1` | Provider fallback safety hardening |
| `v0.8.0` | Provider system and AI fallback control |
| `v0.7.0` | Memory privacy and data control |

`v0.8.0` introduced the local-first provider system and explicit AI fallback controls. `v0.8.1` hardens that provider layer by improving provider boundary safety, Groq client initialization handling, weekly Groq evaluation safety, and safe provider error handling.

The GitHub Releases page is the source of truth for published release artifacts. The `main` branch may document features that are already merged but not yet included in a formal GitHub Release.

---

## Project Status

| Area | Status |
| --- | --- |
| Primary platform | Windows 10 / Windows 11 |
| Language | Python |
| Main interface | Cyber-style desktop UI |
| Command modes | Voice and text |
| Default AI posture | Local-first / free-first |
| Local provider | Enabled by default |
| Cloud fallback | Optional and disabled unless explicitly enabled |
| Groq provider | Optional cloud provider |
| Music control | Optional Spotify integration |
| Memory | Local memory with privacy controls |
| Safety | Destructive actions blocked by default |
| License | MIT |

---

## Features

### Assistant Runtime

- Wake-word flow with `Jarvis`
- Text command input through the desktop UI
- Local-first command routing before optional AI fallback
- Rule parsing plus optional provider-backed AI fallback
- Runtime states for `BOOTING`, `STANDBY`, `LISTENING`, `PROCESSING`, `EXECUTING`, `SPEAKING`, `ERROR`, and `OFFLINE`
- Structured command stream events for UI and diagnostics
- Live system status with time, CPU, memory, latency, uptime, AI status, permission mode, and posture

### Provider System

- Local-first provider routing
- Deterministic local provider for keyless behavior
- Optional Groq provider behind an isolated provider adapter
- Provider request and response models
- Redacted provider representations for safer logs and debugging
- Controlled provider failure responses instead of raw exception leakage
- Safe defaults for local-first operation
- Cloud fallback disabled unless explicitly enabled
- Provider cache and runtime artifacts blocked from release packages

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
- Local memory controls for viewing, listing, deleting, clearing, and exporting data
- Privacy-aware provider memory context path

### Integrations

- Optional Groq cloud AI fallback
- Optional Spotify playback controls
- Optional Gemini key reserved for future vision and multimodal workflows
- Optional local/offline provider planning
- Model catalog verification helpers

### Security And Release Quality

- Permission profiles and destructive-action safety gates
- Safe URL handling
- Plugin manifests, permissions, trust state, signature verification, lifecycle hooks, and sandbox helpers
- Provider boundary hardening
- Safe handling for Groq client initialization failures
- Weekly Groq evaluation safety hardening
- Health checker
- Project audit
- Repository hygiene checker
- Public release readiness checker
- Public source safety scanner
- Evaluation suite
- UI smoke tests
- Screenshot regression checks
- Release signing helpers
- Source-release hygiene tooling

---

## Planned Or Experimental Features

These items are documented roadmap work. They may have planning helpers or configuration placeholders, but they are not guaranteed production-ready flows yet.

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

---

## Screenshots

Screenshots should be stored under `docs/assets/`.

Recommended images:

| Screenshot | Purpose |
| --- | --- |
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
+-- agents/                          Reserved for future agent implementations
+-- core/                            Reserved core package area
+-- docs/                            Architecture, threat model, plugin security, offline STT, and release docs
+-- evals/                           Evaluation support area
+-- open_jarvis/                     Main source package
|   +-- app/                         Package entry point for terminal mode
|   +-- audio/                       Voice state, wake word, push-to-talk, microphone diagnostics, TTS queue, STT/TTS helpers
|   +-- commands/                    Local router, Groq compatibility wrappers, action schema, dispatcher
|   |   `-- domains/                 Runtime, media, and memory action handlers
|   +-- config/                      Settings manager and non-secret configuration
|   +-- evaluation/                  Evaluation suite, runner, artifacts, measurements, and benchmarks
|   +-- health/                      Health center, observability, and feature quality
|   +-- integrations/                Legacy integration helpers, provider health, offline profile, model installer, URL safety
|   +-- memory/                      Memory modules, privacy mode, user profiles, compatibility re-exports
|   +-- plugins/                     Manifest, permissions, context, registry, loader, plugin helpers
|   +-- providers/                   Local-first AI provider system, Groq adapter, provider router
|   +-- release/                     Repo hygiene, project audit, release build, maintenance
|   +-- runtime/                     Runtime loop, wake listener, timers, orchestration, UI bridge, personality
|   +-- security/                    Admin helpers, release security, public release policy helpers
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

Generated runtime output such as `logs/`, `exports/`, `memory.json`, caches, provider caches, build output, and release bundles should not be committed.

Portable Windows packaging is prepared through a dry-run-capable workflow. See `docs/WINDOWS_PORTABLE.md` for user guidance and `docs/BUILD_WINDOWS.md` for build and verification steps. Full installer support is future work.

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
python -m pip install speechrecognition edge-tts pygame psutil requests groq spotipy pyautogui pyperclip customtkinter python-dotenv vosk schedule
python -m pip install pyaudio
```

If `pyaudio` fails on your machine, install it through a compatible Windows wheel or your preferred package method.

### Check Installation

```powershell
python kontrol.py --no-pause
```

---

## Setup

### 1. Groq API Key Optional

- Go to [Groq Console](https://console.groq.com)
- Create an API key
- Copy your key

Groq is optional. Without it, Open.Jarvis keeps local rule-based commands and the local provider path available.

### 2. Gemini API Key Optional

- Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
- Create an API key
- Copy your key

Gemini is optional and currently reserved for future vision and multimodal workflows.

### 3. Spotify API Optional

- Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
- Create an app
- Add this redirect URI:

```text
http://127.0.0.1:8888/callback
```

- Copy your `Client ID` and `Client Secret`

Spotify is optional. Without it, Spotify commands return a clear disabled-mode message and the rest of the assistant continues.

### 4. Create Your `.env` File

Copy `.env.example` to `.env`:

```powershell
Copy-Item .env.example .env
```

Then fill only the integrations you want:

```env
GROQ_API_KEY=
JARVIS_ENABLE_GROQ=false
JARVIS_GROQ_MODEL=llama-3.1-8b-instant
JARVIS_AI_MODE=auto

GEMINI_API_KEY=

SPOTIFY_CLIENT_ID=
SPOTIFY_CLIENT_SECRET=
SPOTIFY_REDIRECT_URI=
JARVIS_ENABLE_SPOTIFY=false
```

Important:

- Never share your real `.env`
- Never push your real `.env` to GitHub
- Only commit `.env.example`
- Rotate any key that was ever exposed publicly

---

## Provider Defaults

Open.Jarvis uses safe local-first defaults.

```text
ai.local_provider_enabled = true
ai.cloud_fallback_enabled = false
ai.groq_enabled = false
ai.cloud_provider = none
```

By default:

- Local handling is preferred first.
- Cloud fallback is off unless explicitly enabled.
- Groq is off unless explicitly enabled.
- Missing Groq API keys return controlled unavailable/local-only behavior instead of crashing.
- Provider errors are returned as controlled failures instead of raw exceptions.

Provider runtime and cache artifacts must not be committed or shipped in release bundles:

```text
provider_cache/
provider_state/
.provider*
groq_cache/
```

---

## Running

### Desktop UI

```powershell
python arayuz.py
```

### Terminal Mode

```powershell
python -m open_jarvis.app.main
```

### Backward-Compatible Terminal Launcher

```powershell
python jarvis.py
```

### Weekly Update Script

```powershell
python haftalik_guncelleme.py
```

### Health Checker

```powershell
python kontrol.py --no-pause
```

### Windows Portable Build Dry Run

```powershell
python scripts/build_windows_portable.py --version v0.5.0 --dry-run
```

### Portable Artifact Verification

```powershell
python scripts/verify_release_artifact.py path\to\Open.Jarvis-v0.5.0-windows-portable
```

### Project Audit

```powershell
python project_audit.py
```

### Repository Hygiene Check

```powershell
python repo_hygiene.py --include-secrets
```

### Public Release Readiness

```powershell
python public_release.py
```

### Public Source Safety Scan

```powershell
python scripts/public_release_check.py
```

### Full Test Suite

```powershell
python -m pytest
```

### Unittest Runner

```powershell
python -m unittest discover -s tests -v
```

### UI Smoke Test

```powershell
python ui_smoke.py
```

### UI Screenshot Regression

```powershell
python ui_screenshot_regression.py
```

### Lint

```powershell
python -m ruff check .
```

---

## Voice Commands

### Activation

Say `Jarvis` to wake the assistant. After the command completes, it returns to standby mode.

Voice is optional. If wake-word mode or the microphone is unavailable, the UI and text/local command paths remain usable. Push-to-talk is the intended fallback path for systems where always-listening wake-word mode is disabled.

### Applications

| Say | Action |
| --- | --- |
| `open browser` | Opens your preferred browser if mapped by the runtime |
| `open google chrome` | Opens Chrome |
| `open edge` | Opens Edge if mapped by the runtime |
| `open spotify` | Opens Spotify |
| `open vscode` | Opens VS Code |
| `open calculator` | Opens Calculator |
| `open notepad` | Opens Notepad |
| `open task manager` | Opens Task Manager |

### Web And Browser

| Say | Action |
| --- | --- |
| `open youtube` | Opens YouTube |
| `open github` | Opens GitHub |
| `open google` | Opens Google |
| `search for openai api` | Opens Google search results |
| `google python speech recognition` | Opens Google search results |
| `go to example.com` | Opens a normalized HTTPS URL |

### System Info

| Say | Action |
| --- | --- |
| `what time is it` | Reads the current time |
| `what day is it` | Reads the current date |
| `show ram usage` | Reads RAM usage |
| `show cpu usage` | Reads CPU usage |
| `show battery` | Reads battery status |

### Desktop Control

| Say | Action |
| --- | --- |
| `take a screenshot` | Saves a screenshot |
| `read clipboard` | Reads clipboard text |
| `summarize clipboard` | Summarizes copied text with provider or local fallback |
| `minimize all` | Shows desktop |
| `maximize window` | Maximizes the active window |
| `close window` | Closes the active window |
| `volume up` | Raises volume |
| `volume down` | Lowers volume |
| `mute volume` | Toggles mute |
| `lock screen` | Requires permission before locking Windows |
| `shutdown` | Blocked unless destructive actions are explicitly allowed |

### Memory

| Say | Action |
| --- | --- |
| `favorite app is chrome` | Saves app preference when preference detection matches |
| `note buy milk` | Saves a note |
| `remember buy milk` | Saves a note |
| `read notes` | Reads saved notes |
| `my habits` | Reads most used commands |
| `memory stats` | Reads memory stats |
| `memory health` | Reads memory health |
| `memory summary` | Reads a memory summary |
| `daily summary` | Builds a daily assistant summary |
| `prune memory` | Runs safe memory cleanup |

### Spotify Optional

| Say | Action |
| --- | --- |
| `play music` | Starts playback when Spotify is configured |
| `pause music` | Pauses playback |
| `next track` | Skips to the next track |
| `previous track` | Returns to the previous track |
| `play lofi beats on spotify` | Searches and plays a track |
| `what is playing on spotify` | Reads current playback |

### Exit

| Say | Action |
| --- | --- |
| `goodbye jarvis` | Personal farewell and shutdown |
| `shut down jarvis` | Stops the assistant runtime |

---

## Safety

Dangerous actions are blocked unless explicitly allowed.

This includes:

- Shutdown
- Restart
- Sleep
- Lock screen
- Unsafe URLs
- Risky plugin entrypoints
- Destructive desktop actions
- Risky input automation

Safety controls include:

- `JARVIS_ALLOW_DESTRUCTIVE_ACTIONS=false` by default
- `JARVIS_PERMISSION_PROFILE=normal` by default
- shell-free process helpers with guard rails for destructive executables, shell execution flags, and pipe-to-shell command patterns
- URL normalization that only allows HTTP and HTTPS browser links
- Plugin path traversal checks
- Plugin signature verification
- Provider boundary safety
- Privacy mode for sensitive sessions
- Secret masking before runtime event logs are written
- Path safety helpers for scoped file operations and private runtime path detection

Jarvis uses confirmation and permission controls where the action policy requires it.

---

## Keyless And Degraded Mode

Open.Jarvis is designed to start without optional credentials.

| Missing item | Behavior |
| --- | --- |
| `.env` | Startup continues with defaults |
| `GROQ_API_KEY` | Groq cloud routing is disabled; local rule commands and local provider behavior still work |
| `JARVIS_ENABLE_GROQ=false` | Groq cloud routing is disabled even if a key is present |
| `ai.cloud_fallback_enabled=false` | Cloud fallback is disabled even if cloud credentials exist |
| `ai.local_provider_enabled=true` | Local provider behavior remains available |
| `SPOTIFY_CLIENT_ID` / `SPOTIFY_CLIENT_SECRET` | Spotify actions are disabled with an actionable message |
| `JARVIS_ENABLE_SPOTIFY=false` | Spotify actions are disabled even if credentials are present |
| `GEMINI_API_KEY` | Future Gemini-backed flows stay unavailable |
| Microphone | UI and non-voice flows can still load; voice input reports an error state |
| Audio mixer | Voice output is disabled with a warning instead of crashing |

---

## Health And Quality

Current project quality checks include:

- Automated health checker
- Runtime service validation
- Startup degraded-mode reporting for missing Groq, Spotify, microphone, and STT mode
- Provider fallback safety tests
- Deterministic and measured eval coverage
- Unit tests
- Ruff linting
- Static project audit
- Repository hygiene scanning
- Public source secret and personal-data scanning
- Public release readiness scanning
- Memory and action history tracking
- Release signing smoke checks
- Signed model catalog verification
- Feature quality reporting
- UI smoke and screenshot regression checks

Run the current validation suite before each release:

```powershell
python -m ruff check .
python -m pytest
python scripts/public_release_check.py
python repo_hygiene.py --include-secrets
python project_audit.py
```

Optional UI and release checks:

```powershell
python ui_smoke.py
python ui_screenshot_regression.py
python public_release.py
python feature_quality.py
```

Current verified v0.9.0 hardening baseline:

| Check | Current result |
| --- | --- |
| Unit tests | `384 passed` after v0.9.0 hardening |
| Ruff | `All checks passed` |
| Project audit | `No static findings detected` |
| Repository hygiene | `PUBLIC RELEASE HYGIENE: PASS` after cleanup |
| Public source release check | `PUBLIC SOURCE RELEASE CHECK: PASS` |
| Public release readiness | `Ready: yes` |
| UI smoke | `UI smoke: ok` |
| UI screenshot regression | `dashboard`, `system`, `integrations`, and `security` passed |
| Health status | No critical blockers in keyless mode, with expected warnings |

Expected warnings in a fresh keyless setup:

- Groq API key not configured
- Spotify credentials missing
- Optional release signing key missing
- Microphone calibration not completed
- Onboarding not completed

---

## Product Feature Inventory

| Feature | Status | Main files | Current gap or improvement |
| --- | --- | --- | --- |
| Wake word and runtime loop | Implemented | `jarvis_runtime.py`, `runtime/wake_word.py`, `runtime/wake_listener.py` | Add richer wake-word engines and live calibration UX |
| Speech recognition | Implemented | `speech_backend.py` | Improve offline quality with faster-whisper or guided Vosk profiles |
| Voice output | Implemented | `ses_motoru.py`, `tts_provider.py` | Add fully local Piper installer and voice preview UI |
| Startup degraded mode | Implemented | `runtime/readiness.py`, `jarvis_runtime.py` | Add UI repair buttons for each warning |
| Local command router | Implemented | `commands/local_intent_router.py` | Add fuzzy matching and more app/site aliases |
| Provider system | Implemented | `providers/base.py`, `providers/local.py`, `providers/groq.py`, `providers/router.py` | Add more provider adapters and richer provider telemetry |
| Groq provider | Implemented optional | `providers/groq.py`, compatibility wrappers | Keep Groq isolated behind provider boundaries |
| Provider safety hardening | Implemented | `providers/router.py`, Groq provider tests, weekly update tests | Continue adding regression cases for unsafe provider errors |
| Action schema validation | Implemented | `commands/action_schema.py`, `commands/action_dispatcher.py` | Add per-action parameter schemas |
| Desktop automation | Implemented | `commands/domains/runtime_actions.py` | Add confirmation UX for risky input automation |
| Clipboard summarization | Implemented | `runtime_actions.py`, provider routing | Improve local summarizer quality |
| Memory notes and habits | Implemented | `memory.py`, `memory_*.py` | Move from JSON to SQLite and semantic search |
| Daily summary | Implemented | `commands/domains/memory_actions.py` | Include calendar/tasks after those modules exist |
| Spotify controls | Implemented optional | `commands/domains/media_actions.py` | Improve token refresh guidance and UI status |
| Timers | Implemented | `runtime/timer.py` | Add persisted reminders |
| UI cockpit | Implemented | `arayuz.py`, `ui_*.py` | Expand screenshot regression coverage as pages evolve |
| Health center | Implemented | `health_center.py`, `kontrol.py`, `ui_dialogs.py` | Add setup validation repair coverage |
| Runtime observability | Implemented | `observability.py`, `runtime/ui_bridge.py` | Add structured dashboards and log rotation |
| Live UI state bridge | Implemented | `runtime/ui_bridge.py`, `ui_state.py`, `komutlar.py`, `ses_motoru.py` | Add richer per-module state transitions |
| Plugin security | Implemented core | `manifest.py`, `permissions.py`, `context.py`, `registry.py`, `loader.py`, `plugin_runner.py` | Add stronger OS-level isolation |
| Plugin marketplace UI | Implemented core | `plugin_marketplace.py`, `ui_plugin_marketplace.py` | Add remote signed catalog support |
| Eval suite | Implemented | `evaluation_suite.py`, `eval_runner.py`, `eval_measurements.py` | Add more real voice and safety fixtures |
| Release artifacts | Implemented | `release_build.py`, `release_security.py` | Add installer packaging and release notes |
| Offline profile | Implemented planning | `offline_profile.py`, `model_installer.py` | Add guided downloads and extraction |
| Vision analysis | Planned | future `vision/` package | Add screenshot OCR and Gemini/local fallback |
| Tasks and reminders | Planned | future `task_manager.py` | Add persistent task/reminder storage |
| Local calendar | Planned | future `calendar_manager.py` | Add local schedule model and command routing |
| Email drafts | Planned | future mail helper | Add safe draft-only creation |
| Developer agents | Planned | future `agents/` modules | Add explicit sandbox, tests, and approval flow |

---

## Product Feature Modules

These modules are intentionally small, testable, and reusable from the desktop app.

| Capability | Module | What it adds |
| --- | --- | --- |
| Onboarding checks | `onboarding_engine.py` | Groq, Spotify, Gemini, and microphone setup status |
| Settings manager | `config/` | Non-secret configuration and local settings precedence |
| Permission profiles | `permission_profiles.py` | Safe, normal, and admin action policy matrix |
| Provider request model | `providers/base.py` | Shared provider request, response, and error boundaries |
| Local provider | `providers/local.py` | Keyless deterministic local-first behavior |
| Groq provider | `providers/groq.py` | Optional cloud provider behind a testable adapter |
| Provider router | `providers/router.py` | Local-first routing, optional fallback, and controlled provider failure handling |
| Memory panel data | `memory_panel.py` | User-visible memory snapshot, preference update, and note deletion |
| Security overview | `security_center.py` | Permission profile, privacy mode, masked secret status, and confirmation-required action summary |
| Command history and undo | `command_history.py` | Recent command list with optional undo callbacks |
| Plugin marketplace | `plugin_marketplace.py` | Local plugin manifest scan, trust status, permission risk, signature status, and enablement state |
| Local LLM fallback | `llm_fallback.py` | AI mode, provider selection, provider result shape, and offline/rules fallback |
| Workflow mode | `workflow_engine.py` | Multi-step task plans with rollback notes |
| Health center | `health_center.py` | Prioritized health cards, fix commands, safe dry-run/apply repairs, and repair audit events |
| Maintenance mode | `maintenance.py` | Safe memory, log, and cache cleanup recommendations |
| Repository hygiene | `repo_hygiene.py` | Detects local secrets, caches, logs, exports, build output, and executables before publishing |
| Public release readiness | `public_release.py` | Combines required docs, local hygiene, quality commands, and signing readiness into one release gate |
| Public source safety scan | `scripts/public_release_check.py` | Scans source-release files for secrets, tokens, private paths, private memory, logs, and cache artifacts |
| User profiles | `user_profiles.py` | Isolated settings and memory skeleton per user |
| Command suggestions | `command_suggestions.py` | Context-aware discoverability suggestions |
| TTS provider selection | `tts_provider.py` | Edge, Piper, and ElevenLabs provider metadata and environment selection |
| Plugin sandbox execution | `plugin_runner.py` | Trusted plugin execution in scoped temp workspaces with timeout and cleanup |
| Plugin signature verification | `plugin_signature.py` | Deterministic manifest signing and verification |
| Plugin enablement state | `plugin_state.py` | Enable/disable state, approval audit events, and `build_plugin_state_audit` |
| Offline profile | `offline_profile.py` | Local STT, TTS, and LLM readiness planning |
| Assistant eval suite | `evaluation_suite.py` | Intent, safety, latency, and STT release-gate scenarios |
| Eval measurements | `eval_measurements.py` | Command-router decisions, STT fixtures, and measured latency |
| Eval runner | `eval_runner.py` | Deterministic or measured release-gate execution |
| Eval artifact reports | `eval_artifacts.py` | JSON/Markdown release evidence and `compare_eval_artifacts` |
| Windows release artifact pipeline | `release_build.py` | PyInstaller build plan, SHA256 computation, signed manifest generation, and verification |
| Signed model catalog | `model_installer.py` | `build_signed_model_catalog`, `verify_model_catalog`, and `verify_model_checksum` |
| Voice calibration | `voice_calibration.py` | Microphone threshold recommendations from ambient samples |
| Performance benchmarks | `performance_benchmarks.py` | Budget comparison for startup, routing, and health checks |
| Release panel | `release_panel.py` | Signing readiness checks for CI and local release |
| Privacy mode | `privacy_mode.py` | Ephemeral session flags and secret masking |
| User-friendly errors | `error_messages.py` | Standard reason and next-step error messages |
| E2E readiness | `e2e_readiness.py` | Desktop-critical journey checklist for future automation |
| Feature quality registry | `feature_quality.py` | Core feature inventory with tests, performance budgets, and security notes |
| Cyber Hologram UI theme | `ui_theme.py` | Shared design tokens for the main window, dialogs, onboarding, and plugin views |
| UI components | `ui_components.py` | Reusable section, metric, info, status, and cockpit button components |
| UI smoke validation | `ui_smoke.py` | Builds the desktop shell without starting the assistant runtime thread |
| UI screenshot regression | `ui_screenshot_regression.py` | Captures key cockpit pages and verifies nonblank HUD visuals |

Feature quality CLI:

```powershell
python feature_quality.py
```

---

## Difficulty Roadmap

| Difficulty | Work item | Why it belongs here | Target files | Acceptance criteria |
| --- | --- | --- | --- | --- |
| Easy | Expand local English command phrases | Uses existing router and action payloads | `commands/local_intent_router.py` | More common commands bypass cloud providers and pass tests |
| Easy | Add README screenshots | Documentation-only | `README.md`, `docs/assets/` | GitHub page shows the UI clearly |
| Easy | Add command examples to tests | Pure test coverage | `tests/` | New examples pass without cloud calls |
| Easy | Add more health copy for optional integrations | Existing health model | `kontrol.py`, `health_center.py` | Warnings are clearer for new users |
| Medium | Add per-action parameter schemas | Shared validation design required | `commands/action_schema.py` | Invalid params are rejected before execution |
| Medium | Add provider health probes | Needs timeout/error handling | `providers/`, `integrations/provider_health.py` | UI can show provider reachable/unreachable |
| Medium | Add persisted reminders | Requires storage and runtime wakeups | future `task_manager.py`, `runtime/` | Reminders survive restart |
| Medium | Add screenshot OCR | Needs dependency and fallback design | future `vision/`, `runtime_actions.py` | Text can be extracted locally from screenshots |
| Medium | Add setup validation repair coverage | Uses existing safe fix allowlist | `ui_dialogs.py`, `health_center.py`, `jarvis_admin.py` | Local setup state can be validated without editing credentials |
| Hard | SQLite memory migration | Data compatibility and migration risk | `memory_store.py`, `memory_*.py` | Existing JSON memory migrates safely |
| Hard | Semantic recall | Embeddings, privacy, ranking, and storage | future vector layer, `memory_*.py` | Memory search works offline with tests |
| Hard | Local LLM adapter expansion | Endpoint differences and timeout behavior | `providers/`, future provider adapters | Ollama/LM Studio can route commands safely |
| Hard | Real vision assistant | Multimodal design and privacy concerns | future `vision/` package | Screen analysis works with local fallback |
| Hard | Developer agents | High safety and sandbox complexity | `agents/`, `plugin_runner.py` | Coding/debugging agents run with approvals and tests |
| Hard | Strong plugin isolation | OS-level process/network isolation required | `plugin_runner.py` | Third-party plugins have constrained execution |

---

## Current Next Roadmap

| Priority | Item | Difficulty | Status | Next step |
| --- | --- | --- | --- | --- |
| 1 | Provider fallback safety hardening | Medium | Complete in `v0.8.1` | Keep adding provider boundary regression tests |
| 2 | Provider health probes | Medium | Planned | Add timeout-based Groq/local endpoint checks |
| 3 | README screenshots | Easy | Not started | Add UI screenshots under `docs/assets/` |
| 4 | Per-action schema validation | Medium | Partial | Add parameter schemas for each action |
| 5 | Persisted reminders | Medium | Planned | Add task/reminder storage module |
| 6 | SQLite memory migration | Hard | Planned | Design migration and rollback path |
| 7 | Local LLM adapter expansion | Hard | Planned | Add provider interface support for Ollama/LM Studio test doubles |
| 8 | OCR and screen analysis | Hard | Planned | Add local OCR package and screenshot pipeline |
| 9 | Developer agents | Hard | Planned | Design agent sandbox and approval model |
| 10 | Installer-grade packaging | Hard | Planned | Move from portable ZIP preparation toward installer UX |

---

## Easy Roadmap Complete

| Item | Status | Evidence |
| --- | --- | --- |
| Security policy | Complete | `SECURITY.md` |
| Contribution guide | Complete | `CONTRIBUTING.md` |
| Issue templates | Complete | `.github/ISSUE_TEMPLATE/` |
| README comparison | Complete | `Compared With Other Jarvis Projects` |
| Health fix commands | Complete | Health reports include explicit fix commands |
| Feature quality dashboard | Complete | `python feature_quality.py` |
| Free-first local routing | Complete | `commands/local_intent_router.py` |
| Provider system | Complete | `open_jarvis/providers/` |
| Provider fallback safety | Complete | `v0.8.1` release scope |
| Known limitations action plan | Complete | `Current Next Roadmap` |

---

## Compared With Other Jarvis Projects

Open.Jarvis is strongest in free-first desktop automation, local command routing, conservative safety gates, provider fallback safety, test coverage, health checks, release artifacts, and quality tracking. Larger assistant projects may be stronger in packaged distribution, cloud-scale integrations, community plugin ecosystems, and mature agent frameworks.

| Area | Open.Jarvis status | Gap before public maturity |
| --- | --- | --- |
| Safety | Destructive actions blocked by default, plugin signatures, sandbox helpers, and provider boundary hardening exist | Add stronger per-action confirmation UX |
| Quality | Unit tests, Ruff, audit, health check, eval artifacts, and screenshot regression exist | Add a larger eval set |
| Extensibility | Plugin trust, marketplace core, and plugin runner exist | Add remote signed plugin catalogs |
| Offline | Vosk fallback, local provider, and offline profile planning exist | Add guided local STT/TTS/LLM installers |
| UX | Custom UI, onboarding, settings, runtime logs, health center, memory center | Add screenshots, guided calibration, and release installer |
| Agentic work | Workflow planning helpers exist | Add real developer agents with explicit sandbox and approvals |

---

## Settings Reference

Open.Jarvis includes a central configuration manager for non-secret preferences. Existing `.env` and environment variables remain supported for compatibility, especially for optional integration secrets.

Configuration precedence is:

1. Built-in safe defaults
2. Environment variables and legacy `.env` values
3. User-local `settings.json` for non-secret settings
4. Explicit Settings UI saves

Source mode stores non-secret settings in the current user's local app data. Portable mode saves non-secret settings to `config/settings.json` in the extracted portable copy.

Real `settings.json` files are private user data and must not be committed or shipped in release ZIPs.

Secrets remain environment-only. The Settings UI shows only masked status for API keys, OAuth secrets, tokens, release signing keys, and plugin signing keys. Open.Jarvis does not claim encrypted vault storage or cloud sync.

### Memory Privacy And Data Control

Open.Jarvis local memory privacy controls build on the settings system. When `privacy.privacy_mode` is enabled or `privacy.memory_enabled` is disabled in non-secret settings, normal note, habit, and detected-preference collection does not add new persistent memory writes.

Explicit user-directed data controls remain available so existing local memory can be viewed, listed, deleted, cleared, or exported.

Memory exports are masked JSON snapshots intended for a user-selected private path. They mask secret-like assignments and sensitive preference keys, but notes and habits can still be personal data.

Do not commit exports, `memory.json`, `config/settings.json`, logs, provider caches, or other private runtime files.

| Setting | Purpose | Safe default |
| --- | --- | --- |
| `JARVIS_AI_MODE` | AI routing mode: `auto`, `free_cloud`, `offline`, or `rules` | `auto` |
| `JARVIS_ENABLE_GROQ` | Explicitly enable optional Groq cloud routing | `false` in `.env.example` |
| `JARVIS_GROQ_MODEL` | Groq model used for routing and summarization | `llama-3.1-8b-instant` |
| `JARVIS_VOICE_ENABLED` | Enable optional voice UX controller behavior | `true` |
| `JARVIS_WAKE_WORD` | Wake word used to activate the assistant | `jarvis` |
| `JARVIS_WAKE_WORD_ENABLED` | Enable always-listening wake-word mode when voice is available | `true` |
| `JARVIS_WAKE_WORD_COOLDOWN_SECONDS` | Minimum seconds between wake-word detections | `1.0` |
| `JARVIS_PUSH_TO_TALK_ENABLED` | Keep push-to-talk fallback available when supported by UI/runtime callers | `true` |
| `JARVIS_ACTIVE_TIMEOUT` | Seconds before returning to standby | `60` |
| `JARVIS_ACTION_SEQUENCE_DELAY` | Delay between multi-action workflow steps | `0.1` |
| `JARVIS_APP_LAUNCH_DELAY` | Short pause after launching apps | `0.2` |
| `JARVIS_CPU_SAMPLE_INTERVAL` | CPU usage sample duration for faster checks | `0.1` |
| `JARVIS_SCREENSHOT_DELAY` | Stabilization pause before screenshots | `0.2` |
| `JARVIS_SLEEP_ACTION_DELAY` | Delay before sending sleep command | `1.0` |
| `JARVIS_TYPE_DELAY` | Delay before automatic typing starts | `0.1` |
| `JARVIS_ENERGY_THRESHOLD` | Microphone sensitivity | `300` |
| `JARVIS_PAUSE_THRESHOLD` | Pause length for command segmentation | `1.0` |
| `JARVIS_TTS_ENABLED` | Enable optional spoken responses | `true` |
| `JARVIS_TTS_PROVIDER` | Voice output provider selector | `edge` |
| `JARVIS_ALLOW_DESTRUCTIVE_ACTIONS` | Permit shutdown, restart, sleep, and lock actions | `false` |
| `JARVIS_PERMISSION_PROFILE` | Permission profile for runtime actions | `normal` |
| `JARVIS_PRIVACY_MODE` | Disable memory writes and tighten masking for sensitive sessions | `false` |
| `JARVIS_OFFLINE_STT` | Enable offline speech recognition fallback | `1` |
| `JARVIS_VOSK_MODEL_PATH` | Path to a local Vosk model | Empty |
| `JARVIS_LOCAL_LLM_URL` | Optional local LLM endpoint | Empty |
| `JARVIS_RELEASE_SIGNING_KEY` | HMAC signing key for release verification | Empty |
| `JARVIS_PLUGIN_SIGNING_KEY` | HMAC signing key for local plugin signing | Empty |
| `JARVIS_PLUGIN_SIGNING_KEYS` | Optional signer-to-key JSON for multiple plugin signers | Empty |
| `GROQ_API_KEY` | Optional AI command routing and summarization key | Empty |
| `JARVIS_ENABLE_SPOTIFY` | Explicitly enable optional Spotify controls | `false` in `.env.example` |
| `SPOTIFY_CLIENT_ID` | Optional Spotify API client ID | Empty |
| `SPOTIFY_CLIENT_SECRET` | Optional Spotify API client secret | Empty |
| `SPOTIFY_REDIRECT_URI` | Spotify callback URI | `http://127.0.0.1:8888/callback` |
| `GEMINI_API_KEY` | Optional future Gemini integration | Empty |

---

## Notes

- Open.Jarvis works without Spotify credentials; only Spotify features stay unavailable.
- Open.Jarvis works without Groq credentials for local-rule commands and local provider behavior.
- Groq/cloud fallback stays disabled unless explicitly enabled.
- Gemini is optional and currently reserved for future vision workflows.
- Desktop automation is Windows-first.
- Voice quality depends on microphone hardware and room noise.
- Logs are written to `logs/jarvis.log`.
- Runtime events are written to `logs/runtime_events.jsonl`.
- Provider runtime caches and state directories must stay out of source control and release bundles.
- Offline STT details live in `docs/OFFLINE_STT.md`.
- Plugin development details live in `docs/PLUGIN_DEVELOPMENT.md`.
- Plugin security details live in `docs/PLUGIN_SECURITY.md`.
- Release signing details live in `docs/RELEASE_SIGNING.md`.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
