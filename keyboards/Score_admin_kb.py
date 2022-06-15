from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# кнопки админа
button_load = KeyboardButton('Загрузить')
button_delete = KeyboardButton('Удалить')


buttonc_case_admin = ReplyKeyboardMarkup(resize_keyboard = True).add(button_load)\
    .add(button_delete)