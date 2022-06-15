from aiogram import types, Dispatcher
from aiogram.dispatcher.storage import FSMContext
from keyboards.default.markups import meinMenu, genderMenu, weightMenu, heightMenu, ageMenu, ActiveMenu, ActiveMenu2
from loader import dp
from states import Test


@dp.message_handler(text="БЖУ")  # по команде test начнется порос
async def enter_test(message: types.Message):
    await message.answer("БЖУ", reply_markup=meinMenu)



@dp.message_handler(text="Каллорийность📈")  # фильтр ответа на первый вопрос
async def answer_q1(message: types.Message, state: FSMContext):
    answer = message.text  # добавляем переменную для хранения ответа на первый вопрос
    await state.update_data(answer1=answer)  # сохраняем ответ на первый вопрос в машину остояния
    first_name = message.from_user.first_name
    await message.answer(f'{first_name}, давайте посчитаем \n вашу суточную норму каллрий'.format(message.from_user))
    await message.answer("Выберите ваш пол", reply_markup=genderMenu)  # отправляем сообщение со вторым вопросом
    await Test.Q1.set()  # вводи пользователя в состояние ответа на второй вопрос

@dp.message_handler(text='Назад', state=Test.Q1)  # фильтр ответа на второй вопрос
async def answer_q1_2(message: types.Message, state: FSMContext):
    if message.text == "Назад":
        await message.delete()
        await message.answer("⬅ Назад", reply_markup=meinMenu)
        await state.finish()


@dp.message_handler(text='Мужчина', state=Test.Q1)  # фильтр ответа на второй вопрос
async def answer_q2(message: types.Message, state: FSMContext):
    answer2 = message.text  # добавляем переменную для хранения ответа на второй вопрос
    if message.text == 'Мужчина':
        x = 88.36
        await state.update_data(x=x)  # сохраняет переменную х
        await state.update_data(answer2=answer2)  # сохраняем ответ на второй вопрос в машину остояния
        await message.answer("Введите пожалуйста ваш вес(кг)",
                             reply_markup=weightMenu)  # отправляем сообщение со третьем вопросом
        await Test.Q2.set()  # вводи пользователя в состояние ответа на третий вопрос


@dp.message_handler(text='Женщина', state=Test.Q1)  # фильтр ответа на второй вопрос
async def answer_q3(message: types.Message, state: FSMContext):
    answer2 = message.text  # добавляем переменную для хранения ответа на второй вопрос
    if message.text == "Женщина":
        x = 447.6
        await state.update_data(x=x)  # сохраняет переменную х
        await state.update_data(answer2=answer2)  # сохраняем ответ на второй вопрос в машину остояния
        await message.answer("Введите пожалуйста ваш вес(кг)",
                             reply_markup=weightMenu)  # отправляем сообщение со третьем вопросом
        await Test.Q2.set()  # вводи пользователя в состояние ответа на третий вопрос

@dp.message_handler(text='Назад', state=Test.Q2)  # фильтр ответа на второй вопрос
async def answer_q3_2(message: types.Message, state: FSMContext):
    if message.text == "Назад":
        await message.answer("Выберите ваш пол", reply_markup=genderMenu)
        await Test.Q1.set()



@dp.message_handler(state=Test.Q2)  # фильтр ответа на второй вопрос
async def answer_q4(message: types.Message, state: FSMContext):
    message.text = str(message.text)
    if message.text.isnumeric():
        y = message.text  # добавляем переменную для хранения ответа на третий вопрос
        await state.update_data(y=y)  # сохраняем ответ на третий вопрос в машину остояни
        await message.answer("Введите пожалуйста ваш рост(см)",
                             reply_markup=heightMenu)  # отправляем сообщение с четвертым вопросом
        await Test.Q3.set()  # вводи пользователя в состояние ответа на второй вопрос
    else:
        await message.answer("Некорректный ввод, попробуте ещё раз", reply_markup=weightMenu)


@dp.message_handler(text='Назад', state=Test.Q3)  # фильтр ответа на второй вопрос
async def answer_q4_2(message: types.Message, state: FSMContext):
    if message.text == "Назад":
        await message.answer("Введите пожалуйста ваш вес(кг)", reply_markup=weightMenu)
        await Test.Q2.set()


