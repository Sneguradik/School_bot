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



def register_handlers_admin(dp:Dispatcher):
    dp.register_message_handler(reg_event, commands=['NewEvent'],state=None)
    dp.register_message_handler(reg_event_name ,state=EventFSM.name)
    dp.register_message_handler(reg_description, state = EventFSM.description)
    dp.register_message_handler(reg_date, state=EventFSM.date)