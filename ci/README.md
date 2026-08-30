# Parked CI workflow

`screen.yml` belongs at `.github/workflows/screen.yml`. It is parked here because the
credential used to push this branch is a Personal Access Token without the `workflow`
scope, and GitHub refuses any push that creates or modifies a file under
`.github/workflows/` with such a token. Nothing is wrong with the workflow itself.

## Activating it

Either grant the token `workflow` scope (GitHub → Settings → Developer settings →
Personal access tokens → edit → tick **workflow**), then:

```bash
git mv ci/screen.yml .github/workflows/screen.yml
git rm ci/README.md
git commit -m "Activate the daily screen workflow"
git push
```

Or, without touching the token, create the file through the GitHub web UI — Add file →
Create new file → path `.github/workflows/screen.yml` → paste the contents of
`ci/screen.yml`. The web editor is not subject to the token scope restriction.

## Before trusting the schedule

1. Add the repository secret `SEC_USER_AGENT` = `equity-engine <your-email>` under
   Settings → Secrets and variables → Actions. SEC returns 403 to anonymous clients, so
   without it every fundamental is missing.
2. Run it once manually via **workflow_dispatch** with `limit: 40` and confirm it commits.

Until the workflow is live, run the screen yourself:

```bash
SEC_USER_AGENT="equity-engine <your-email>" python run.py daily && python run.py site
```
