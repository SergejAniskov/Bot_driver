from datetime import datetime, timedelta, date
import asyncio
import logging
import sys
import keyboards.keyboard
import sqlite
import emoji
import calendar
import openpyxl
###################PDF

from win32com import client
from openpyxl.worksheet import worksheet
from datetime import datetime
from aiogram.exceptions import TelegramBadRequest
from aiogram import types
from os import getenv
from re import Match
from magic_filter import RegexpMode
from aiogram import Bot, Dispatcher, F, Router, html
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from contextlib import suppress
from aiogram.fsm.state import State, StatesGroup
from aiogram.enums import ParseMode, ChatAction

from handlers import start
from handlers import flight
from handlers import delivery
from handlers import categore
from handlers import tranzacion

from aiogram.types import (
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)

from main_modified import Registration

logging.basicConfig(level=logging.INFO, stream=sys.stdout)


import os
from dotenv import load_dotenv
load_dotenv()  # загружает .env
TOKEN = os.getenv("BOT_TOKEN")
print("TOKEN:", TOKEN)  # временно для проверки



form_router = Router()


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

class Dates(StatesGroup):
    day = State()
    month = State()
    yer = State()
    itog = State()

class Fuels(StatesGroup):
    fuel_vol = State()
class Flight(StatesGroup):
    name = State()
    status = State()
    cars = State()
    mileage = State()
    fuel = State()

class Flight_exit(StatesGroup):
    status = State()
    name = State()
    finish_odometr = State()
    fuel_residues = State()

class orders_gen(StatesGroup):
    namber = State()

class Delivery(StatesGroup):
    and_us = State()
    and_phone = State()
    sender = State()
    recipient = State()
    sender_city = State()
    recipient_city = State()
    photo = State()



now = datetime.now().strftime("%Y-%m-%d %H:%M")
now2 = datetime.now().strftime("%d.%m.%Y")
now1 = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# delivery - Доставки
# categories - Управление категориями
# flight - Управление Рейсами
# cancel - Выход


# Запуск бота
async def on_startup(_):
    await sqlite.db_connect()
    logging.info("Подключение к базе данных успешно")


def transform_date(date):
    months = ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня',
              'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря']
    day, month, year = now2.split('.')
    return f'{day} {months[int(month) - 1]} {year} года'

def transform_date_new(date):
    months = ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня',
              'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря']
    year, month, day = date.split('-')
    return f'{day} {months[int(month) - 1]} {year} года'


def is_number(string):
    try:
        float(string)
        return True
    except ValueError:
        return False


@form_router.callback_query(keyboards.keyboard.Flight_Callback.filter(F.action == "order_flights_pdf"))
@form_router.message(Command("pdf"))
async def handle_command_pic(callback: types.CallbackQuery):
    # await message.bot.send_chat_action(
    #     chat_id=message.chat.id,
    #     action=ChatAction.UPLOAD_PHOTO,
    # )
    # Create a Workbook object
    await callback.message.answer("Создаю PDF")

    #
    # # Opening Microsoft Excel
    WB_PATH = r'test.xlsx'
    WB_PATH2 = "C:\\Users\\Сергей\\PycharmProjects\\pythonProject2\\test.xlsx"
    WB_PATH3 = "C:\\Users\\Сергей\\PycharmProjects\\pythonProject2\\test.pdf"
    file_dsc = "test.pdf"
    excel = client.Dispatch("Excel.Application")
    # Read Excel File
    sheets = excel.Workbooks.Open(WB_PATH2)
    work_sheets = sheets.Worksheets[0]
    # # Converting into PDF File
    work_sheets.ExportAsFixedFormat(0, WB_PATH3)
    sheets.Close(False)
    excel.Quit()

    await callback.message.reply_document(
        document=types.FSInputFile(
            path=file_dsc,
        ),
    )


@form_router.message(Command("pic"))
async def handle_command_pic(message: types.Message):
    await message.bot.send_chat_action(
        chat_id=message.chat.id,
        action=ChatAction.UPLOAD_PHOTO,
    )
    # url = "https://t4.ftcdn.net/jpg/00/97/58/97/360_F_97589769_t45CqXyzjz0KXwoBZT9PRaWGHRk5hQqQ.jpg"
    # url = "https://images.unsplash.com/photo-1608848461950-0fe51dfc41cb"
    file_path = "cat.jpg"
    file_dsc = "test.pdf"
    # await message.bot.send_photo()
    # await message.reply_photo(
    #     # photo=url,
    #     photo=types.FSInputFile(
    #         path=file_path,
    #         # filename=
    #     ),
    #     caption="cat small pic",
    # )
    await message.reply_document(
        document=types.FSInputFile(
            path=file_dsc,
        ),
    )



############ Нажатие кнопки Создать Эксель
@form_router.callback_query(keyboards.keyboard.Flight_Callback.filter(F.action == "order_flights_exel"))
async def callbacks_num_change_fab(
        callback: types.CallbackQuery,
        callback_data: keyboards.keyboard.Flight_Callback
) -> None:
    flight_id = callback_data.id_fl


    # await exel_creat(flight_id)
    await callback.message.edit_text("Создан отчёт")
    await callback.answer()










def date_diff(date1, date2):
    d1 = date.strptime(date1, '%Y-%m-%d')
    t1 = datetime.strptime(date1 + ' ' + date1.split()[-1], '%Y-%m-%d %H:%M').time()
    d2 = date.strptime(date2, '%Y-%m-%d')
    t2 = datetime.strptime(date2 + ' ' + date2.split()[-1], '%Y-%m-%d %H:%M').time()

    delta = d2 - d1 - timedelta(hours = t2.hour-t1.hour , minutes = t2.minute-t1.minute )
    return delta.days





@form_router.message(Form.cat_new, F.text.casefold() == "No")
async def process_like_write_bots(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.reply(
        "Круто! Я тоже в Расход",
        reply_markup=ReplyKeyboardRemove(),
    )


# @form_router.message(Command("cancel"))
@form_router.message(F.text.casefold() == "cancel")
async def cancel_handler(message: Message, state: FSMContext) -> None:
    """
    Allow user to cancel any action
    """
    current_state = await state.get_state()
    if current_state is None:
        return

    logging.info("Cancelling state %r", current_state)
    await state.clear()
    await message.answer(
        "Cancelled.",
        reply_markup=ReplyKeyboardRemove(),
    )



@form_router.message(Form.like_bots)
async def process_unknown_write_bots(message: Message) -> None:
    await message.reply("Я тебя не понимаю :(")




async def main():
    bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher()
    dp.include_router(form_router)
    dp.include_router(categore.form_router)
    dp.include_router(flight.form_router)
    dp.include_router(start.start_router)
    dp.include_router(delivery.form_router)
    dp.include_router(tranzacion.form_router)

    await dp.start_polling(bot,
                           on_startup=on_startup
                           )


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        stream=sys.stdout,
                        )
    asyncio.run(main())
