# minecraft-server-status-bot

Bot that checks status for a specified server and displays it in the Discord sidebar

## Installation

1. Clone the repository
2. Install requirements (listed in the next section)
3. Create a config.yml file, and paste this in (make sure to fill in the values):
   ```yml
   bot-token: BOT-TOKEN-HERE
   server-url: SERVER-URL-HERE
   ```
4. Run bot.py

## Requirements

- discord.py==1.3.2
- mcstatus
- pyyaml
- OPTIONAL: jishaku
