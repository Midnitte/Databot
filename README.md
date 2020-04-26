# Databot
A telegram bot written in python, for a data science orientated channel.

## Available commands are:
`/pydoc <text>` to generate a printout of a python command's documentation
`/roll 1d20`, where 1 is the number of die, and 20 is the number of faces for the die.
`/funny` which posts a random top post from today via the r/ProgrammerHumor subreddit
  
## Setup:
  I currently run this script from a rasbian install on my Raspberry Pi 4, the script is setup to run from reboot via crontab:
  ```
  @reboot /usr/bin/python3.7 /home/pi/Desktop/TelegramBot/pybot.py >> log.log 2>&1
  ```
  
