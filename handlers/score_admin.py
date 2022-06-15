from aiogram.dispatcher import FSMContext
from aiogram import types, Dispatcher
from loader import dp, bot
from aiogram.dispatcher.filters import Text
from data_base import sqlite_db_score
from keyboards import Score_admin_kb
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from states import Score_admin


ID2 = None


#получаем ID текущего модератора:
@dp.message_handler(text='moderator2', is_chat_admin=True)
async def make_changes_command(message: types.Message):
    global ID2
    ID2 = message.from_user.id
    await bot.send_message(message.from_user.id, 'Что хозяин посчитаем???', reply_markup=Score_admin_kb.buttonc_case_admin)
    await message.delete()

#начало диалога загрузки нового пункта меню
@dp.message_handler(text="Загрузить", state=None)
async def cm_start(message: types.Message, state: FSMContext):
    if message.from_user.id == ID2:
        await Score_admin.name.set()
        await message.reply("Напишите название продукта")
#Выход из состояний
@dp.message_handler(state="*", commands='отмена')
@dp.message_handler(Text(equals='отмена', ignore_case=True), state="*")
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply("OK")

#ловим первый ответ и пишем словарь
@dp.message_handler(state=Score_admin.name)
async def load_name_product(message: types.Message, state: FSMContext):
    if message.from_user.id == ID2:
        async with state.proxy() as data:
            data['name'] = message.text
        await Score_admin.next()
        await message.reply("Введите колличество белка")

#ловим второй ответ
@dp.message_handler(state=Score_admin.protein)
async def load_protein(message: types.Message, state: FSMContext):
    if message.from_user.id == ID2:
        async with state.proxy() as data:
            data['protein'] = float(message.text)
        await Score_admin.next()
        await message.reply("Введите колличество жиров")
#ловим третий ответ
@dp.message_handler(state=Score_admin.fat)
async def load_fat(message: types.Message, state: FSMContext):
    if message.from_user.id == ID2:
        async with state.proxy() as data:
            data['fat'] = message.text
        await Score_admin.next()
        return await message.reply("Введите колличество углеводов")
#ловим четвертый ответ
@dp.message_handler(state=Score_admin.carbohydrate)
async def load_carbohydrate(message: types.Message, state: FSMContext):
    if message.from_user.id == ID2:
        async with state.proxy() as data:
            data['carbohydrate'] = message.text
        await Score_admin.next()
        return await message.reply("Введите колличество калорий")
#ловим последний ответ и используем полученные данные
@dp.message_handler(state=Score_admin.calories)
async def load_calories(message: types.Message, state: FSMContext):
    if message.from_user.id == ID2:
        async with state.proxy() as data:
            data['calories'] = float(message.text)
        await sqlite_db_score.sql_add_command(state)
        await state.finish()


@dp.callback_query_handler(lambda x: x.data and x.data.startswith ('del '))
async def del_callback_run(callback_query: types.CallbackQuery):
    await sqlite_db_score.sql_delete_command(callback_query.data.replace('del ',''))
    await callback_query.answer(text=f'{callback_query.data.replace("del","")} удалена.',show_alert=True)

@dp.message_handler(text="Удалить")
async def delete_item(message: types.Message):
    if message.from_user.id == ID2:
        read = await sqlite_db_score.sql_read2()
        for ret in read:
            await bot.send_message(message.from_user.id,f'{ ret[0]} название {ret[1]},белка: {ret[2]} г.,жиров: {ret[3]}г.,углеводов: {ret[4]}г.')
            await bot.send_message(message.from_user.id, text='^^^',reply_markup=InlineKeyboardMarkup().\
                                   add(InlineKeyboardButton(f'Удалить{ret[0]}',callback_data=f'del {ret[0]}')))

#регестрируем хендлеры
def register_handlers_score_admin(dp: Dispatcher):
    dp.register_message_handler(cm_start,text="Загрузить", state=None)
    dp.register_message_handler(cancel_handler,Text(equals='отмена', ignore_case=True), state="*")
    dp.register_message_handler(make_changes_command,text='moderator2', is_chat_admin=True)
    dp.register_message_handler(load_name_product,content_types=['name'],state=Score_admin.name)
    dp.register_message_handler(load_protein, state=Score_admin.protein)
    dp.register_message_handler(load_fat, state=Score_admin.fat)
    dp.register_message_handler(load_carbohydrate, state=Score_admin.carbohydrate)
    dp.register_message_handler(load_calories, state=Score_admin.calories)
    dp.register_message_handler(cancel_handler,state="*", commands='отмена')
    dp.register_message_handler(del_callback_run,lambda x: x.data and x.data.startwith('del '))
    dp.register_message_handler(delete_item,text="Удалить")


