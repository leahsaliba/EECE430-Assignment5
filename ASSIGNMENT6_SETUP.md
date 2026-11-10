# Assignment 6 — GitHub Actions CI/CD

The workflow in `.github/workflows/ci.yml` runs on pushes to `main`:

1. Installs Python 3.14 and project dependencies.
2. Runs `python manage.py check` with a CI-only placeholder key (does not call Gemini).
3. Builds the Docker image.
4. Publishes it to `ghcr.io/leahsaliba/eece430-assignment5:latest`.
5. Deploys on a Windows self-hosted runner labeled `ai-agent-deploy` by replacing the `eece430-ai-agent` container.

## One-time actions on your Windows computer

1. Install and launch Docker Desktop; keep it on Linux containers. Run `docker info` in PowerShell to verify.
2. In GitHub, go to **Settings → Secrets and variables → Actions → New repository secret**. Add `GEMINI_API_KEY` with your own API key. Do not commit your .env file or expose your key.
3. Go to **Settings → Actions → Runners → New self-hosted runner**. Choose **Windows x64**.
4. In **PowerShell** execute the download/extract commands GitHub displays on that page (use a runner directory outside your project such as `C:\\actions-runner`).
5. Run the GitHub-provided `./config.cmd --url ... --token ...` command. Use the label `ai-agent-deploy` when prompted. Keep the default runner group and work folder. Do not run as a service for the lab demo.
6. Start it with `.\\run.cmd` in the runner folder and keep that window open. Keep Docker Desktop running, too.
7. Open **Actions → AI Agent CI/CD → Run workflow**, or push to `main`. After both jobs finish, visit **http://localhost:8000**.

Note: The assignment also requires a **new GitHub repository**, a collaborator invitation to `am38@aub.edu.lb`, and an in-lab demonstration. This workflow currently targets the existing Assignment 5 repo; if the project is copied to a new repository, update the GHCR image tag in the workflow to match its new name before triggering deployment.

## Troubleshooting
- **CI fails at Django check:** Verify dependencies and the Python version.
- **Deploy is queued:** The Windows runner is not online or does not have the `ai-agent-deploy` label.
- **Docker fails:** Start Docker Desktop and switch to Linux containers.
- **Deployment missing key:** Set the `GEMINI_API_KEY` Actions repository secret.
- **Port 8000 occupied:** Stop the conflicting local app/container.
