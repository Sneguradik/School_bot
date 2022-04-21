import logging
from aiogram import Bot,Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage


TOKEN = '5274097359:AAHrx0jsu8mNl4fUhZkNZ_JdOj8n_awj1_A'

logging.basicConfig(level=logging.INFO)

storage = MemoryStorage()

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=storage)