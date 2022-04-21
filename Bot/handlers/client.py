from typing import Text
from aiogram import Dispatcher, types
from numpy import equal
from create import dp, bot
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
import database.sqlite_db as db 
from aiogram.dispatcher.filters import Text

class FSMClient(StatesGroup):
    telegram_id = State()
    username = State()
    name = State()
    surname = State()
    grade_num = State()
    grade_letter = State()
    status = State()

async def start(message: types.Message):
    await message.answer('Привет! Это чат бот для организациитвоеё работы! Пожалуйста зарегистрируйся командой /register, если ты не зарегистрировался.')


async def register(message: types.Message, state:FSMContext):
    FSMClient.telegram_id.set()
    async with state.proxy() as data:
        data['telegram_id'] = message.from_user.id
    FSMClient.username.set()
    async with state.proxy() as data:
        data['username'] = message.from_user.first_name
    await FSMClient.name.set() 
    await message.answer('Введи имя')
 

async def reg_name(message: types.Message, state:FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await FSMClient.next()
    await message.answer('Введи фамилию')

async def reg_surname(message: types.Message, state:FSMContext):
    async with state.proxy() as data:
        data['surname'] = message.text
    await FSMClient.next()
    await message.answer('Введи номер класса')

async def reg_grade_num(message: types.Message, state:FSMContext):
    async with state.proxy() as data:
        data['grade_num'] = int(message.text)
    await FSMClient.next()
    await message.answer('Введи букву класса')

async def reg_grade_letter(message: types.Message, state:FSMContext):
    async with state.proxy() as data:
        data['grade_letter'] = message.text.upper()
    db.add_User(state)
    await state.finish()
    await message.answer('Спасибо!')
    


async def cancel(message: types.Message, state: FSMContext):
    await state.finish()
    await message.reply('OK')



def register_handlers_client(dp:Dispatcher):
    dp.register_message_handler(start, commands=['start'])
    dp.register_message_handler(register, commands=['register'] ,state=None)
    dp.register_message_handler(reg_name, state=FSMClient.name)
    dp.register_message_handler(reg_surname, state=FSMClient.surname)
    dp.register_message_handler(reg_grade_num, state=FSMClient.grade_num)
    dp.register_message_handler(reg_grade_letter, state=FSMClient.grade_letter)
    dp.register_message_handler(cancel, state="*", commands=['отмена', 'cancel'])
    dp.register_message_handler(cancel, Text(equals='отмена', ignore_case=True),state="*")
    