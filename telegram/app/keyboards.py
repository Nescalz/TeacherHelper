from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from sqlite3 import connect
main = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Отменить заявку", callback_data="cancel")]])
def tests(id):
    connectdb = connect("test.db") 
    cursor = connectdb.cursor()
    cursor.execute('''
        SELECT name, id FROM test WHERE student_id = ? AND otmetca = NONE
    ''', (id,))
    result = cursor.fetchall()
    connectdb.close()
    kb = []
    for i in result:
        kb.append(KeyboardButton(text=str(i)))
    tests = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, input_field_placeholder="Выберите тест")
    return tests