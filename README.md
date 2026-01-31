# SISA-GO

A daily news briefing bot that curates Korean news and delivers analysis via Discord.

## Overview

SISA-GO fetches news from major Korean outlets, analyzes them using an LLM, and sends a curated briefing to a Discord channel. The goal is to help professionals in their 20s-30s stay informed on essential topics: global economy, politics, and technology.

## Tech Stack

-   Python 3.9+
-   Vercel Serverless Functions
-   OpenAI API
-   Discord Webhook

## Data Pipeline

### News Sources

The bot fetches from Google News RSS Korea (5 per topic, outputs 2 per topic = 6 total):

| Feed       | Fetch | Output | Description                |
| ---------- | ----- | ------ | -------------------------- |
| World      | 5     | 2      | International, geopolitics |
| Business   | 5     | 2      | Economy, finance, markets  |
| Technology | 5     | 2      | IT, AI, tech industry      |

**Fetch criteria:** Google News ranks by importance (not recency). LLM selects the 2 most significant from each topic.

### Schedule

Runs daily via Vercel Cron (schedule in `vercel.json`).

### LLM Processing

-   Model: `gpt-4.1`
-   Max tokens: 16,384
-   Role: Select top 5 essential news, provide factual summary, historical context, and key term definitions

## Environment Variables

| Variable              | Description                 |
| --------------------- | --------------------------- |
| `OPENAI_API_KEY`      | OpenAI API key              |
| `DISCORD_WEBHOOK_URL` | Discord channel webhook URL |
