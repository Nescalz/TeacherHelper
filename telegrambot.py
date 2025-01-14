from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ConversationHandler, ContextTypes, JobQueue
from telegram.ext.filters import TEXT
from sqlite3 import connect, IntegrityError
import asyncio
import os
import bot_token

os.chdir(os.path.dirname(os.path.abspath(__file__)))

