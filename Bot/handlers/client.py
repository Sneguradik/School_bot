from typing import Text
from aiogram import Dispatcher, types
from numpy import equal
from create import dp, bot
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
import database.sqlite_db as db 
from aiogram.dispatcher.filters import Text
from keyboards.client import *

class RegisterFMS(StatesGroup):
    telegram_id = State()
    username = State()
    name = State()
    surname = State()
    grade_num = State()
    grade_letter = State()
    status = State()


async def start(message: types.Message):
    if db.get_inf('Users', 'telegram_id', message.from_user.id):
        reply = f'Привет {message.from_user.first_name}'
        kb = kbc.kb
    else:
        reply = 'Привет! Это чат бот для организациитвоеё работы! Пожалуйста зарегистрируйся командой /register, если ты не зарегистрировался.'
        kb = kbr.kb
    await message.answer(reply, reply_markup=kb)

async def register(message: types.Message, state:FSMContext):
    RegisterFMS.telegram_id.set()
    async with state.proxy() as data:
        data['telegram_id'] = message.from_user.id
    RegisterFMS.username.set()
    async with state.proxy() as data:
        data['username'] = message.from_user.first_name
    await RegisterFMS.name.set() 
    await message.answer('Введи имя', reply_markup=ReplyKeyboardRemove())
 

async def reg_name(message: types.Message, state:FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await RegisterFMS.next()
    await message.answer('Введи фамилию')

async def reg_surname(message: types.Message, state:FSMContext):
    async with state.proxy() as data:
        data['surname'] = message.text
    await RegisterFMS.next()
    await message.answer('Введи номер класса')

async def reg_grade_num(message: types.Message, state:FSMContext):
    async with state.proxy() as data:
        data['grade_num'] = int(message.text)
    await RegisterFMS.next()
    await message.answer('Введи букву класса')

async def reg_grade_letter(message: types.Message, state:FSMContext):
    async with state.proxy() as data:
        data['grade_letter'] = message.text.upper()
    await db.add_User(state)
    await state.finish()
    await message.answer('Спасибо!', reply_markup=kbc.kb)

async def get_events(message: types.Message):
   
    data = db.get_inf('Events')
    if data:
        for i in data:
            response = f'Название ивента: {i[0]}\nОписание ивента: {i[1]}\nДата: {i[2]}'
            await message.answer(response)



def register_handlers_client(dp:Dispatcher):
    dp.register_message_handler(start, commands=['start'])
    dp.register_message_handler(register, commands=['register'] ,state=None)
    dp.register_message_handler(reg_name, state=RegisterFMS.name)
    dp.register_message_handler(reg_surname, state=RegisterFMS.surname)
    dp.register_message_handler(reg_grade_num, state=RegisterFMS.grade_num)
    dp.register_message_handler(reg_grade_letter, state=RegisterFMS.grade_letter)
    dp.register_message_handler(get_events, commands=['Events'])