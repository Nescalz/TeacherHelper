from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import app.keyboards as kb

router = Router()

class reg(StatesGroup):
    id = State()
    fio = State()
    clas = State()

@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.set_state(reg.id)
    await message.answer("Привет! Чтобы начать пользоватся введите ID вашего учителя")

@router.message(reg.id)
async def reg_id(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(reg.fio)
    await message.answer("Введите ваше ФИО")


@router.message(reg.fio)
async def reg_fio(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(reg.clas)
    await message.answer("Введите ваш класс")