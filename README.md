# Discord News Bot

A modular news briefing system that curates news via LLM and delivers to Discord.

## Architecture

```
discord-bot/
├── api/
│   └── index.py          # HTTP entry point
├── core/                  # Shared pipeline logic
│   ├── interfaces.py      # Abstract classes (Fetcher, Analyst, Notifier)
│   ├── fetcher.py         # RSS fetching
│   ├── analyst.py         # OpenAI analysis
│   └── notifier.py        # Discord webhook
├── bots/
│   ├── registry.py        # Bot registry
│   └── my_bot/           # Bot implementation
│       ├── config.py
│       └── prompt.txt
└── vercel.json
```

## Usage

```
GET /api?bot=sisa-go
```

## Environment Variables

| Variable              | Description     |
| --------------------- | --------------- |
| `OPENAI_API_KEY`      | OpenAI API key  |
| `SISA_GO_WEBHOOK_URL` | Discord webhook |

## Adding a New Bot

1. Create a new directory under `bots/`:

```
bots/
└── my_bot/
    ├── __init__.py
    ├── config.py
    └── prompt.txt
```

2. Define `config.py`:

```python
import os
from core import BotConfig

config = BotConfig(
    name="MY-BOT",
    sources=[
        ("https://news.google.com/rss/...", "Category", 5),
    ],
    prompt_path=os.path.join(os.path.dirname(__file__), "prompt.txt"),
    webhook_url=os.environ.get("MY_BOT_WEBHOOK_URL"),
    avatar_url="https://example.com/avatar.png",
)
```

3. Create `__init__.py`:

```python
from .config import config
```

4. Write `prompt.txt` with LLM instructions.

5. Register in `bots/registry.py`:

```python
@classmethod
def _ensure_initialized(cls):
    if cls._initialized:
        return

    from bots.sisa_go.config import config as sisa_go_config
    from bots.my_bot.config import config as my_bot_config  # Add this

    cls._bots["sisa-go"] = sisa_go_config
    cls._bots["my-bot"] = my_bot_config  # Add this
    cls._initialized = True
```

6. Add cron schedule in `vercel.json`:

```json
{
    "crons": [
        { "path": "/api?bot=sisa-go", "schedule": "0 10 * * *" },
        { "path": "/api?bot=my-bot", "schedule": "0 11 * * *" }
    ]
}
```

7. Set the environment variable `MY_BOT_WEBHOOK_URL` in Vercel.

## Local Development

```bash
vercel dev
# Access: http://localhost:3000/api?bot=sisa-go
```
