import sqlite
from aiogram import types
from aiogram import Bot, Dispatcher, F, Router, html
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from aiogram.types import (
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)

start_router = Router()


class Registration(StatesGroup):
    choosing_role = State()
    entering_name = State()

class Form(StatesGroup):
    name = State()
    like_bots = State()
    language = State()
    cash = State()
    id_us = State()
    cat_new = State()
    mes_id = State()
    coments = State()
    fuel_vol = State()


@start_router.message(CommandStart())
async def command_start(message: Message, state: FSMContext) -> None:
    id = message.from_user.id
    data = await sqlite.db_sel_driver(id)
    user = ""
    if len(data) != 0:
        for i in data:
            user = i[0]
        await message.answer(f"Приветствую <b>{user}</b>!\nВы зарегистрированы в системе, можете продолжать работать.")
    else:
        keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="🚛 Водитель")],
                [KeyboardButton(text="🏢 Владелец парка")]
            ],
            resize_keyboard=True
        )
        await message.answer("Привет! Выберите вашу роль:", reply_markup=keyboard)
        await state.set_state(Registration.choosing_role)


@start_router.message(Registration.choosing_role)
async def process_role_choice(message: Message, state: FSMContext):
    role = message.text.strip()

    if role not in ["🚛 Водитель", "🏢 Владелец парка"]:
        await message.answer("Выберите роль, используя кнопки ниже.")
        return

    role_db = "driver" if role == "🚛 Водитель" else "owner"
    await state.update_data(role=role_db)

    await message.answer("Добро пожаловать!\nПредставьтесь полным ФИО, будем использовать для отчёта.\n"
            "   Этот бот может помочь водителю в учете доходов и расходов, а также создании отчетов о рейсах.")
    await state.set_state(Registration.entering_name)


@start_router.message(Form.name)
async def handle_code(message: types.Message, state: FSMContext) -> None:
    user_name = message.text
    user_id = message.from_user.id
    await sqlite.db_insert_driver(user_id,user_name)
    await state.clear()
    await message.answer(
        f"Поздравляю <b>{user_name}</b>!\nВы зарегистрированы в системе, можете продолжать работать.",
        reply_markup=ReplyKeyboardRemove(),
    )
    # await message.reply("Я тебя не понимаю :(")
