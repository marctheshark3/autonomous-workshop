# Local Workshop setup and review

This guide covers a private Spark build from a source checkout. Workshop still
specializes in physical toys and CAD products; it is not a general-purpose
automation service. Local builds use a signed-in model account and can use
native research tools. `--no-publish` controls publication, not model access.

## Environment

Use a current uv installation and a managed Python 3.14 interpreter:

```bash
uv python install 3.14
uv sync --frozen --python 3.14
codex login
uv run --frozen workshop doctor
```

The CLI supports Python 3.11 and newer, but the parallel motion tool uses
Python 3.14's worker termination API. Motion checking is opt-in; a successful
run without it must continue to report motion as unverified. The dev dependency
group installs pytest so both pytest functions and unittest classes run, plus
pip for the installed-wheel acceptance script.

Use the locked uv environment for CAD. It installs the repository's reviewed
`cadgen` fork through `[tool.uv.sources]`. A plain pip install resolves a
different PyPI package with the same `0.4.19` version and is not an equivalent
CAD installation. Avoid changing the interpreter or its installation paths
under an unfinished run: native sessions bind their exact runtime identities.

### Linux sandbox

Workshop denies filesystem reads outside the run and its trusted runtimes.
For npm Codex installations it grants the JS launcher and actual native
platform executable as separate read-only files. Python aliases retain their
identity bindings, but a symlink already exposed by a trusted directory and
explicit target needs no additional Linux bind mount.

Codex 0.159.3 with a system Bubblewrap 0.6.1 still fails to re-enter its sandbox:
the older launcher needs an alias inside Codex home, which Workshop denies.
Select Bubblewrap with `--argv0` support (introduced in 0.9) on PATH. Codex's
installed `codex-resources/bwrap` is one suitable build:

```bash
# Replace this with the codex-resources directory in your Codex installation.
PATH="/path/to/codex-resources:$PATH" uv run --frozen workshop doctor
PATH="/path/to/codex-resources:$PATH" uv run --frozen workshop wish \
  "A small one-piece tactile desk pebble" --inventor halden-detent \
  --max-tokens 10000000 --no-publish
```

