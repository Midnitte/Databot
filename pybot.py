import os
import time
import pydoc
import random
from emoji import emojize
import re
import sys
import praw
#from dotenv import load_dotenv
#load_dotenv()

#API_KEY = os.getenv('PROJECT_API_KEY')
API_KEY = '7061726b6f7572'

reddit = praw.Reddit(client_id='497427732064616e6765726f757320746f20676f20616c6f6e65',
                     client_secret='646572706465727064657270',
                     password='useasecurepassword',
                     user_agent='redbot by /u/midnitte',
                     username='midnitte')


import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)



def get_top_posts():
    top_posts_data = []
    top_post_title = []
    subreddit = reddit.subreddit('ProgrammerHumor')
    
    top_python = subreddit.top(time_filter='day')
    for submission in top_python:
        if not submission.stickied:
            top_posts_data.append(submission.url)
            top_post_title.append(submission.title)
    todays_post = random.choice([0,1,2,3,4])
    todays_data = top_posts_data[todays_post]
    post_title = top_post_title[todays_post]
    logging.info(f'Todays Number: {todays_post}')
    logging.info(f'Todays URL: {todays_data}')
    logging.info(f'Todays Title: {post_title}')
    return todays_data, post_title
    

import telegram
from telegram.ext import Updater
updater = Updater(token=API_KEY, use_context=True)

dispatcher = updater.dispatcher



def start(update, context):
    context.bot.send_chat_action(chat_id=update.effective_message.chat_id, action=telegram.ChatAction.TYPING)
    time.sleep(0.2) # Give the appearance of typing
    context.bot.send_message(chat_id=update.effective_chat.id, text="Oh, don't get me <i>started</i>.", 
                 parse_mode=telegram.ParseMode.HTML, disable_notification=True)

from telegram.ext import CommandHandler
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

def pydoccmd(update, context):
    help_msg = pydoc.render_doc(context.args[0])
    shortened_msg = help_msg[0:250]
    logging.info('Help Message length: ' + str(len(shortened_msg)))
    logging.info(shortened_msg)
    time.sleep(0.2)
    context.bot.send_message(chat_id=update.effective_chat.id, text=shortened_msg, 
                 parse_mode=telegram.ParseMode.MARKDOWN, disable_notification=True)

# Adapted from https://gist.github.com/ryands/1340998
def roll(sides):
    """ Roll a (sides) sided die and return the value. 1 <= N <= sides """
    return random.randint(1,sides)

def parse_dice(cmd):
  """ Parse strings like "2d6" or "1d20" and roll accordingly """
  pattern = re.compile(r'^(?P<count>[0-9]*d)?(?P<sides>[0-9]+)$')
  match = re.match(pattern, cmd)

  if not match:
      raise ValueError() # invalid input string

  sides = int(match.group('sides'))
  try:
    count = int(match.group('count')[:-1])
  except:
    count = 1

  if count > 1:
    return [ roll(sides) for i in range(count) ]
  else:
    return roll(sides)

def roll_func(update, context):
    context.bot.send_chat_action(chat_id=update.effective_message.chat_id, action=telegram.ChatAction.TYPING)
    time.sleep(0.2)
    logging.info('Context is: ' + str(context.args))
    dice = emojize(":game_die:", use_aliases=True)
    roll = parse_dice(context.args[0])
    text_msg = ''
    if isinstance(roll, list):
      list_of_rolls = ','.join([str(x) for x in roll])
      total_roll = sum(roll)
      text_msg = f"You rolled {list_of_rolls} - for a total of {total_roll}. {dice}"
    else:
      text_msg = f"You rolled a {roll}. {dice}"

    context.bot.send_message(chat_id=update.effective_chat.id, text=text_msg, 
             parse_mode=telegram.ParseMode.HTML, disable_notification=True)

def funny(update, context):
    context.bot.send_chat_action(chat_id=update.effective_message.chat_id, action=telegram.ChatAction.TYPING)
    time.sleep(0.2)
    logging.info('Posting a top post')
    photo_url, photo_title = get_top_posts()
    time.sleep(0.2)
    print(photo_title)
    print(photo_url)
    match = re.search(r'(?:([^:/?#]+):)?(?://([^/?#]*))?([^?#]*\.(?:gif|mp4))(?:\?([^#]*))?(?:#(.*))?', photo_url)
    if match:
      context.bot.send_animation(chat_id=update.effective_message.chat_id, animation=photo_url, caption=photo_title, disable_notification=True)
    else:
      context.bot.send_photo(chat_id=update.effective_message.chat_id, photo=photo_url, caption=photo_title, disable_notification=True)


roll_handler = CommandHandler('roll', roll_func)
dispatcher.add_handler(roll_handler)

pydoc_handler = CommandHandler('pydoc', pydoccmd)
dispatcher.add_handler(pydoc_handler)

funny_handler = CommandHandler('funny', funny)
dispatcher.add_handler(funny_handler)

updater.start_polling()
