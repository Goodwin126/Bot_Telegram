from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# кнопки админа
button_load = KeyboardButton('/Загрузить')
button_delete = KeyboardButton('/Удалить')
button_sendall = KeyboardButton('/Cделать рассылку')


buttonc_case_admin = ReplyKeyboardMarkup(resize_keyboard = True).add(button_load)\
    .add(button_delete).add(button_sendall)