@dp.message_handler(state=Test.Q3)  # фильтр ответа на второй вопрос
async def answer_q5(message: types.Message, state: FSMContext):
    message.text = str(message.text)
    if message.text.isnumeric():
        z = message.text  # добавляем переменную для хранения ответа на третий вопрос
        await state.update_data(z=z)  # сохраняем ответ на третий вопрос в машину остояни
        await message.answer("Введите пожалуйста ваш возраст(лет)",
                             reply_markup=ageMenu)  # отправляем сообщение с четвертым вопросом
        await Test.Q4.set()  # вводи пользователя в состояние ответа на второй вопрос
    else:
        await message.answer("Некорректный ввод, попробуте ещё раз", reply_markup=heightMenu)

@dp.message_handler(text='Назад', state=Test.Q4)  # фильтр ответа на второй вопрос
async def answer_q5_2(message: types.Message, state: FSMContext):
    if message.text == "Назад":
        await message.answer("Введите пожалуйста ваш рост(см)", reply_markup=heightMenu)
        await Test.Q3.set()




@dp.message_handler(state=Test.Q4)  # фильтр ответа на второй вопрос
async def answer_q6(message: types.Message, state: FSMContext):
    message.text = str(message.text)
    if message.text.isnumeric():
        age = message.text  # добавляем переменную для хранения ответа на третий вопрос
        await state.update_data(age=age)  # сохраняем ответ на третий вопрос в машину остояни
        await message.answer("Как часто вы тренируетесь? выберите подходящий ответ",
                             reply_markup=ActiveMenu)  # отправляем сообщение с четвертым вопросом
        await Test.Q5.set()  # вводи пользователя в состояние ответа на второй вопрос
    else:
        await message.answer("Некорректный ввод, попробуте ещё раз", reply_markup=ageMenu)

@dp.message_handler(text='Назад', state=Test.Q5)  # фильтр ответа на второй вопрос
async def answer_q6_2(message: types.Message, state: FSMContext):
    if message.text == "Назад":
        await message.answer("Введите пожалуйста ваш возраст(лет)", reply_markup=ageMenu)
        await Test.Q5.set()

@dp.message_handler(text='⬅в главному меню', state=Test.Q5)  # фильтр ответа на второй вопрос
async def answer_q1_2(message: types.Message, state: FSMContext):
    if message.text == "⬅в главному меню":
        await message.answer("⬅в главному меню", reply_markup=meinMenu)
        await Test.Q1.set()


@dp.message_handler(state=Test.Q5)  # фильтр ответа на второй вопрос
async def answer_q7(message: types.Message, state: FSMContext):
    if message.text == 'не тренируюсь':
        c1 = 1.2  # добавляем переменную для хранения ответа на третий вопрос
        await state.update_data(c1=c1)
        await Test.Q6.set()
    elif message.text == '1-3 раза в неделю':
        c1 = 1.375  # добавляем переменную для хранения ответа на третий вопрос
        await state.update_data(c1=c1)
        await Test.Q6.set()
    elif message.text == '4-5 раз в неделю':
        c1 = 1.55  # добавляем переменную для хранения ответа на третий вопрос
        await state.update_data(c1=c1)
        await Test.Q6.set()
    elif message.text == '6-7 дней в неделю':
        c1 = 1.725  # добавляем переменную для хранения ответа на третий вопрос
        await state.update_data(c1=c1)
        await Test.Q6.set()
    elif message.text == '1-2 раза в день':
        c1 = 1.9  # добавляем переменную для хранения ответа на третий вопрос
        await state.update_data(c1=c1)
        await Test.Q6.set()
    else:
        await message.answer("Некорректный ввод, попробуте ещё раз", reply_markup=ActiveMenu)
    first_name = message.from_user.first_name
    data = await state.get_data()
    x = data.get("x")
    y = float(data.get("y"))
    z = float(data.get("z"))
    age = float(data.get("age"))
    c1 = float(data.get("c1"))
    if x == 88.36:
        x = (x + (13.4 * y) + (4.8 * z) - (5.7 * age))
        x = round(x * c1,2)
        await state.update_data(x=x)
        belok = round(x / 100 * 30, 1)
        gyr = round(x / 100 * 20, 1)
        ygl = round(x / 100 * 50, 1)
        await message.answer(f'{first_name}' + ", <b>ваша суточноя норма \nкалорий составляет: </b>" + str(x) +
                             " ккал.\n" "белка: " + str(belok) + " ккал.\n" + "жиров: " + str(gyr) + " ккал.\n"
                             "углеводов: " + str(ygl) + " ккал.",
                               parse_mode='HTML', reply_markup=ActiveMenu2)
    if x == 447.6:
        x = (x + (9.2 * y) + (3.1 * z) - (4.3 * age))
        x = round(x * c1, 2)
        await state.update_data(x=x)
        belok = round(x / 100 * 30, 1)
        gyr = round(x / 100 * 20, 1)
        ygl = round(x / 100 * 50, 1)
        await message.answer(f'{first_name}' + ", <b>ваша суточноя норма \nкалорий составляет: </b>" + str(x) +
                             " ккал.\n" "белка: " + str(belok) + " ккал.\n" + "жиров: " + str(gyr) + " ккал.\n"
                             "углеводов: " + str(ygl) + " ккал.",
                               parse_mode='HTML', reply_markup=ActiveMenu2)

