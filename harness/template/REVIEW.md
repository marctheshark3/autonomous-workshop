# Standalone Make final signature review

This reference is copied into each standalone Harness workspace as `REVIEW.md`.
Read it when preparing the final gate, after the shape has settled. It preserves
schema 8 for this standalone workflow; it does not select a Workshop Contract
Mode protocol or grant host/effect authority. Read the actual verifier result.

Final mode refuses to start until `snap/SIGNATURE-REVIEW.json` exists — the blind review that
Workshop requires before its integrated gate. Produce it like this:

1. `render_product model.step -o snap/iso.png` and a fixed-camera state or motion sheet at
   `snap/signature.png` (`--state-sheet` for a mechanism, `--motion-sheet` for a static shape),
   both at least 1200×800.
2. Give one independent critic (a subagent) only those two images, without the user's request,
   and record its held-object, form, subjects, action, relationship and anti-generic reads. Then
   reveal the request and judge the matches. Repair and re-render if it finds a blocker; at most
   four review rounds.
3. Write the review as canonical JSON (`sort_keys`, separators `,` and `:`, no trailing newline)
   with exactly these keys: `schema_version` (8), `kind`
   (`autonomous-workshop.signature-experience-review`), `concept_sha256` (sha256 of your brief),
   `iso_sha256`, `signature_sha256` (sha256 of the two PNGs), `reviewer`, `blind_held_read`,
   `blind_form_read`, `blind_subjects_read`, `blind_action_read`, `blind_relationship_read`,
   `anti_generic_signature_read`, `largest_risk`, `resolution` (non-empty text);
   `wish_revealed_after_blind_read`, `held_object_unmistakable`, `form_matches_wish`,
   `subjects_match_wish`, `action_matches_wish`, `relationship_matches_wish`,
   `anti_generic_signature_visible`, `signature_experience_unmistakable`,
   `finished_product_desirable` (all `true`); `review_rounds` (1–4);
   `critical_form_requirements` (1–16 of `{requirement, blind_evidence, matches: true}`);
   `blocking_visual_defects` (`[]`); `print_gate_sha256s` (`{}` until the print gates ran, then
   each cited `measure/<gate>-<role>.md` mapped to its sha256).
