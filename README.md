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

The bot collects articles from 6 RSS feeds (5 articles each, 30 total):

| Source               | Category                            |
| -------------------- | ----------------------------------- |
| Yonhap News          | Economy, International, Industry/IT |
| Korea Economic Daily | Economy, International, IT          |

**Fetch criteria:** Takes the first N items from each feed in feed order. RSS feeds typically list articles by publication date (newest first). No view count or time filter—publishers control the order.

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
