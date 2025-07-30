# actions-sample-1

This repository contains a simple notes CLI application (`main.py`) and a GitHub
Actions workflow that analyzes code changes using OpenAI before sending a summary
via email upon approval.

## Notes Application

The CLI allows you to add, list, remove and search notes stored in `notes.json`.

```bash
python main.py add "title" "content"
python main.py list
python main.py remove <id>
python main.py search "keyword"
```

## GitHub Actions Workflow

The workflow located at `.github/workflows/analyze.yml` performs the following:

1. Trigger on pushes to the `main` branch.
2. Capture the git diff and send it to OpenAI to summarize potential impact.
3. Upload the summary as an artifact and wait for manual approval.
4. After approval, email the analysis to the address specified in secrets.

### Required Secrets

- `OPENAI_API_KEY` – API key for OpenAI.
- `SMTP_SERVER`, `SMTP_PORT`, `SMTP_USERNAME`, `SMTP_PASSWORD` – credentials for sending email.
- `MAIL_TO` – recipient email address.

The manual approval step uses the [trstringer/manual-approval](https://github.com/trstringer/manual-approval)
action. The email is sent using [dawidd6/action-send-mail](https://github.com/dawidd6/action-send-mail).

### Personal Access Token

The workflow relies on the built-in `GITHUB_TOKEN` for most operations. When running in
environments where this token does not have sufficient privileges (e.g. forks), create a
PAT with at least the following scopes:

- `repo` – read repository contents and create statuses for approval.
- `workflow` – trigger and approve workflows.

Add this token as a secret (for example `GH_PAT`) and reference it in the workflow if needed.

### Notes on `GITHUB_OUTPUT`

The `Analyze diff with OpenAI` step outputs the analysis using a multi-line variable. To
avoid `"Matching delimiter not found '__END_OF_ANALYSIS__'"` errors, the closing delimiter
must appear on its own line. The workflow writes a blank line before the closing delimiter:

```bash
echo "analysis<<__END_OF_ANALYSIS__" >> $GITHUB_OUTPUT
cat sanitized_analysis.txt >> $GITHUB_OUTPUT
echo "" >> $GITHUB_OUTPUT
echo "__END_OF_ANALYSIS__" >> $GITHUB_OUTPUT
```
