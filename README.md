# secretary-bot
A [telegram bot](https://core.telegram.org/bots/) which remembers everything you say and generates a digest later.
The idea is to talk to a robotic secretary in Telegram instead of talking to yourself (which I do all the time).
It also allows you to run simple actions on the bot's machine. (Control you machine via chat messages!)

Features:
- Saves text messages to a database. When the user sends the `/digest` command the bot replies with an html containing all the messages since the last `/digest`.
- If you send the bot a link to a video on a video hosting site (the list of sites is configurable) it will download it (to the machine on which the bot runs). You can interrupt the downloading process (e.g. if you would like your hard drive to stop producing noise) by issuing the `/pause` command.
- Meditation. Say `/meditate [time-in-minutes]` and the bot will ring a gong twice: at the beginning and at the end of your meditation session. Of course the machine on which the bot is running must be able to make the sound i.e. have speakers connected to it and a simple sound playing software (see below).
- [Not implemented]: message classificataion. What I say to the bot is usually an idea or a quote or a TODO item, etc.

# dependencies
- python 2.7
- [telepot](https://github.com/nickoala/telepot)
  - `pip install telepot`
- [html](https://pypi.python.org/pypi/html)
  - `pip install html`
- [youtube-dl](https://github.com/rg3/youtube-dl) to download videos
  - `pip install youtube_dl`
- sqlite3
- aplay (for producing the gong sound)

If you don't have `pip`, install it first: e.g. `sudo apt-get install python-pip`.

# running
First, create a config file of the following form:
```
[bot] # Section name. Not optional.
token = 123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11 # Your token (see below) to control the bot through http api.
digest_dir = digest # Direcotry for saving digests on the server.
video_download_dir = ~/video/youtube
```
Now simply run

`python secretary.py <config-file>`

or even `python secretary.py` if your config file happens to be  "./bot-secretary.config" or "~/bot-secretary.config".

The bot is not demonized, however there's a script (auto-restart.sh) which restarts the bot in a detached screen session if it is not running.

If you don't know what the token I am talking about is, chat with [BotFather](https://telegram.me/BotFather) to create yourself a new bot.

# attribution
This repository includes these sounds from freesound:

[Gong.wav](http://www.freesound.org/people/juskiddink/sounds/86773/) by [juskiddink](http://www.freesound.org/people/juskiddink/).
