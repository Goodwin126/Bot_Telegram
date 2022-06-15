from aiogram import types, Dispatcher
from loader import dp, bot
from keyboards import kb_client
from data_base import sqlite_db
import logging
from data_base.db import Database


db = Database('database.db')

logging.basicConfig(level=logging.INFO)



@dp.message_handler(text=['/start'])
async def command_start(message: types.Message):
    try:
        if message.chat.type == 'private':
            if not db.user_exists(message.from_user.id):
                db.add_user(message.from_user.id)
                await bot.send_message(message.from_user.id, 'Добро пожаловать, {0.first_name}'.format(message.from_user))

        await bot.send_message("Общение с ботом через ЛС,\n {0.first_name} напишите пожалуйста ему: \n  https://t.me/igoodwin_bot".format(message.from_user))
    except:
        await bot.send_message(message.from_user.id," {0.first_name} Добро пожаловать,\n выберите интерусующий \n вас раздел в меню⬇".format(message.from_user),parse_mode='HTML', reply_markup=kb_client)


@dp.message_handler(text="Режим работы")
async def salon_open_command(message: types.Message):
    await bot.send_message(message.from_user.id, "Сеансы идут по записи, Пт-Сб с 8:00 до 21:00")

@dp.message_handler(text="Расположение")
async def salon_place_command(message: types.Message):
    await bot.send_message(message.from_user.id, "Адрес: ул. Гагарина 47В, \"Тур Плаза\",\n (там где Мистер Фримэн),"
                                                 " 3 этаж, \n вход со стороны магазина \"Геркулес\"")

@dp.message_handler(text='Услуги')
async def salon_menu_command(message: types.Message):
    await sqlite_db.sql_read(message)

@dp.message_handler(commands=['sendall'])
async def sendall(message: types.Message):
    if message.chat.type == 'private':
        if message.from_user.id == 377288092:
            text = message.text[9:]
            users = db.get_users()
            for row in users:
                try:
                    await bot.send_message(row[0],text)
                    if int(row[1]) != 1:
                        db.set_active(row[0], 1)
                except:
                    db.set_active(row[0],0)
            await bot.send_message(message.from_user.id, "Успешная рассылка ")





def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start','help'])
    dp.register_message_handler(salon_open_command, commands=["Режим_работы"])
    dp.register_message_handler(salon_place_command,commands=["Расположение"])
    dp.register_message_handler(salon_menu_command,commands=['Услуги'])









