import logging
from aiogram import Bot, Dispatcher, executor, types

TOKEN = '5274097359:AAHrx0jsu8mNl4fUhZkNZ_JdOj8n_awj1_A'

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer('Привет! Это чат бот для организациитвоеё работы! Пожалуйста зарегистрируйся командой /register, если ты не зарегистрировался.')

@dp.message_handler(commands=['register'])
async def register(message: types.Message):
    pass

@dp.message_handler