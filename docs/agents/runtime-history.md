# Historical runtime instruction chain

This is archival evidence for investigating decisions and frozen protocols, not
active instructions or a recipe for a new run. Start with the current
[builder guidance](../../AGENTS.md) and [runtime map](../NATIVE_AGENT_RUNTIME.md).
A frozen run's materialized inputs govern that run; an old ADR does not upgrade
it or restore a retired path. Paths in backticks below are repository-relative.
The former read-all list is retained for provenance, not as a current requirement.

## Former builder amendment narrative

Read `docs/NATIVE_AGENT_RUNTIME.md`,
`docs/adr/0012-codex-orchestrated-runtime.md`, and
`docs/adr/0013-manual-first-release.md`, and
`docs/adr/0014-terminal-published-release.md`, and
`docs/adr/0015-defer-playtest.md`, and
`docs/adr/0016-selectable-effort-routes.md`, and
`docs/adr/0019-frozen-spark-economics-profile.md`, and
`docs/adr/0020-signature-experience-evidence.md`, and
`docs/adr/0021-compacted-spark-and-signature-review.md`, and
`docs/adr/0022-blind-review-before-final-verification.md`, and
`docs/adr/0023-bounded-spark-turn-and-semantic-review.md`, and
`docs/adr/0050-structured-terminal-failure-diagnostics.md`, and
`docs/adr/0049-product-wide-token-budget.md`, and
`docs/adr/0060-make-round-visual-feedback-and-three-repairs.md`, and
`docs/adr/0061-spark-make-owned-verification.md`, and
`docs/adr/0062-step-only-cad-toolchain.md`, and
`docs/adr/0063-spark-component-first-make.md`, and
`docs/adr/0063-print-gates-on-source.md`, and
`docs/adr/0064-operator-selected-turn-boundary.md`, and
`docs/adr/0074-every-component-scored-against-its-own-image.md`, and
`docs/adr/0075-component-review-compares-form-and-acceptance-needs-a-second-reader.md`, and
`docs/adr/0076-component-passes-on-an-independent-review-not-a-likeness-score.md`, and
`docs/adr/0077-component-workers-and-a-root-owned-reviewer.md`, and
`docs/adr/0080-component-workers-author-and-a-hook-admits-their-rounds.md`, and
`docs/adr/0081-shape-rounds-follow-component-reviews.md`, and
`docs/adr/0082-interfaces-between-components.md`, and
`docs/adr/0083-compare-in-the-display-pose-at-the-reference-camera.md`, and
`docs/adr/0084-interface-text-and-reference-conflicts.md`, and
`docs/adr/0085-in-run-contract-amendments-for-invisible-fixes.md` before changing the CLI, runtime,
workflow, product-run instructions, or lifecycle orchestration. ADR 0013
supersedes ADR 0012's page-first Release details; ADR 0014 supersedes their
optional-publication and executable-Deliver details. ADR 0015 supersedes the
active Playtest stage while preserving truthful omission and frozen-run
compatibility. ADR 0016 supersedes ADR 0015's fixed topology for new runs while
preserving its truthful omission contract for Spark and Forge. The
native-session path is the production architecture. ADR 0019 freezes a
lower-cost Codex profile only for new marked Spark runs without changing their
gates or upgrading older sessions. ADR 0020 adds exact signature-experience
evidence and batched manual review without adding a host-side judge. ADR 0021
adds a frozen Spark compaction ceiling, final signature-review evidence, and a
bounded simple-manual path without splitting the Wish-wide session. ADR 0022
makes the review blind, places it before one final integrated verifier, rejects
duplicate final render families, and distinguishes core creative ownership from
carrier mechanics.
ADR 0023 adds a frozen 20-minute Spark native-turn boundary, requires the blind
critic to agree separately on subjects, action, and relationship, bounds that
critic to two rounds, and makes the integrated final CAD verifier refuse to run
before the hash-bound review exists.
ADR 0024 treats “10x quality at 0.1x cost” as a comparative North Star rather
than a literal lifecycle threshold. ADR 0025 extends the blind review to exact
form and the concept's anti-generic signature, binds it to the canonical concept
hash, and requires the final verification report inside the declared
self-contained CAD project.
ADR 0050 retains a bounded structured diagnosis for terminal provider failures
while continuing to discard unsafe free-form provider text.
ADR 0049 supersedes earlier Workshop time/turn/retry/round spending caps for
token-budget products, not Make's internal engineering or review policy.
ADR 0061 supersedes duplicate host verification and native manual
authoring for Spark only; it leaves Make's own implementation intact. Do not
reintroduce these removed boundaries from an older ADR or frozen-run fixture.
ADR 0063 makes new Spark Make work component-first: every distinct component
has its own source and isolated make-round repair loop before assembly review.
It changes native Make work and its deterministic round tool, not Workshop's
host-owned Spark acceptance boundary.
ADR 0060 requires native Manager visual feedback within Make rounds and expands
final blind review to an initial review plus three repair-and-rereview cycles
for new runs. Frozen older runs retain their original allowance and tool bytes.
ADR 0062 makes STEP the only geometry format Workshop writes, seals or ships:
the mesh export, cadgen's STL/3MF writers and the Workshop-local
print-preflight path are gone. Do not reintroduce a mesh deliverable from an
older ADR or a frozen-run fixture.
ADR 0063 supersedes ADR 0062's gate half and keeps its export half. The
`check_mesh`, `check_overhang` and `check_thickness` gates are back, reading
the B-rep directly instead of an exported mesh, so the CAD gate has two tiers
again. A product is print-ready only behind a passing `verify_project
--print-gates` run at the nozzle the print will use, declared twice — root
product status `full-with-thickness` **and** `print_ready_claim: true` — and
reproduced by the host's own rerun. A half-declared claim is refused, not
downgraded, and the legacy `--exports` full-tier replay path stays retired.
ADR 0064 adds one opt-in `--turn-minutes` override above the frozen turn
boundaries of ADR 0019, ADR 0023 and the deep-economics profiles, and supersedes
none of them: a run that does not ask keeps the exact boundary it froze. It
bounds a wall clock only; no gate, review, round or token allowance moves.
ADR 0074 scores every Contract Mode Component against its own sealed
`geometry:<id>` image at the 0.90 floor, never against the whole object, and
makes the final verifier account for every sealed image. Below the floor the
Workshop Manager may accept an image only after it stalls out, with a reason
the run reports when it ends; it is never recorded as the person's decision.
ADR 0075 amends that acceptance: a stall-out counts only rounds that changed
the geometry, every scored image is composed beside the model for the review,
feedback below the floor must list its differences from the image, and a
component acceptance needs a recorded review by someone other than the
Workshop Manager.
ADR 0076 supersedes the likeness parts of ADRs 0072, 0074 and 0075: no IoU
is computed anywhere in the pipeline. A Component passes on build, print gates
and an independent reviewer's recorded agreement, judged from each reference
beside the model at its declared camera. After five Shape Rounds a disagreeing
review is recorded as a Component Acceptance, sealed as
`component_acceptances` and reported when the run ends. Assembly rounds keep
the Manager's visual feedback, the blind review and `--full`.
ADR 0077 moves each Component's repair loop out of the root Manager for new
runs: one Component Worker per Component, with only that Component's inputs,
and one reused Component Reviewer thread per Component that the root, not the
worker, asks. Only the reviewer views component images. The host materializes
both as declarative custom agents; Codex owns spawning. Waits use 300000 ms.
Assembly rounds, the blind review and final verification stay with the root.
ADR 0080 amends ADR 0077 and ADR 0063 step 1 for new runs: the root writes
only shared `params.py`/`features/` files with every joint fixed, and each
Component Worker authors its Component. The worker may view its own sealed
reference but never rendered rounds. A host-state `PreToolUse` hook admits a
component round only from a `component-worker` and passes it a one-time
nonce; the host refuses a component round without an issued nonce. Two
contradicting Design Contract statements are a `need`.
ADR 0081 amends the Shape Round counting and cap of ADRs 0075-0077 for new
runs: a passing component round is reviewed before its geometry may change; a
Shape Round is the first geometry change after a disagreeing review; an
agreeing review or a Component Acceptance locks the Component until a Shared
Helper it imports changes or the Manager records an assembly unlock, and a
rerun of the reviewed B-rep carries the review forward. A component packet
binds only the Shared Helpers it imports, and a failed round is not rendered.
ADR 0081's extension (issue #77) binds each Component's reviews to one proven
Component Reviewer on Claude Code: a review names the reviewer's native agent
id, the first review binds it, and Make acceptance refuses a review whose
reviewer the guard did not see start as a `component-reviewer` or read every
packet image. The Manager sends a fixed request (packet, hash, contract rows)
once per packet and tells the worker only which round was reviewed. Codex
keeps its earlier review rules until it exposes the same evidence.
ADR 0082 records Interfaces between Components for new schema 2 Design
Contracts: each Interface has a Kind (static, separable or coupled) and the
Components it joins. The Manager's Shared Helpers hold only Interface values,
joint sections and standard profiles, and are frozen by hash after their
samples pass `make_round --shared-helpers`; component rounds refuse to start
before the freeze and report later helper changes with their importers. A
separable Interface's Keep-out Envelope is checked in each side's own
component round, and `make_round --interface <id>` checks a Coupled
Interface on its locked Components, unlocking the yielding one on failure.
Assembly and final verification need a current passing check of every
Coupled Interface, both modes are root-only, Component Workers live until the
assembly passes, and the run report lists every Interface with its proof.
Its #80 amendment lets an Interface name one instance of a Unique Geometry
whose count is above 1, `<id>#<n>` (`wing#1` meets `wing#2`); the geometry's
one Component file builds and places each instance, and locking, staleness
and unlocks stay with that Component.
ADR 0083 adds Design Contract schema 3 for new contracts: every reference
carries its Reference Camera (`[AZ, EL]` in the Display Pose frame, estimated
by eye in design-a-toy and approved with the images), every Component defines
`assembly_pose`, and a component round composes each reference beside
`assembly_pose(shape, None)` rendered at that camera while front, top and iso
stay in the print stance. The Component Reviewer's third verdict, camera
mismatch, is not a Shape Round and gives the worker no repair text; it stops
the run with a need that `workshop resume --reference-camera FILE=AZ,EL`
answers with a host-recorded amendment of that one camera, leaving WISH.json,
requirements and images sealed. Schema 1 and 2 contracts and frozen runs keep
the earlier comparison.
ADR 0084 adds Design Contract schema 4: every Interface carries `text`, what
it imposes on each Component it joins, which no gate measures. A component
round writes the Component's rows and the text of every Interface naming it
into its visual packet and summary, so the Manager's review request is the
packet path and hash. Where a reference shows what the contract forbids, the
reviewer lists a Reference Conflict, not a difference: the contract wins, it
costs no Shape Round, never reaches the worker, and the final receipt and
`workshop status --json` report it. A difference below the print limits is
not listed. Schema 1 to 3 contracts and frozen runs keep the earlier review.
ADR 0085 amends ADR 0080 and ADR 0083 for new runs: where a Contract
Contradiction's smallest fix changes nothing a sealed reference shows, the
Manager may propose a Contract Amendment with `make_round
--propose-amendment` instead of a need. A fresh `contract-reviewer`, a third
fixed Make role agent, confirms that the quoted rows cannot both hold, that
the change is the smallest and that no reference shows it; otherwise the run
stops on the need. Only requirement and Interface text change; WISH.json and
the images keep their bytes. Rounds read the amended rows and a Component
whose rows changed unlocks; `--clear-blocked` may answer a Blocked Report
with the applied amendment. The host replays the ledger against the sealed
contract by hash before Make acceptance, refusing a missing review, a
disagreement or visible change counted as applied, or a changed contract
hash, and the receipt lists every amendment. `build-a-toy` folds each
applied amendment into the toy's contract and ledger.
Its #96 amendment allows one Smaller Retry: when a review confirms the
contradiction, finds the change invisible but names a smaller one, the
Manager may propose once more with the same rows, each change's new text the
refused `from` with only deletions applied, to another fresh
`contract-reviewer`. The tool and the host's replay refuse a retry that adds
or respells a word, a third proposal for the same rows, a retry after a
contradiction or visibility refusal, and a reused reviewer.
ADR 0081's #97 amendment makes a Manager's ruling on a Blocked Report bind
the Component Reviewer for new runs: the Component's decided rulings travel
in its review packet and join the carry key, the request stays the packet
path and hash, and a reviewer who thinks a ruling wrong lists a Ruling
Dispute instead of a difference. A dispute costs no Shape Round and never
reaches the worker; a dispute-only review agrees.
Preserve useful deterministic contracts and tests; do not reintroduce removed
cognitive orchestration as a compatibility layer.

