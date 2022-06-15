from aiogram.dispatcher import FSMContext
from loader import dp, bot
from aiogram import types
from states import Score
from keyboards.default.markups import meinMenu
from keyboards import score_bgu_kb
from data_base import sqlite_db_score
import string
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.filters import Text


@dp.message_handler(text='ПРИЁМ ПИЩИ🍴(КБЖУ)')
async def start_score(message: types.Message):
    first_name = message.from_user.first_name
    await Score.V1.set()  # вводим в сотояние ответа на первый вопрос
    await message.answer(f'{first_name}, давайте посчитаем БЖУ вашего блюда,'
                         f' введите название первого '
                         f'ингридиента'.format(message.from_user),reply_markup=score_bgu_kb.meinMenuBGU)

#СЧИТАЕМ КАЛОРИИ, ПОДВОДИМ ИТОГ
@dp.message_handler(state="*", commands='посчитать')
@dp.message_handler(Text(equals='посчитать', ignore_case=True), state="*")
async def score_finich_handler(message: types.Message, state: FSMContext):
    try:
        current_state = await state.get_state()
        data = await state.get_data()
        A1 = float(data.get("result1")) #выгружаем A1 и считаем
        A2 = float(data.get("result2")) #выгружаем A2 и считаем
        A3 = float(data.get("result3")) #выгружаем A3 и считаем
        A4 = float(data.get("result4")) #выгружаем A4 и считаем
        A1 = round(A1, 2) #округляем до 2 знаков после запятой
        A2 = round(A2, 2) #округляем до 2 знаков после запятой
        A3 = round(A3, 2) #округляем до 2 знаков после запятой
        A4 = round(A4, 2) #округляем до 2 знаков после запятой
        await bot.send_message(message.from_user.id, f'<b>Блюдо состоит из: </b>'
        f''+str(A1)+' г. белка, '+str(A2)+' г. жиров, '+str(A3)+' г. углеводов. \n<b>Итого :</b>'+str(A4)+' ккал.',parse_mode='HTML',reply_markup=meinMenu)
        if current_state is None:
            return
        await state.finish()
    except:
        pass
@dp.message_handler(state="*", commands='⬅ Назад')
@dp.message_handler(Text(equals='⬅ Назад', ignore_case=True), state="*")
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.delete()
    await message.answer("⬅ Назад",reply_markup=meinMenu)


#ИЩЕМ ПЕРВЫЙ ИНГРИДИЕНТ
@dp.message_handler(state=Score.V1)
async def score_1(message: types.Message):
    try:
        if not message.text.isnumeric(): #проверка на то что это не число
            read = await sqlite_db_score.sql_read2() #выбираем данные из БД ингридиентов
            for ret in read: #перебираем массив с ингридиентами
                for i in ret: #перебираем с данными внутри ингридиентов
                    if i.lower().startswith(message.text.lower().translate(str.maketrans("","",string.punctuation))):
                    #if message.text.lower().translate(str.maketrans("","",string.punctuation)) in i.lower():
                        await bot.send_message(message.from_user.id,f'<b>{ret[0]} </b>, состав: {ret[1]} г., белка, {ret[2]} г., жиров, {ret[3]} г., углеводов, {ret[4]}  ккал.',parse_mode='HTML',reply_markup=InlineKeyboardMarkup().\
                                        add(InlineKeyboardButton(f'Добавить "{ret[0]}"',callback_data=ret[0])))
        else:
            await message.answer("Некорректный ввод, попробуте ещё раз")
    except:
        pass

#вытаскиваем данные и сохраняем в машину состояний
@dp.callback_query_handler(state=Score.V1)
async def del_callback_run1(callback_query: types.CallbackQuery, state: FSMContext):
    read = await sqlite_db_score.sql_read2()
    for ret in read:
        for i in ret:
            if i == callback_query.data:
                await state.update_data(A1=ret[1])#сохраняем ответ в машину состояний
                await state.update_data(A2=ret[2])#сохраняем ответ в машину состояний
                await state.update_data(A3=ret[3])#сохраняем ответ в машину состояний
                await state.update_data(A4=ret[4])#сохраняем ответ в машину состояний
                await Score.V2.set()
                await callback_query.answer(text=f'"{callback_query.data}" добавлено,\nсколько в граммах?', show_alert=True)
