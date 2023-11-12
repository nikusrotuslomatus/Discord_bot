import pathlib
import os
import logging
from logging.config import dictConfig
import discord
from discord.ext import commands
from discord import app_commands
import asyncio
import discord
from random import randint
import os
import random as rn
import youtube_dl
import json
from youtube_dl import *
from pydotenv import Environment
from discord.utils import get
from discord.ext import commands
from asyncio import sleep

BASE_DIR = pathlib.Path(__file__).parent

env = Environment()
TOKEN = env[ 'DISCORD_TOKEN' ]
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
prefix = '-'
client = commands.Bot(command_prefix=prefix, intents=intents)
flag_for_bulling_olya = False
olyas_tag = "9114"
client.remove_command("help")
youtube_dl.utils.bug_reports_message = lambda: ''
YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'False'}
FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                  'options': '-vn'}
new_class = None
films = [ i[ :-1 ] for i in open("moviesdoneright.txt", "r", encoding="utf-8") ]
mas_playlist = [ ]
command_list = [ "кто", "кого", "who", "fuck", "date", "story", "spam", "cls", "play", "game", "sendl", "help",
                 "test", "add", "add_all" ]
