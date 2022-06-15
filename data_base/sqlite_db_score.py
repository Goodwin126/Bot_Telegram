import sqlite3 as sq
from loader import bot

def sql_start():
    global base, cur
    base = sq.connect("score.db")
    cur = base.cursor()
    if base:
        print('Database "score" connected OK!')
    base.execute('CREATE TABLE IF NOT EXISTS menu(name TEXT PRIMARY KEY, protein TEXT, fat TEXT, carbohydrate TEXT, calories TEXT)')
    base.commit()

async def sql_add_command(state):
    async with state.proxy() as data:
        cur.execute('INSERT INTO menu VALUES (?,?,?,?,?)', tuple(data.values()))
        base.commit()

async def sql_read(message):
    for ret in cur.execute('SELECT * FROM menu').fetchall():
        await bot.send_photo(message.from_user.id,f'{ ret[0]} название {ret[1]},белка: {ret[2]} г.,жиров: {ret[3]}г.,углеводов: {ret[4]}г.')

async def sql_read2():
    return cur.execute('SELECT * FROM menu').fetchall()


async def sql_delete_command(data):
    cur.execute('DELETE FROM menu WHERE name == ?',(data,))
    base.commit()