#вводим грамаж, считаем грамаж и сохраняем в машину состояний
@dp.message_handler(state=Score.V2)
async def score_2(message: types.Message, state: FSMContext):
    if message.text.isnumeric():
        gramm = float(message.text)
        data = await state.get_data()
        A1 = (float(data.get("A1"))) / 100 * gramm #выгружаем A1 и считаем
        A2 = (float(data.get("A2"))) / 100 * gramm #выгружаем A2 и считаем
        A3 = (float(data.get("A3"))) / 100 * gramm #выгружаем A3 и считаем
        A4 = (float(data.get("A4"))) / 100 * gramm #выгружаем A4 и считаем
        await state.update_data(result1=A1)  # сохраняем ответ в машину состояний
        await state.update_data(result2=A2)  # сохраняем ответ в машину состояний
        await state.update_data(result3=A3)  # сохраняем ответ в машину состояний
        await state.update_data(result4=A4)  # сохраняем ответ в машину состояний
        await Score.V3.set()
        await bot.send_message(message.from_user.id,'введите название второго ингридиента')
    else:
        await message.answer("Некорректный ввод, попробуте ещё раз, напишите количество в граммах?")


#ИЩЕМ ВТОРОЙ ИНГРИДИЕНТ
@dp.message_handler(state=Score.V3)
async def score_3(message: types.Message):
    try:
        if not message.text.isnumeric(): #проверка на то что это не число
            read = await sqlite_db_score.sql_read2() #выбираем данные из БД ингридиентов
            for ret in read: #перебираем массив с ингридиентами
                for i in ret: #перебираем с данными внутри ингридиентов
                    if i.lower().translate(str.maketrans("", "", string.punctuation)).find(message.text.lower()) != -1:
                        await bot.send_message(message.from_user.id,
                                             f'<b>{ret[0]} </b>, состав: {ret[1]} г., белка, {ret[2]} г., жиров, {ret[3]} г., углеводов, {ret[4]}  ккал.'
                                                f'',parse_mode='HTML',reply_markup=InlineKeyboardMarkup().\
                                        add(InlineKeyboardButton(f'Добавить "{ret[0]}"',callback_data=ret[0])))
        else:
            await message.answer("Некорректный ввод, попробуте ещё раз")
    except:
        pass
#вытаскиваем данные и сохраняем в машину состояний
@dp.callback_query_handler(state=Score.V3)
async def del_callback_run2(callback_query: types.CallbackQuery, state: FSMContext):
    read = await sqlite_db_score.sql_read2()
    for ret in read:
        for i in ret:
            if i == callback_query.data:
                await state.update_data(A1=ret[1])#сохраняем ответ в машину состояний
                await state.update_data(A2=ret[2])#сохраняем ответ в машину состояний
                await state.update_data(A3=ret[3])#сохраняем ответ в машину состояний
                await state.update_data(A4=ret[4])#сохраняем ответ в машину состояний
                await Score.V4.set()
                await callback_query.answer(text=f'"{callback_query.data}" добавлено,\nсколько в граммах?', show_alert=True)
#вводим грамаж, считаем грамаж и сохраняем в машину состояний
@dp.message_handler(state=Score.V4)
async def score_4(message: types.Message, state: FSMContext):
    if message.text.isnumeric():
        gramm = float(message.text)
        data = await state.get_data()
        A1 = ((float(data.get("A1"))) / 100 * gramm) + (float(data.get("result1"))) #выгружаем A1 и result2, считаем
        A2 = ((float(data.get("A2"))) / 100 * gramm) + (float(data.get("result2"))) #выгружаем A2 и result2, считаем
        A3 = ((float(data.get("A3"))) / 100 * gramm) + (float(data.get("result3"))) #выгружаем A3 и result3, считаем
        A4 = ((float(data.get("A4"))) / 100 * gramm) + (float(data.get("result4"))) #выгружаем A4 и result4, считаем
        await state.update_data(result1=A1)  # сохраняем ответ в машину состояний
        await state.update_data(result2=A2)  # сохраняем ответ в машину состояний
        await state.update_data(result3=A3)  # сохраняем ответ в машину состояний
        await state.update_data(result4=A4)  # сохраняем ответ в машину состояний
        await Score.V5.set()
        await bot.send_message(message.from_user.id,'введите название третьего ингридиента')
    else:
        await message.answer("Некорректный ввод, попробуте ещё раз, напишите количество в граммах?")

