from aiogram import executor
from data_base import sqlite_db
from data_base import sqlite_db_score
from loader import dp



async def on_startup(_):
    print('Бот вышел в онлайн')
    sqlite_db.sql_start()
    sqlite_db_score.sql_start()

from handlers import client,admin,score_admin,testing,other

client.register_handlers_client(dp)
admin.register_handlers_admin(dp)
score_admin.register_handlers_score_admin(dp)
testing.register_handlers_testing(dp)
other.register_handlers_other(dp)


executor.start_polling(dp, skip_updates=True, on_startup=on_startup)

