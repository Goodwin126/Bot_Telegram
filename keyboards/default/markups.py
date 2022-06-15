from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

btnMain = KeyboardButton("⬅Главное меню")


#Превое меню калорийность или Бжу

btnRandom = KeyboardButton("Каллорийность📈")
btnOther = KeyboardButton('ПРИЁМ ПИЩИ🍴(КБЖУ)')
meinMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(btnRandom, btnOther)
#Второе меню мужчина или женщина

btnInfo = KeyboardButton('Мужчина')
btnMany = KeyboardButton("Женщина")
btnback = KeyboardButton("Назад")
genderMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(btnInfo,btnMany,btnback)

#ввведите ваш вес, далее, назад
btnMany = KeyboardButton("Назад")
weightMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(btnMany)


#ввведите ваш рост, далее, назад
btnMany = KeyboardButton("Назад")
heightMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(btnMany)


#ввведите ваш возраст, далее, назад
btnMany = KeyboardButton("Назад")
ageMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(btnMany)

#ввведите ваш возраст, далее, назад
btn1 = KeyboardButton('не тренируюсь')
btn2 = KeyboardButton("1-3 раза в неделю")
btn3 = KeyboardButton("4-5 раз в неделю")
btn4 = KeyboardButton("6-7 дней в неделю")
btn5 = KeyboardButton("1-2 раза в день")
btnback = KeyboardButton("Назад")
btnback2 = KeyboardButton("⬅в главному меню")
ActiveMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(btn1,btn2,btn3,btn4,btn5,btnback,btnback2)

btn6 = KeyboardButton('похудеть 🥑')
btn7 = KeyboardButton('набрать 💪🏻')
btnback = KeyboardButton("Назад")
btnback2 = KeyboardButton("⬅в главному меню")

ActiveMenu2 = ReplyKeyboardMarkup(resize_keyboard=True).add(btn6,btn7,btnback2)

btn8 = KeyboardButton('"Назад"')


dishMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(btn8,btnMain)