#ИЩЕМ ТРЕТИЙ ИНГРИДИЕНТ
@dp.message_handler(state=Score.V5)
async def score_5(message: types.Message):
    try:
        if not message.text.isnumeric(): #проверка на то что это не число
            read = await sqlite_db_score.sql_read2() #выбираем данные из БД ингридиентов
            for ret in read: #перебираем массив с ингридиентами
                for i in ret: #перебираем с данными внутри ингридиентов
                    if i.lower().translate(str.maketrans("", "", string.punctuation)).find(message.text.lower()) != -1:
                        await bot.send_message(message.from_user.id,
                                            f'<b>{ret[0]} </b>, состав: {ret[1]} г., белка, {ret[2]} г., жиров, {ret[3]} г., углеводов, {ret[4]}  ккал.'
                                                f'',parse_mode='HTML',reply_markup=InlineKeyboardMarkup().\
                                        add(InlineKeyboardButton(f'Добавить "{ret[0]}"',callback_data=ret[0])))
        else:
            await message.answer("Некорректный ввод, попробуте ещё раз")
    except:
        pass
#вытаскиваем данные и сохраняем в машину состояний
@dp.callback_query_handler(state=Score.V5)
async def del_callback_run3(callback_query: types.CallbackQuery, state: FSMContext):
    read = await sqlite_db_score.sql_read2()
    for ret in read:
        for i in ret:
            if i == callback_query.data:
                await state.update_data(A1=ret[1])#сохраняем ответ в машину состояний
                await state.update_data(A2=ret[2])#сохраняем ответ в машину состояний
                await state.update_data(A3=ret[3])#сохраняем ответ в машину состояний
                await state.update_data(A4=ret[4])#сохраняем ответ в машину состояний
                await Score.V6.set()
                await callback_query.answer(text=f'"{callback_query.data}" добавлено,\nсколько в граммах?', show_alert=True)
#вводим грамаж, считаем грамаж и сохраняем в машину состояний
@dp.message_handler(state=Score.V6)
async def score_6(message: types.Message, state: FSMContext):
    if message.text.isnumeric():
        gramm = float(message.text)
        data = await state.get_data()
        A1 = ((float(data.get("A1"))) / 100 * gramm) + (float(data.get("result1"))) #выгружаем A1 и result2, считаем
        A2 = ((float(data.get("A2"))) / 100 * gramm) + (float(data.get("result2"))) #выгружаем A2 и result2, считаем
        A3 = ((float(data.get("A3"))) / 100 * gramm) + (float(data.get("result3"))) #выгружаем A3 и result3, считаем
        A4 = ((float(data.get("A4"))) / 100 * gramm) + (float(data.get("result4"))) #выгружаем A4 и result4, считаем
        await state.update_data(result1=A1)  # сохраняем ответ в машину состояний
        await state.update_data(result2=A2)  # сохраняем ответ в машину состояний
        await state.update_data(result3=A3)  # сохраняем ответ в машину состояний
        await state.update_data(result4=A4)  # сохраняем ответ в машину состояний
        await Score.V7.set()
        await bot.send_message(message.from_user.id,'введите название четвертого ингридиента')
    else:
        await message.answer("Некорректный ввод, попробуте ещё раз, напишите количество в граммах?")

#ИЩЕМ ЧЕТВЕРТЫЙ ИНГРИДИЕНТ
@dp.message_handler(state=Score.V7)
async def score_7(message: types.Message):
    try:
        if not message.text.isnumeric(): #проверка на то что это не число
            read = await sqlite_db_score.sql_read2() #выбираем данные из БД ингридиентов
            for ret in read: #перебираем массив с ингридиентами
                for i in ret: #перебираем с данными внутри ингридиентов
                    if i.lower().translate(str.maketrans("", "", string.punctuation)).find(message.text.lower()) != -1:
                        await bot.send_message(message.from_user.id,
                                            f'<b>{ret[0]} </b>, состав: {ret[1]} г., белка, {ret[2]} г., жиров, {ret[3]} г., углеводов, {ret[4]}  ккал.'
                                                f'',parse_mode='HTML',reply_markup=InlineKeyboardMarkup().\
                                        add(InlineKeyboardButton(f'Добавить "{ret[0]}"',callback_data=ret[0])))
        else:
            await message.answer("Некорректный ввод, попробуте ещё раз")
    except:
        pass
