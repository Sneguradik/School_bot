from aiogram import executor
from create import dp
from handlers import client, admin,other
from database import sqlite_db

async def on_startup(_):
    print('Bot online')
    sqlite_db.on_start()

client.register_handlers_client(dp)
admin.register_handlers_admin(dp)

if __name__=='__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)