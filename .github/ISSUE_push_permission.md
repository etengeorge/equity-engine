# Routine cannot persist runs: GitHub connection needs push permission

## Summary
The scheduled routine (claude.ai/code → Routines → "Equity Engine — daily research") ran 27 times
between Jun 5 and Aug 22 and **pushed nothing**. Every run clones fresh, commits `store/` locally,
fails to push, and the clone is destroyed. The repo's last run commit on `main` is from Jun 5.

v2 (#PR) makes this failure loud (exit 2 + manifest), but no code change can grant the permission.

## What the routine needs
| Requirement | Why |
|---|---|
| GitHub connection for `etengeorge/equity-engine` with **Contents: read & write** (push) | `store/` is the git-tracked audit trail; the retrospective scores theses against it; a fresh clone each run means an unpushed run is lost |
| Push to branch `main` allowed for the connection's identity (no branch-protection rule requiring PRs / status checks for that actor) | `orchestrate.git_committer` pushes `HEAD:main` directly twice per run (run + manifest) |
| Env in the routine: `SEC_USER_AGENT`, `PRICE_PROVIDER`, optional `TIINGO_API_KEY` | secrets live in the routine env, never in the repo (HARD RULE 6) |
| Connectors: Robinhood (read-only), S&P Global, Gmail, Google Drive only | every connected tool loads its schemas into every run's context; the other seven were never used |

## How to verify
From a routine run (or locally with the same token):
```
git push --dry-run origin main      # must print "Everything up-to-date" or a ref update, not 403/auth error
```
The v2 routine prompt runs exactly this at setup and stops with "push credential missing" if it fails.
After the first real run, `store/runs/<date>_daily.json` on `main` must show `"pushed": true`.

## Out of scope here
No tokens, emails, or account identifiers belong in this issue or the repo. Configure the permission
in the claude.ai GitHub connection settings and the routine's env.