#вытаскиваем данные и сохраняем в машину состояний
@dp.callback_query_handler(state=Score.V7)
async def del_callback_run4(callback_query: types.CallbackQuery, state: FSMContext):
    read = await sqlite_db_score.sql_read2()
    for ret in read:
        for i in ret:
            if i == callback_query.data:
                await state.update_data(A1=ret[1])#сохраняем ответ в машину состояний
                await state.update_data(A2=ret[2])#сохраняем ответ в машину состояний
                await state.update_data(A3=ret[3])#сохраняем ответ в машину состояний
                await state.update_data(A4=ret[4])#сохраняем ответ в машину состояний
                await Score.V8.set()
                await callback_query.answer(text=f'"{callback_query.data}" добавлено,\nсколько в граммах?', show_alert=True)
#вводим грамаж, считаем грамаж и сохраняем в машину состояний
@dp.message_handler(state=Score.V8)
async def score_8(message: types.Message, state: FSMContext):
    if message.text.isnumeric():
        gramm = float(message.text)
        data = await state.get_data()
        A1 = ((float(data.get("A1"))) / 100 * gramm) + (float(data.get("result1"))) #выгружаем A1 и result2, считаем
        A2 = ((float(data.get("A2"))) / 100 * gramm) + (float(data.get("result2"))) #выгружаем A2 и result2, считаем
        A3 = ((float(data.get("A3"))) / 100 * gramm) + (float(data.get("result3"))) #выгружаем A3 и result3, считаем
        A4 = ((float(data.get("A4"))) / 100 * gramm) + (float(data.get("result4"))) #выгружаем A4 и result4, считаем
        await state.update_data(result1=A1)  # сохраняем ответ в машину состояний
        await state.update_data(result2=A2)  # сохраняем ответ в машину состояний
        await state.update_data(result3=A3)  # сохраняем ответ в машину состояний
        await state.update_data(result4=A4)  # сохраняем ответ в машину состояний
        await Score.V9.set()
        await bot.send_message(message.from_user.id,'введите название пятого ингридиента')
    else:
        await message.answer("Некорректный ввод, попробуте ещё раз, напишите количество в граммах?")

#ИЩЕМ ПЯТЫЙ ИНГРИДИЕНТ
@dp.message_handler(state=Score.V9)
async def score_9(message: types.Message):
    try:
        if not message.text.isnumeric(): #проверка на то что это не число
            read = await sqlite_db_score.sql_read2() #выбираем данные из БД ингридиентов
            for ret in read: #перебираем массив с ингридиентами
                for i in ret: #перебираем с данными внутри ингридиентов
                    if i.lower().translate(str.maketrans("", "", string.punctuation)).find(message.text.lower()) != -1:
                        await bot.send_message(message.from_user.id,
                                               f'<b>{ret[0]} </b>, состав: {ret[1]} г., белка, {ret[2]} г., жиров, {ret[3]} г., углеводов, {ret[4]}  ккал.'
                                                f'',parse_mode='HTML',reply_markup=InlineKeyboardMarkup().\
                                        add(InlineKeyboardButton(f'Добавить "{ret[0]}"',callback_data=ret[0])))
        else:
            await message.answer("Некорректный ввод, попробуте ещё раз")
    except:
        pass
#вытаскиваем данные и сохраняем в машину состояний
@dp.callback_query_handler(state=Score.V9)
async def del_callback_run5(callback_query: types.CallbackQuery, state: FSMContext):
    read = await sqlite_db_score.sql_read2()
    for ret in read:
        for i in ret:
            if i == callback_query.data:
                await state.update_data(A1=ret[1])#сохраняем ответ в машину состояний
                await state.update_data(A2=ret[2])#сохраняем ответ в машину состояний
                await state.update_data(A3=ret[3])#сохраняем ответ в машину состояний
                await state.update_data(A4=ret[4])#сохраняем ответ в машину состояний
                await Score.V10.set()
                await callback_query.answer(text=f'"{callback_query.data}" добавлено,\nсколько в граммах?', show_alert=True)
