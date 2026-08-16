# telegram-reminder-bot

A simple Telegram bot built with `python-telegram-bot` for reminders, with support for three languages (English — default, Русский, Deutsch).

## Usage

The main way to use the bot is the persistent menu — no need to type commands by hand:

- **⏰ New reminder** — step-by-step wizard: pick a time (presets 5m/15m/30m/1h/3h/1d, or ✍️ Custom to type your own), then enter the text
- **📋 My reminders** — list of active reminders with time remaining; each one has its own 🗑 delete button
- **❓ Help** — detailed instructions
- **🌐 Language** — change interface language (English / Русский / Deutsch)

The same actions are also available as commands, for those who prefer typing:

- `/start` — show the greeting and menu
- `/help` — detailed instructions
- `/remind <time><unit> <text>` — quick shortcut, e.g. `/remind 10m call the client`
  - units: `s` (seconds), `m` (minutes), `h` (hours), `d` (days)
- `/myreminders` — list reminders and delete them
- `/language` — change language
- `/cancel` — abort setting a reminder

The default language is **English**, shown immediately on first launch regardless of the Telegram client's language; it can be changed at any time via the 🌐 Language button.

## Setup

```
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
```

Put your bot token (from [@BotFather](https://t.me/BotFather)) into `.env`:

```
BOT_TOKEN=your_token_here
```

`.env` is already listed in `.gitignore` and will not end up in git/GitHub.

## Running

```
python bot.py
```

## Data storage

Reminders and the chosen language are stored in a local SQLite database `bot_data.db` (created automatically next to `bot.py`). The DB file is listed in `.gitignore` and is not committed to git.

- On startup, the bot reloads reminders that haven't fired yet from the database and reschedules them — a bot restart doesn't lose them.
- Reminders that were due while the bot was offline are sent immediately after startup.

## Notes

- `.env` with the token is never committed (see `.gitignore`) — keep the token local only.