@dp.message_handler(text='⬅в главному меню', state=Test.Q6)  # фильтр ответа на второй вопрос
async def answer_q1_2(message: types.Message, state: FSMContext):
    if message.text == "⬅в главному меню":
        await message.answer("⬅в главному меню", reply_markup=meinMenu)
        await Test.Q1.set()


@dp.message_handler(state=Test.Q6)  # фильтр ответа на второй вопрос
async def answer_q8(message: types.Message, state: FSMContext):
    if message.text == 'набрать 💪🏻':
        message.text = str(message.text)
        first_name = message.from_user.first_name
        data = await state.get_data()
        x = data.get("x")
        a = round(x / 100 * 110, 1)
        b = round(x / 100 * 120, 1)
        belok = round(a / 100 * 30, 1)
        gyr = round(a / 100 * 25, 1)
        ygl = round(a / 100 * 45, 1)
        belok2 = round(b / 100 * 30, 1)
        gyr2 = round(b / 100 * 25, 1)
        ygl2 = round(b / 100 * 45, 1)
        await message.answer(f'{first_name}' +", <b>чтобы достичь цели,\nвам необходимо потреблять:</b> от " + str(a) + " до " + str(b) +
                               " ккал.\n""белка: от " + str(belok) + " до " + str(belok2) + " ккал.\n""жиров : от " + str(
                                   gyr) + " до " + str(gyr2) + " ккал.\n""углеводов: от " + str(ygl) + " до " + str(ygl2) + " ккал.",
                               parse_mode='HTML', reply_markup=ActiveMenu2)

    if message.text == 'похудеть 🥑':
        message.text = str(message.text)
        first_name = message.from_user.first_name
        data = await state.get_data()
        x = data.get("x")
        a = round(x / 100 * 90, 1)
        b = round(x / 100 * 80, 1)
        belok = round(a / 100 * 40, 1)
        gyr = round(a / 100 * 35, 1)
        ygl = round(a / 100 * 25, 1)
        belok2 = round(b / 100 * 40, 1)
        gyr2 = round(b / 100 * 35, 1)
        ygl2 = round(b / 100 * 25, 1)
        await message.answer(f'{first_name}' +", <b>чтобы достичь цели,\nвам необходимо потреблять:</b> от " + str(b) + " до " + str(a) +
                               " ккал.\n""белка: от " + str(belok2) + " до " + str(belok) + " ккал.\n""жиров : от " + str(
                                   gyr2) + " до " + str(gyr) + " ккал.\n""углеводов: от " + str(ygl2) + " до " + str(ygl) + " ккал.",
                               parse_mode='HTML', reply_markup=ActiveMenu2)



def register_handlers_testing(dp: Dispatcher):
    dp.register_message_handler(enter_test,text="БЖУ")
    dp.register_message_handler(answer_q1, text="Каллорийность")
    dp.register_message_handler(answer_q2, text='Мужчина', state=Test.Q1)
    dp.register_message_handler(answer_q3, text='Женщина', state=Test.Q1)
    dp.register_message_handler(answer_q4, state=Test.Q2)
    dp.register_message_handler(answer_q5, state=Test.Q3)
    dp.register_message_handler(answer_q6, state=Test.Q4)
    dp.register_message_handler(answer_q7, state=Test.Q5)
    dp.register_message_handler(answer_q8, state=Test.Q6)