#вводим грамаж, считаем грамаж и сохраняем в машину состояний
@dp.message_handler(state=Score.V10)
async def score_10(message: types.Message, state: FSMContext):
    if message.text.isnumeric():
        gramm = float(message.text)
        data = await state.get_data()
        A1 = ((float(data.get("A1"))) / 100 * gramm) + (float(data.get("result1"))) #выгружаем A1 и result2, считаем
        A2 = ((float(data.get("A2"))) / 100 * gramm) + (float(data.get("result2"))) #выгружаем A2 и result2, считаем
        A3 = ((float(data.get("A3"))) / 100 * gramm) + (float(data.get("result3"))) #выгружаем A3 и result3, считаем
        A4 = ((float(data.get("A4"))) / 100 * gramm) + (float(data.get("result4"))) #выгружаем A4 и result4, считаем
        await state.update_data(result1=A1)  # сохраняем ответ в машину состояний
        await state.update_data(result2=A2)  # сохраняем ответ в машину состояний
        await state.update_data(result3=A3)  # сохраняем ответ в машину состояний
        await state.update_data(result4=A4)  # сохраняем ответ в машину состояний
        await Score.V11.set()
        await bot.send_message(message.from_user.id,'введите название шестого ингридиента')
    else:
        await message.answer("Некорректный ввод, попробуте ещё раз, напишите количество в граммах?")

#ИЩЕМ ШЕТСТОЙ ИНГРИДИЕНТ
@dp.message_handler(state=Score.V11)
async def score_11(message: types.Message):
    try:
        if not message.text.isnumeric(): #проверка на то что это не число
            read = await sqlite_db_score.sql_read2() #выбираем данные из БД ингридиентов
            for ret in read: #перебираем массив с ингридиентами
                for i in ret: #перебираем с данными внутри ингридиентов
                    if i.lower().translate(str.maketrans("", "", string.punctuation)).find(message.text.lower()) != -1:
                        await bot.send_message(message.from_user.id,
                                             f'<b>{ret[0]} </b>, состав: {ret[1]} г., белка, {ret[2]} г., жиров, {ret[3]} г., углеводов, {ret[4]}  ккал.'
                                                f'',parse_mode='HTML',reply_markup=InlineKeyboardMarkup().\
                                        add(InlineKeyboardButton(f'Добавить "{ret[0]}"',callback_data=ret[0])))
        else:
            await message.answer("Некорректный ввод, попробуте ещё раз")
    except:
        pass
#вытаскиваем данные и сохраняем в машину состояний
@dp.callback_query_handler(state=Score.V11)
async def del_callback_run6(callback_query: types.CallbackQuery, state: FSMContext):
    read = await sqlite_db_score.sql_read2()
    for ret in read:
        for i in ret:
            if i == callback_query.data:
                await state.update_data(A1=ret[1])#сохраняем ответ в машину состояний
                await state.update_data(A2=ret[2])#сохраняем ответ в машину состояний
                await state.update_data(A3=ret[3])#сохраняем ответ в машину состояний
                await state.update_data(A4=ret[4])#сохраняем ответ в машину состояний
                await Score.V12.set()
                await callback_query.answer(text=f'"{callback_query.data}" добавлено,\nсколько в граммах?', show_alert=True)
#вводим грамаж, считаем грамаж и сохраняем в машину состояний
@dp.message_handler(state=Score.V12)
async def score_12(message: types.Message, state: FSMContext):
    if message.text.isnumeric():
        gramm = float(message.text)
        data = await state.get_data()
        A1 = ((float(data.get("A1"))) / 100 * gramm) + (float(data.get("result1"))) #выгружаем A1 и result2, считаем
        A2 = ((float(data.get("A2"))) / 100 * gramm) + (float(data.get("result2"))) #выгружаем A2 и result2, считаем
        A3 = ((float(data.get("A3"))) / 100 * gramm) + (float(data.get("result3"))) #выгружаем A3 и result3, считаем
        A4 = ((float(data.get("A4"))) / 100 * gramm) + (float(data.get("result4"))) #выгружаем A4 и result4, считаем
        await state.update_data(result1=A1)  # сохраняем ответ в машину состояний
        await state.update_data(result2=A2)  # сохраняем ответ в машину состояний
        await state.update_data(result3=A3)  # сохраняем ответ в машину состояний
        await state.update_data(result4=A4)  # сохраняем ответ в машину состояний
        await Score.V13.set()
        await bot.send_message(message.from_user.id,'введите название седьмого ингридиента')
    else:
        await message.answer("Некорректный ввод, попробуте ещё раз, напишите количество в граммах?")

