# exchange-rate-bot

Telegram exchange rate bot

# prepare data

1. Navigate to configs/config.py
2. Set up the following data
   | Key | Description |
   | ----------------------------------- | ------------------------------------ |
   | **TELEBOT_TOKEN** | your bot token in the telegram app |
   | **EXCHANGE_API** | url excange api|

# start commands

1. Export application varibles
   **export TELEBOT_TOKEN=<string>**
   **export EXCHANGE_API=<url>**
2. Run application module
   **poetry run python3 -m exchange**