Alternatively, an owner-created symlink at `.venv/bin/bwrap` can select that
same installed binary for this checkout's `uv run` commands. Keep it out of
Git. Do not grant all of Codex home or disable the sandbox to fix this error.
The relevant upstream behavior is in Codex's
[Bubblewrap launcher](https://github.com/openai/codex/blob/rust-v0.159.3/codex-rs/linux-sandbox/src/launcher.rs)
and [native helper setup](https://github.com/openai/codex/blob/rust-v0.159.3/codex-rs/arg0/src/lib.rs).

`doctor` requires Codex 0.153.4 or newer for new token-budget runs and checks
installation, authentication and available assets;
it does not execute a sandboxed CAD command or prove a successful product run.
Treat its `ready` result as setup discovery, not end-to-end acceptance.

## First private build

```bash
uv run --frozen workshop wish "A small one-piece tactile desk pebble" \
  --inventor halden-detent --workflow spark --agent codex \
  --max-tokens 10000000 --no-publish
uv run --frozen workshop status <product-id>
uv run --frozen workshop resume <product-id>
```

The host owns the run directory, checkpoints and local Release archive.
Resume uses the exact native session and keeps consumed tokens. An explicit
`resume --max-tokens N` changes the total allowance, not the remaining amount.
No Factory login, credential read or publishing effect is needed for a local
Release. `start <inventor> --once --no-publish` also works, as do saved ideas,
typed Wishes and repeated local builds. Omit `--once` only when you intend an
ongoing loop; each build gets its own budget and Daydream has a separate session.

## Observed acceptance

On 2026-10-07, a real Codex 0.159.3 Spark run built a one-piece tactile pebble,
passed Make, and completed host-owned Release with `status: complete` and
publication `unreleased`. Its 130 archived files matched their manifest
hashes. The same native session survived the setup repairs and an explicit
finalizer-tool refresh. No Factory effect or physical print was performed.

That run used managed Python 3.11. The checkout was then moved to managed
Python 3.14.8 for motion support. A fresh Codex sandbox probe built a build123d
solid under 3.14.8 while source-checkout and credential reads remained denied;
`doctor` reported ready. The latest focused runtime, CLI, finalizer, integration,
motion and architecture checks passed 443 tests, and Release checks passed 51.

The full managed-3.14 sweep passed 2,784 tests and skipped 19 before three
outdated test fixtures were repaired and rerun. Its fourth failure, the input
headroom assertion below, remains open. The separate opt-in native-fidelity and
installed-wheel acceptance suites also need fixture migration. This is evidence
for local Spark operation, not a claim that every workflow or acceptance suite
passes. The private sample, native session and logs stay outside Git.

## Review findings to keep visible

- **Native launch:** Linux virtualenv aliases and npm native-helper grants
  prevented the first live attempt. The repaired policy retains exact path
  identities and accepts only its known predecessors on resume. A real sandbox
  probe imported build123d while the source checkout and Codex credentials
  remained inaccessible.
- **Optional vault:** Linux may present an absent protected `VAULT.json` as a
  zero-byte file. The finalizer now accepts that placeholder only when a valid,
  read-only host stage has no vault binding. A bound empty snapshot, a symlink,
  or corrupt nonempty data still fails. Existing runs need an explicit host
  tool refresh to acquire this finalizer fix; preview it with
  `workshop resume <id> --refresh-tools --refresh-tree autonomous-workshop --dry-run`
  and review the complete list before rerunning without `--dry-run`.
- **Local entry point:** `start` previously required a publishing account even
  when local work was wanted. `start --no-publish` now forwards the existing
  frozen host restriction and skips that login for every input path.
- **Local archive reporting:** new unreleased archives identify their timing
  boundary as the locally sealed Release, and their reproduction command keeps
  `--no-publish`. Older archive bytes are preserved. The smoke run also exposed
  a discrepancy between the archive's best-effort per-turn token summary and
  the host's rollout-based whole-run budget after resumes. Read the `budget`
  field of `workshop status --json` for the enforced allowance; archive usage
  reporting needs a separate accounting review.
- **Offline acceptance drift:** the opt-in deterministic native fidelity
  fixture identifies itself as Codex 0.150.0, while current token-budget runs
  require 0.153.4 or newer and native rollout usage. Its failure before creative
  stages is not evidence that Forge or Quest pass. The fixture needs a separate
  update to the current protocol; production gates must remain intact.
- **Wheel acceptance:** its package-data allowlist still rejects the three
  required fixed Make role agents, before it can test the installed command.
  Update that fixture alongside its old native-runtime protocol. Keep the role
  agents in the wheel; removing required runtime files is not a packaging fix.
- **Input headroom:** the complete installed roster and skill tree exceeds the
  test's reserved 1 MiB headroom by roughly 9 KiB. It remains below the actual
  6 MiB input limit. Audit duplicated or unnecessary assets before expanding
  the roster or changing this limit.

## Vibecad and printables handoff

The local companion projects are `10-X-eng/vibecad` and
`marctheshark3/printables`. They have compatible uses, but different contracts:

| Stage | Authority and output |
| --- | --- |
| Workshop | Wish, Inventor, checked CAD source, STEP geometry and sealed archive |
| Vibecad | Optional inspection or further editing of imported STEP in its own project |
| Printables | A new `PRINT_SPEC.yaml`, parameter provenance, one STL per manufactured body, geometry/assembly validation and optional slicing |

Keep the first integration as a separate downstream project referencing the
Workshop archive and its hashes. Import STEP for inspection; edited geometry
needs fresh checks. STEP import does not preserve Workshop's Python parameter
history, and a static imported body alone does not satisfy printables'
parametric-source contract. A proper printables adapter must retain an editable
source, explicit printer/nozzle/material/orientation constraints, conversion
provenance and the existing validation gates.

Do not install the printables bundle wholesale into a product run: Workshop
ships STEP only, while printables deliberately exports STL. Keep conversion
and slicing after Workshop's sealed boundary, and keep printer control as a
separate explicit operation. No companion repository or printer configuration
is changed by the local-start repair.