#ИЩЕМ СЕДЬМОЙ ИНГРИДИЕНТ
@dp.message_handler(state=Score.V13)
async def score_13(message: types.Message):
    try:
        if not message.text.isnumeric(): #проверка на то что это не число
            read = await sqlite_db_score.sql_read2() #выбираем данные из БД ингридиентов
            for ret in read: #перебираем массив с ингридиентами
                for i in ret: #перебираем с данными внутри ингридиентов
                    if i.lower().translate(str.maketrans("", "", string.punctuation)).find(message.text.lower()) != -1:
                        await bot.send_message(message.from_user.id,
                                            f'<b>{ret[0]} </b>, состав: {ret[1]} г., белка, {ret[2]} г., жиров, {ret[3]} г., углеводов, {ret[4]}  ккал.'
                                                f'',parse_mode='HTML',reply_markup=InlineKeyboardMarkup().\
                                        add(InlineKeyboardButton(f'Добавить "{ret[0]}"',callback_data=ret[0])))
        else:
            await message.answer("Некорректный ввод, попробуте ещё раз")
    except:
        pass
#вытаскиваем данные и сохраняем в машину состояний
@dp.callback_query_handler(state=Score.V13)
async def del_callback_run7(callback_query: types.CallbackQuery, state: FSMContext):
    read = await sqlite_db_score.sql_read2()
    for ret in read:
        for i in ret:
            if i == callback_query.data:
                await state.update_data(A1=ret[1])#сохраняем ответ в машину состояний
                await state.update_data(A2=ret[2])#сохраняем ответ в машину состояний
                await state.update_data(A3=ret[3])#сохраняем ответ в машину состояний
                await state.update_data(A4=ret[4])#сохраняем ответ в машину состояний
                await Score.V14.set()
                await callback_query.answer(text=f'"{callback_query.data}" добавлено,\nсколько в граммах?', show_alert=True)
#вводим грамаж, считаем грамаж и сохраняем в машину состояний
@dp.message_handler(state=Score.V14)
async def score_14(message: types.Message, state: FSMContext):
    if message.text.isnumeric():
        gramm = float(message.text)
        data = await state.get_data()
        A1 = ((float(data.get("A1"))) / 100 * gramm) + (float(data.get("result1"))) #выгружаем A1 и result2, считаем
        A2 = ((float(data.get("A2"))) / 100 * gramm) + (float(data.get("result2"))) #выгружаем A2 и result2, считаем
        A3 = ((float(data.get("A3"))) / 100 * gramm) + (float(data.get("result3"))) #выгружаем A3 и result3, считаем
        A4 = ((float(data.get("A4"))) / 100 * gramm) + (float(data.get("result4"))) #выгружаем A4 и result4, считаем
        await state.update_data(result1=A1)  # сохраняем ответ в машину состояний
        await state.update_data(result2=A2)  # сохраняем ответ в машину состояний
        await state.update_data(result3=A3)  # сохраняем ответ в машину состояний
        await state.update_data(result4=A4)  # сохраняем ответ в машину состояний
        await Score.V15.set()
        await bot.send_message(message.from_user.id,'введите название восьмого ингридиента')
    else:
        await message.answer("Некорректный ввод, попробуте ещё раз, напишите количество в граммах?")

#ИЩЕМ ВОСЬМОЙ ИНГРИДИЕНТ
@dp.message_handler(state=Score.V15)
async def score_15(message: types.Message):
    try:
        if not message.text.isnumeric(): #проверка на то что это не число
            read = await sqlite_db_score.sql_read2() #выбираем данные из БД ингридиентов
            for ret in read: #перебираем массив с ингридиентами
                for i in ret: #перебираем с данными внутри ингридиентов
                    if i.lower().translate(str.maketrans("", "", string.punctuation)).find(message.text.lower()) != -1:
                        await bot.send_message(message.from_user.id,
                                             f'<b>{ret[0]} </b>, состав: {ret[1]} г., белка, {ret[2]} г., жиров, {ret[3]} г., углеводов, {ret[4]}  ккал.'
                                                f'',parse_mode='HTML',reply_markup=InlineKeyboardMarkup().\
                                        add(InlineKeyboardButton(f'Добавить "{ret[0]}"',callback_data=ret[0])))
        else:
            await message.answer("Некорректный ввод, попробуте ещё раз")
    except:
        pass
