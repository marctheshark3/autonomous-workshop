# Autonomous Workshop agent instructions

This file governs coding agents building, reviewing, testing or documenting the
source repository. It is directory-scoped guidance, not a product-run role.
A product run belongs to a separate persistent toy project with its own
materialized `AGENTS.md`, `.agents/skills/autonomous-workshop/` and immutable
`STAGE.json`. Inspecting those files during maintenance grants no product,
publication, manufacturing or credential authority.

## Shared runtime architecture

Workshop is a thin workflow host around a native coding-agent runtime. The
native Manager owns cognitive work and native child-agent routing; the host
owns lifecycle order, durable state, deterministic gates, budgets and authorized
external effects. Codex is the implemented Manager runtime; preserve the same
boundary when working on other adapters.

- `workshop wish` preserves the exact Wish, selected effort and private run
  workspace. `workshop resume` continues the same native session. Stages are
  durable checkpoints, not separate one-shot model sessions or Python agents.
- New runs choose Spark (`Wish -> Make -> Release`), Forge
  (`Wish -> Invent -> Make -> Release`) or Quest
  (`Wish -> Invent -> Make -> Playtest -> Release`). Omitted stages produce no
  turn, artifact or passing evidence; Spark/Forge record Playtest `not-run`.
- New marked Spark runs select the Inventor during setup, then continue into
  Make in the same session. Setup and host-only publication are not creative
  Goals. Each active creative attempt has one Goal whose verifiable stopping
  condition is its stage finalizer; only one Goal is active at once.
- Codex runs freeze the selected model, effort and shared token allowance across
  stages, descendants and resumes; the fixed Component Reviewer role uses `low`.
  For token-budget runs, historical host clocks and turn/retry/lifecycle-round
  spending caps do not apply. Make retains its own frozen checks and review
  allowance. Preserve accounting even when usage is pending.
- Spark accepts Make's existing output without duplicate host CAD verification,
  manual review, native Release turn or a new PDF. Forge/Quest retain their
  contracts. Exact identity, credential isolation and authenticated effect
  reconciliation remain host responsibilities.
- `--no-publish` is frozen: seal/project locally as `unreleased`, with no Factory
  effect, credential read or ledger write. A resume cannot add or drop it.
- Frozen runs retain their materialized protocol and capabilities. A change to
  builder documentation never upgrades them. Apply only explicitly documented,
  host-recorded operator corrections; do not revive retired paths from old ADRs.
- Inventors are declared specialist bundles bound to exact Taste/skill bytes.
  The host materializes official custom agents; native Codex owns spawning and
  synthesis. Only the root Manager receives stage authority and submits a
  proposal. Child agents cannot advance gates or perform external effects.
- Python is trusted substrate for typed contracts, deterministic tools/gates,
  hashes, checkpoints, exclusive mutation locks, budgets, sandbox/session
  boundaries, authorization, idempotency, receipts and reconciliation. Never add
  a second Python agent framework, prompt chain, stage-role worker, model judge,
  browsing/repair strategy or cognitive orchestration compatibility layer.
- External-effect credentials never enter the native agent subprocess. Model
  prose and self-scores are proposals, not passing evidence. Only host-verified
  exact bytes, deterministic checks and reconciled receipts advance a gate.

## Coding agents building this repository

Read the current contract for the area being changed. Use the
[current runtime map](docs/NATIVE_AGENT_RUNTIME.md) to choose the relevant
section, then the owning contract/tool and cited decisions. Do not reconstruct
all historical amendments for an unrelated edit.

| Work | Context to read before changing its contract |
| --- | --- |
| Native runtime, CLI lifecycle, budgets or authenticated effects | [Runtime map](docs/NATIVE_AGENT_RUNTIME.md), [domain vocabulary](CONTEXT.md), then the relevant runtime/workflow owner |
| Component authoring, review, interfaces or contract amendments | [Current Make workflow](src/workshop/make/skills/make-round/SKILL.md), [current runtime policy](docs/NATIVE_AGENT_RUNTIME.md#current-token-budget-and-spark-handoff-policy), then its cited ADRs |
| Product-run instructions or stage proposals | [Product-run constitution](.agents/product-run/AGENTS.md), the [run skill](.agents/product-run/.agents/skills/autonomous-workshop/SKILL.md), and the current stage contract |
| Frozen-run compatibility or an operator correction | The run's materialized inputs and the matching [resume](docs/NATIVE_AGENT_RUNTIME.md#start-and-resume) / [budget policy](docs/NATIVE_AGENT_RUNTIME.md#product-budgets-and-legacy-timeouts); consult only the applicable historical decision |
| Standalone Make harness | [Harness instructions](harness/AGENTS.md), its copied template reference and the CAD tool contract; this workflow has no Workshop host or shop |

The [historical decision chain](docs/agents/runtime-history.md) preserves the
previous amendment narrative and source links for investigations. It is history,
not the operating recipe for a new run. Keep current contracts and tests intact.

## Repository ownership

- `src/cli/`: argument parsing, output formatting and exit codes.
- `src/workshop/runtime/`: native adapters and trusted state/effect boundaries.
- `src/workshop/workflow/`: lifecycle, checkpoints, invalidation, frozen budgets
  and whole-run host composition.
- `src/workshop/<stage>/`: stage-owned public contracts and deterministic tools;
  `src/workshop/make/skills/` owns reusable Make domain skills.
- `.agents/product-run/`: the complete template materialized only into a toy
  project. Its run-local finalizer proposes exact outcomes; it does not reason
  or advance host gates. It is not builder authority.
- `tests/<component>/`: the component's behavior checks.

Keep the `src/` layout, single `workshop` namespace and installed sibling `cli`
package. Preserve unrelated work. Add contract and failure-path tests for runtime
or workflow behavior changes, using deterministic fakes for CI; never weaken a
production gate to make a test pass. Make small coherent commits.

Never commit credentials, `.env`, transcripts, run workspaces, build outputs or
private customer artifacts. Do not claim manufacture, delivery, publication or
live readiness from mocked or model-generated evidence. Distinguish implemented
behavior from accepted targets still migrating.

## Product-run agents

A product-run agent follows its materialized constitution and skill in its
isolated run root. It reads current `STAGE.json` and proposes compact outcomes
through the run-local finalizer. It does not use builder guidance as a product
workflow, modify Workshop source while making a toy, or bypass host authority.

## Agent skills

Issues use GitHub Issues via `gh`; read [issue tracking](docs/agents/issue-tracker.md).
Use the [canonical triage roles](docs/agents/triage-labels.md). For vocabulary and
ADRs, follow [domain documentation](docs/agents/domain.md): read the relevant
context rather than creating missing scaffolding upfront.
