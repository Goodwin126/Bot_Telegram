from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

b1 = KeyboardButton("Режим работы")
b2 = KeyboardButton("Расположение")
b3 = KeyboardButton("Услуги")
b4 = KeyboardButton("БЖУ")

kb_client = ReplyKeyboardMarkup(resize_keyboard=True)

kb_client.row(b1,b2,b3).row(b4)