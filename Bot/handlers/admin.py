from typing import Text
from aiogram import Dispatcher, types
from numpy import equal
from create import dp, bot
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
import database.sqlite_db as db 
from aiogram.dispatcher.filters import Text
from keyboards.client import *

class EventFSM(StatesGroup):
    name = State()
    description = State()
    date = State()

class SendToClassFSM(StatesGroup):
    grade_num = State()
    grade_letter = State()
    text = State()

async def reg_event(message: types.Message, state:FSMContext):
    users = db.get_inf('Users', 'status', "teacher")
    
    if users:
        print(1)
        for user in users:
            print(2)
            if user[0] == message.from_user.id:
                print(3)
                await EventFSM.name.set()
                await message.answer('Введи название ивента')
            else:
                pass
    else:
        pass

async def reg_event_name(message: types.Message, state:FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await EventFSM.next()
    await message.answer('Введите описание ивента')

async def reg_description(message: types.Message, state:FSMContext):
    async with state.proxy() as data:
        data['description'] = message.text
    await EventFSM.next()
    await message.answer('Введите дату (YYYY-MM-DD HH:MM)')

async def reg_date(message: types.Message, state:FSMContext):
    async with state.proxy() as data:
        data['date'] = message.text
    await db.add_Event(state)
    await state.finish()
    await message.answer('Спасибо!')

async def send_to_class(message: types.Message, state:FSMContext):
    users = db.get_inf('Users', 'status', "teacher")
    
    if users:
        print(1)
        for user in users:
            print(2)
            if user[0] == message.from_user.id:
                print(3)
                await SendToClassFSM.grade_num.set()
                await message.answer('Введи номер класса')
            else:
                pass
    else:
        pass

async def get_class_grade(message: types.Message, state:FSMContext):
    async with state.proxy() as data:
        data['grade_num'] = int(message.text)
    await SendToClassFSM.next()
    await message.answer('Введите букву класса')

async def get_class_letter(message: types.Message, state:FSMContext):
    async with state.proxy() as data:
        data['grade_letter'] = message.text
    await SendToClassFSM.next()
    await message.answer('Введите текст сообщения')

async def get_text(message: types.Message, state:FSMContext):

    users = db.get_Grade(state)
    text = message.text
    print(users)
    for user in users:
        print(user)
        bot.send_message(user[0], text)
    await state.finish()
    await message.answer('Спасибо!')

def register_handlers_admin(dp:Dispatcher):
    dp.register_message_handler(reg_event, commands=['NewEvent'],state=None)
    dp.register_message_handler(reg_event_name ,state=EventFSM.name)
    dp.register_message_handler(reg_description, state = EventFSM.description)
    dp.register_message_handler(reg_date, state=EventFSM.date)
    dp.register_message_handler(send_to_class, commands=['SendToClass'], state=None)
    dp.register_message_handler(get_class_grade, state=SendToClassFSM.grade_num)
    dp.register_message_handler(get_class_letter, state=SendToClassFSM.grade_letter)
    dp.register_message_handler(get_text, state=SendToClassFSM.text)