#вытаскиваем данные и сохраняем в машину состояний
@dp.callback_query_handler(state=Score.V15)
async def del_callback_run8(callback_query: types.CallbackQuery, state: FSMContext):
    read = await sqlite_db_score.sql_read2()
    for ret in read:
        for i in ret:
            if i == callback_query.data:
                await state.update_data(A1=ret[1])#сохраняем ответ в машину состояний
                await state.update_data(A2=ret[2])#сохраняем ответ в машину состояний
                await state.update_data(A3=ret[3])#сохраняем ответ в машину состояний
                await state.update_data(A4=ret[4])#сохраняем ответ в машину состояний
                await Score.V16.set()
                await callback_query.answer(text=f'"{callback_query.data}" добавлено,\nсколько в граммах?', show_alert=True)
#вводим грамаж, считаем грамаж и сохраняем в машину состояний
@dp.message_handler(state=Score.V16)
async def score_16(message: types.Message, state: FSMContext):
    if message.text.isnumeric():
        gramm = float(message.text)
        data = await state.get_data()
        A1 = ((float(data.get("A1"))) / 100 * gramm) + (float(data.get("result1"))) #выгружаем A1 и result2, считаем
        A2 = ((float(data.get("A2"))) / 100 * gramm) + (float(data.get("result2"))) #выгружаем A2 и result2, считаем
        A3 = ((float(data.get("A3"))) / 100 * gramm) + (float(data.get("result3"))) #выгружаем A3 и result3, считаем
        A4 = ((float(data.get("A4"))) / 100 * gramm) + (float(data.get("result4"))) #выгружаем A4 и result4, считаем
        await state.update_data(result1=A1)  # сохраняем ответ в машину состояний
        await state.update_data(result2=A2)  # сохраняем ответ в машину состояний
        await state.update_data(result3=A3)  # сохраняем ответ в машину состояний
        await state.update_data(result4=A4)  # сохраняем ответ в машину состояний
        await Score.V17.set()
        await bot.send_message(message.from_user.id,'введите название девятого ингридиента')
    else:
        await message.answer("Некорректный ввод, попробуте ещё раз, напишите количество в граммах?")

#ИЩЕМ ДЕВЯТЫЙ ИНГРИДИЕНТ
@dp.message_handler(state=Score.V17)
async def score_17(message: types.Message):
    try:
        if not message.text.isnumeric(): #проверка на то что это не число
            read = await sqlite_db_score.sql_read2() #выбираем данные из БД ингридиентов
            for ret in read: #перебираем массив с ингридиентами
                for i in ret: #перебираем с данными внутри ингридиентов
                    if i.lower().translate(str.maketrans("", "", string.punctuation)).find(message.text.lower()) != -1:
                        await bot.send_message(message.from_user.id,
                                            f'<b>{ret[0]} </b>, состав: {ret[1]} г., белка, {ret[2]} г., жиров, {ret[3]} г., углеводов, {ret[4]}  ккал.'
                                                f'',parse_mode='HTML',reply_markup=InlineKeyboardMarkup().\
                                               add(InlineKeyboardButton(f'Добавить "{ret[0]}"',callback_data=ret[0])))
        else:
            await message.answer("Некорректный ввод, попробуте ещё раз")
    except:
        pass
#вытаскиваем данные и сохраняем в машину состояний
@dp.callback_query_handler(state=Score.V17)
async def del_callback_run9(callback_query: types.CallbackQuery, state: FSMContext):
    read = await sqlite_db_score.sql_read2()
    for ret in read:
        for i in ret:
            if i == callback_query.data:
                await state.update_data(A1=ret[1])#сохраняем ответ в машину состояний
                await state.update_data(A2=ret[2])#сохраняем ответ в машину состояний
                await state.update_data(A3=ret[3])#сохраняем ответ в машину состояний
                await state.update_data(A4=ret[4])#сохраняем ответ в машину состояний
                await Score.V18.set()
                await callback_query.answer(text=f'"{callback_query.data}" добавлено,\nсколько в граммах?', show_alert=True)
