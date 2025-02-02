from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import app.keyboards as kb
from sqlite3 import connect
from time import sleep
router = Router()

class reg(StatesGroup):
    id = State()
    fio = State()
    clas = State()
    start = State()


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    connectdb = connect("student.db") 
    cursor = connectdb.cursor()
    cursor.execute('''
        SELECT * FROM students WHERE id = ?
    ''', (message.from_user.id,))
    result = cursor.fetchall()
    connectdb.commit()
    connectdb.close()
    if result:
        if result[0][4] == 1:
            await message.answer("Вы уже отправили заявку на регистрацию, ожидайте ответа.")
        elif result[0][4] == 0:
            if 1 == 1 :
                await message.answer("В данынй момент для вас нету тестов.")
            else:
                await state.set_state(reg.start)
                await message.answer("Чтобы начать проходить тест, нажмите на кнопку теста, который надо пройти.", reply_markup=kb.keyboards.tests(message.from_user.id))
            
    else:
        await state.set_state(reg.id)
        await message.answer("Привет! Чтобы начать пользоватся введите ID вашего учителя")

@router.message(reg.id)
async def reg_id(message: Message, state: FSMContext):
    await state.update_data(id=message.text)
    await state.set_state(reg.fio)
    await message.answer("Введите ваше ФИО(Фамилия Имя Отчество)")


@router.message(reg.fio)
async def reg_fio(message: Message, state: FSMContext):
    await state.update_data(fio=message.text)
    await state.set_state(reg.clas)
    await message.answer("Введите ваш класс. Пример: 1б")

@router.message(reg.clas)
async def reg_fio(message: Message, state: FSMContext):
    await state.update_data(clas=message.text)
    data = await state.get_data()

    connectdb = connect("student.db") 
    cursor = connectdb.cursor()
    cursor.execute('''
        INSERT INTO students (name, id, teacher_id, telegram_id, auth, clas)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (data["fio"], message.from_user.id, data["id"],  f"@{message.from_user.username}", 1 , data["clas"].lower()))
    connectdb.commit()
    connectdb.close()
    await message.answer(f"Заявка на вступление в класс зарегистрирована.\nID: {data["id"]}, ФИО: {data["fio"]}, Класс: {data["clas"]}, Ваш ID: {message.from_user.id}", reply_markup=kb.main)

#     await state.set_state(reg.loading)

# @router.message(reg.loading)
# async def loading(message: Message, state: FSMContext):
#     await state.update_data(loading=message.text)
@router.message(reg.start)
async def start(message: Message, state: FSMContext):
    print(1)
    await message.answer("В данынй момент для вас нету тестов.")


@router.callback_query(F.data == "cancel")
async def clear(callback: CallbackQuery):
    connectdb = connect("student.db") 
    cursor = connectdb.cursor()
    cursor.execute('''
        DELETE FROM students WHERE id = ?
    ''', (callback.from_user.id,))
    connectdb.commit()
    connectdb.close()
    await callback.answer("Заявка на тест отменена.\nДля создание новой введите: /start", show_alert=True)
