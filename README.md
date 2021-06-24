# Basic Utility Discord Bot

Just a basic utility bot that connects to Google Sheets to fetch some data - that's about it really.

## Recreating the Setup

On Linux:
1. Create a project on GCP, enable both the Google Drive and Google Sheets APIs, and upload an API token to `token.json` in this repository's root directory.
2. Create a Discord bot ready to run the code, and have the token ready.
3. In a terminal, from inside the root directory for this repository, run `echo "bot_token=<YOUR TOKEN>" > .env`, replacing `<YOUR TOKEN>` with the token from the previous step.
4. Install `docker-compose`.
5. Run `docker-compose up --build -d`.
