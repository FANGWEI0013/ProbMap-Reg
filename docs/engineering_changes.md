# Second-round non-destructive packaging changes

No original research source, dataset, checkpoint or paper was edited. The first-round candidate is snapshotted privately before changes. Candidate copies with uncertain rights are moved to external quarantine, not destroyed. Existing Git remains on release-review with no commits or remotes; no history rewrite is performed.

The complete retained `src/reconstruction` files are byte-identical to the first-round candidate. No thresholds, HOG, matching, scaling, RANSAC, geometry, AUC, legacy bootstrap or failure-case logic was corrected silently. The minimal tests no longer import quarantined historical utilities.

New `bootstrap_statistics.py` is an explicitly separate reporting diagnostic calling the recovered AUC. It calculates point AUC, actual bootstrap mean and percentile CI under the recovered sample order/seed. Legacy bootstrap output semantics remain documented and unchanged. This does not change paper values or add a claimed missing experiment.

The former training/model implementation is an external preserved bundle. New `train_unet.py` only launches a user-supplied authorized trainer; it has no replacement architecture/loss/preprocessing. Its help/delegation path is tested without fitting. Public requirements are trimmed to retained-core imports. Historical/variant dependencies remain with private quarantine.

Two-pair controlled profile changes and FPE policies exist only in private diagnostic scripts and public aggregate reports. They are not configurable production fixes or claimed publication runs. No training input/target folder was automatically swapped.

## Round 3 packaging additions

Added `scripts/evaluate_fire.py`, a saved-error CLI that calls the unchanged summarizer and refuses input overwrite. Improved main wrapper help and bootstrap/failure prerequisite reporting. Added three CLI/evaluation tests. Updated Quickstart, README, reporting/config metadata, privacy/rights review and positive manifests. Public archival inventories were replaced with aggregate/source-class descriptions; detailed prior copies remain in private snapshots. All eleven scientific modules retain their Round 2 hashes. Original projects are untouched.

## First-release preparation — 2026-10-28

Author confirmation updates source-authorship status; the scoped contrary-evidence check was limited to retained code/notices. README and release evidence were polished, an MIT draft with author-selected name Wei Fang was prepared, and only the explicit non-license list was staged. All scientific source bytes and published metadata remain unchanged. Preserved Windows CRLF lines require Git whitespace checks with cr-at-eol enabled; this recognizes line endings without ignoring genuine trailing spaces or rewriting source. No commit, remote or push.

## Approved MIT finalization — 2026-10-29

Explicit MIT approval supersedes the earlier dated pending status. LICENSE bytes and all twenty Python source files are unchanged. Updated current README, reports, status metadata and checksums; staged the entire approved 68-file list including LICENSE. All twelve tests passed again in the actual candidate. Commit/remote/push/visibility actions remain separately gated and were not performed.
