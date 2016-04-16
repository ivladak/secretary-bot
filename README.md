# secretary-bot
[Telegram bot](https://core.telegram.org/bots/) which structures (classifies) messages sent to it and generates a digest later.
The idea is to talk to a robotic secretary in Telegram instead of talking to yourself (which I do all the time).
Messages I send myself usually fall into these categories:
- Ideas
- Quotes from articles I read on my phone
- TODOs and notes to self
- Things to check out later (movies, series, books, etc.)
- Links to youtube/vimeo/etc. videos I want to watch later

# dependencies
- python 2.7
- [telepot](https://github.com/nickoala/telepot)
  - `pip install telepot`
- [html](https://pypi.python.org/pypi/html)
  - `pip install html`
- [youtube-dl](https://github.com/rg3/youtube-dl) to download videos
  - `pip install youtube_dl`
- sqlite3

If you don't have `pip`, install it first: e.g. `sudo apt-get install python-pip`.

# running
`python secretary.py <token-to-access-http-api>`

Note, that the script is not yet demonized, so it's a good idea to keep it running inside a `screen` session.

If you don't know what the token I am talking about is, chat with [BotFather](https://telegram.me/BotFather) to create yourself a new bot.