## Former runtime-map introduction

# Native coding-agent runtime

This is the operating map for people and coding agents building Autonomous
Workshop. It is authoritative together with
[ADR 0012](../adr/0012-codex-orchestrated-runtime.md),
[ADR 0013](../adr/0013-manual-first-release.md),
[ADR 0014](../adr/0014-terminal-published-release.md),
[ADR 0015](../adr/0015-defer-playtest.md),
[ADR 0016](../adr/0016-selectable-effort-routes.md),
[ADR 0019](../adr/0019-frozen-spark-economics-profile.md),
[ADR 0020](../adr/0020-signature-experience-evidence.md),
[ADR 0021](../adr/0021-compacted-spark-and-signature-review.md),
[ADR 0022](../adr/0022-blind-review-before-final-verification.md),
[ADR 0023](../adr/0023-bounded-spark-turn-and-semantic-review.md),
[ADR 0031](../adr/0031-bind-deep-profile-and-bound-first-proof.md),
[ADR 0032](../adr/0032-restore-make-depth-and-blindly-review-first-proof.md),
[ADR 0036](../adr/0036-reserve-proof-runway-for-product-bytes.md),
[ADR 0037](../adr/0037-raise-deep-compaction-ceiling.md),
[ADR 0038](../adr/0038-prove-product-states-and-bound-final-source.md),
[ADR 0039](../adr/0039-make-invent-recovery-a-source-handoff.md),
[ADR 0040](../adr/0040-make-proof-recovery-a-sealing-handoff.md),
[ADR 0042](../adr/0042-browser-issued-factory-credential.md),
[ADR 0043](../adr/0043-freeze-agent-model-and-effort.md),
[ADR 0044](../adr/0044-scope-component-cad-network.md),
[ADR 0045](../adr/0045-own-agent-selected-dependencies.md),
[ADR 0046](../adr/0046-budgeted-spark-twenty-minute-turns.md),
[ADR 0049](../adr/0049-product-wide-token-budget.md),
[ADR 0050](../adr/0050-structured-terminal-failure-diagnostics.md),
[ADR 0060](../adr/0060-make-round-visual-feedback-and-three-repairs.md),
[ADR 0061](../adr/0061-spark-make-owned-verification.md),
[ADR 0063](../adr/0063-spark-component-first-make.md), and the repository
[agent instructions](../../AGENTS.md). ADR 0013 supersedes ADR 0012's page-first
Release details; ADR 0014 supersedes their optional-publication and
executable-Deliver details; ADR 0016 supersedes ADR 0015's one fixed route.
