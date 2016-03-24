# secretary-bot
[Telegram bot](https://core.telegram.org/bots/) which structures (classifies) messages sent to it and generates a digest later.
The idea is to talk to a robotic secretary in Telegram instead of talking to yourself (which I do all the time).
Messages I send myself usually fall into these categories:
- Ideas
- Quotes from articles I read on my phone
- TODOs and notes to self
- Things to check out later (movies, series, books, etc.)

# dependencies
- python 2.7
- [telepot](https://github.com/nickoala/telepot)
  - `sudo apt-get install python-pip && pip install telepot`
- [html](https://pypi.python.org/pypi/html)
  - `pip install html`
- sqlite3

# running
`python secretary.py <token-to-access-http-api>`

Note, that the script is not yet demonized, so it's a good idea to keep it running inside a `screen` session.

If you don't know what the token I am talking about is, chat with [BotFather](https://telegram.me/BotFather) to create yourself a new bot.
