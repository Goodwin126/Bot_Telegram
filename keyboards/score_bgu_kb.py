from aiogram.types import ReplyKeyboardMarkup, KeyboardButton



btnRandom = KeyboardButton("посчитать")
btnOther = KeyboardButton("⬅ Назад")
meinMenuBGU = ReplyKeyboardMarkup(resize_keyboard=True).add(btnRandom, btnOther)