#вводим грамаж, считаем грамаж и сохраняем в машину состояний
@dp.message_handler(state=Score.V18)
async def score_18(message: types.Message, state: FSMContext):
    if message.text.isnumeric():
        gramm = float(message.text)
        data = await state.get_data()
        A1 = ((float(data.get("A1"))) / 100 * gramm) + (float(data.get("result1"))) #выгружаем A1 и result2, считаем
        A2 = ((float(data.get("A2"))) / 100 * gramm) + (float(data.get("result2"))) #выгружаем A2 и result2, считаем
        A3 = ((float(data.get("A3"))) / 100 * gramm) + (float(data.get("result3"))) #выгружаем A3 и result3, считаем
        A4 = ((float(data.get("A4"))) / 100 * gramm) + (float(data.get("result4"))) #выгружаем A4 и result4, считаем
        await state.update_data(result1=A1)  # сохраняем ответ в машину состояний
        await state.update_data(result2=A2)  # сохраняем ответ в машину состояний
        await state.update_data(result3=A3)  # сохраняем ответ в машину состояний
        await state.update_data(result4=A4)  # сохраняем ответ в машину состояний
        await Score.V19.set()
        await bot.send_message(message.from_user.id,'введите название десятого ингридиента')
    else:
        await message.answer("Некорректный ввод, попробуте ещё раз, напишите количество в граммах?")

#ИЩЕМ ДЕСЯТЫЙ ИНГРИДИЕНТ
@dp.message_handler(state=Score.V19)
async def score_19(message: types.Message):
    try:
        if not message.text.isnumeric(): #проверка на то что это не число
            read = await sqlite_db_score.sql_read2() #выбираем данные из БД ингридиентов
            for ret in read: #перебираем массив с ингридиентами
                for i in ret: #перебираем с данными внутри ингридиентов
                    if i.lower().translate(str.maketrans("", "", string.punctuation)).find(message.text.lower()) != -1:
                        await bot.send_message(message.from_user.id,
                                            f'<b>{ret[0]} </b>, состав: {ret[1]} г., белка, {ret[2]} г., жиров, {ret[3]} г., углеводов, {ret[4]}  ккал.'
                                                f'',parse_mode='HTML',reply_markup=InlineKeyboardMarkup().\
                                        add(InlineKeyboardButton(f'Добавить "{ret[0]}"',callback_data=ret[0])))
        else:
            await message.answer("Некорректный ввод, попробуте ещё раз")
    except:
        pass
#вытаскиваем данные и сохраняем в машину состояний
@dp.callback_query_handler(state=Score.V19)
async def del_callback_run10(callback_query: types.CallbackQuery, state: FSMContext):
    read = await sqlite_db_score.sql_read2()
    for ret in read:
        for i in ret:
            if i == callback_query.data:
                await state.update_data(A1=ret[1])#сохраняем ответ в машину состояний
                await state.update_data(A2=ret[2])#сохраняем ответ в машину состояний
                await state.update_data(A3=ret[3])#сохраняем ответ в машину состояний
                await state.update_data(A4=ret[4])#сохраняем ответ в машину состояний
                await Score.V20.set()
                await callback_query.answer(text=f'"{callback_query.data}" добавлено,\nсколько в граммах?', show_alert=True)
#вводим грамаж, считаем грамаж и сохраняем в машину состояний
@dp.message_handler(state=Score.V20)
async def score_20(message: types.Message, state: FSMContext):
    if message.text.isnumeric():
        gramm = float(message.text)
        data = await state.get_data()
        A1 = ((float(data.get("A1"))) / 100 * gramm) + (float(data.get("result1"))) #выгружаем A1 и result2, считаем
        A2 = ((float(data.get("A2"))) / 100 * gramm) + (float(data.get("result2"))) #выгружаем A2 и result2, считаем
        A3 = ((float(data.get("A3"))) / 100 * gramm) + (float(data.get("result3"))) #выгружаем A3 и result3, считаем
        A4 = ((float(data.get("A4"))) / 100 * gramm) + (float(data.get("result4"))) #выгружаем A4 и result4, считаем
        A1 = round(A1, 2)  # округляем до 2 знаков после запятой
        A2 = round(A2, 2)  # округляем до 2 знаков после запятой
        A3 = round(A3, 2)  # округляем до 2 знаков после запятой
        A4 = round(A4, 2)  # округляем до 2 знаков после запятой
        await bot.send_message(message.from_user.id, f'<b>Блюдо состоит из: </b>'
                                                     f'' + str(A1) + ' г. белка, ' + str(A2) + ' г. жиров, ' + str(
            A3) + ' г. углеводов. \n<b>Итого:</b>' + str(A4) + ' ккал.', parse_mode='HTML',reply_markup=meinMenu)
        await state.finish()
    else:
        await message.answer("Некорректный ввод, попробуте ещё раз, напишите количество в граммах?")

