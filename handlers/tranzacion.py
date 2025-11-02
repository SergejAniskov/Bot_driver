from calendar import calendar
from datetime import datetime
from aiogram.exceptions import TelegramBadRequest
import sqlite
import keyboards.keyboard
import openpyxl
from aiogram import types
from aiogram import Bot, Dispatcher, F, Router, html
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import Command, CommandStart
from contextlib import suppress
from re import Match



from aiogram.types import (
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)


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



now = datetime.now().strftime("%Y-%m-%d %H:%M")
now2 = datetime.now().strftime("%d.%m.%Y")
now1 = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def transform_date_new(date):
    months = ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня',
              'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря']
    year, month, day = date.split('-')
    return f'{day} {months[int(month) - 1]} {year} года'

def transform_date(date):
    months = ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня',
              'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря']
    day, month, year = now2.split('.')
    return f'{day} {months[int(month) - 1]} {year} года'



# Обработка редактирование даты
@form_router.callback_query(keyboards.keyboard.Itog_Callback.filter(F.action == "tr_date"))
async def callbacks_num_change_fab(
        callback: types.CallbackQuery,
        callback_data: keyboards.keyboard.Itog_Callback,
        state: FSMContext
) -> None:
     # mes_id = mes_id,
    id_tranz = callback_data.id_tranz
    us_id = callback_data.val
    # mes_id = callback.data.mes_id

    data = await sqlite.sel_tranc(id_tranz,us_id)

    cash = ""
    cat = ""
    date = ""
    for i in data:
        cash = i[0]
        cat = i[1]
        date = i[2]

    dates = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
    ss = dates.strftime('%d-%m-%y %H:%M')
    month = dates.month
    year = dates.year
    days_in_month = calendar.monthrange(dates.year, dates.month)[1]  # 28
    text_mes = f"Добавлено <b>{cat}</b> ₽ в категорию <b>{cash}</b> операция расход \n {date} "
    await state.update_data(text_mes=text_mes)
    await state.update_data(dates=date)
    await state.update_data(dates_in=date)
    await state.update_data(id_tranz=id_tranz)
    await state.update_data(us_id=us_id)

    await callback.message.edit_text(
        text_mes + "\n<b>Изменить дату на:</b>",
        reply_markup=keyboards.keyboard.get_key_date(id_tranz,dates.day,month,year)
    )


# Обработка нопки назад к дате
@form_router.callback_query(keyboards.keyboard.Itog_Callback.filter(F.action == "pr_date"))
async def callbacks_num_change_fab(
        callback: types.CallbackQuery,
        callback_data: keyboards.keyboard.Itog_Callback,
        state: FSMContext
) -> None:

    data = await state.get_data()
    date = data["dates"]
    id_tranz = data["id_tranz"]
    text_mes = data["text_mes"]
    dates = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')


    await callback.message.edit_text(
         text_mes + "\n<b>Изменить дату на:</b>",
         reply_markup=keyboards.keyboard.get_key_date(id_tranz, dates.day, dates.month, dates.year)
    )

###################################################
# Обработка кнопки готово дата
@form_router.callback_query(keyboards.keyboard.Itog_Callback.filter(F.action == "dates_finish"))
async def callbacks_num_change_fab(
        callback: types.CallbackQuery,
        state: FSMContext
) -> None:

    data = await state.get_data()
    text_mes = data["text_mes"]
    id_tranz = data["id_tranz"]
    date = data["dates"]
    date_in = data["dates_in"]
    us_id = data["us_id"]

    dates = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
    dates_in = datetime.strptime(date_in, '%Y-%m-%d %H:%M:%S')

    if dates == dates_in:

        text_mes = text_mes[:-20] + f" {transform_date_new(date[:-9])} {date[11:]}"
    else:
        await sqlite.update_trans_date(date,id_tranz)
        text_mes = text_mes[:-20] + f"Дата изменена на {transform_date_new(date[:-9])} {date_in[11:]}"

    await callback.message.edit_text(
        text_mes,
        reply_markup=keyboards.keyboard.get_keyboard(id_tranz, callback.message.message_id, us_id)
    )
    await state.clear()


###################################################
# Обработка редактирование года
@form_router.callback_query(keyboards.keyboard.Itog_Callback.filter(F.action == "dates_year"))
async def callbacks_num_change_fab(
        callback: types.CallbackQuery,
        state: FSMContext
) -> None:

    data = await state.get_data()
    text_mes = data["text_mes"]
    id_tranz = data["id_tranz"]
    date = data["dates"]
    us_id = data["us_id"]

    dates = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')

    await callback.message.edit_text(
        text_mes + "\n<b>Выбери год:</b>",
        reply_markup=keyboards.keyboard.get_key_year(dates.year,id_tranz,us_id)
    )

# Установка выбраного года
@form_router.callback_query(keyboards.keyboard.Itog_Callback.filter(F.action == "year_set"))
async def callbacks_num_change_fab(
        callback: types.CallbackQuery,
        callback_data: keyboards.keyboard.Itog_Callback,
        state: FSMContext
) -> None:

    data = await state.get_data()
    date = data["dates"]
    id_tranz = data["id_tranz"]
    text_mes = data["text_mes"]
    dates = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
    select_year = callback_data.val
    d_new = dates.replace(year=select_year)
    await state.update_data(dates=d_new.strftime('%Y-%m-%d %H:%M:%S'))

    await callback.message.edit_text(
        text_mes+ "\n<b>Изменить дату на:</b>",
        reply_markup=keyboards.keyboard.get_key_date(id_tranz,d_new.day,d_new.month,d_new.year)
    )




###################################################
# Обработка редактирование месяца
@form_router.callback_query(keyboards.keyboard.Itog_Callback.filter(F.action == "dates_month"))
async def callbacks_num_change_fab(
        callback: types.CallbackQuery,
        state: FSMContext
) -> None:

    data = await state.get_data()
    text_mes = data["text_mes"]
    id_tranz = data["id_tranz"]
    us_id = data["us_id"]

    await callback.message.edit_text(
        text_mes + "\n<b>Выбери месяц:</b>",
        reply_markup=keyboards.keyboard.get_key_month(id_tranz,us_id)
    )

# Установка выбраного месяца
@form_router.callback_query(keyboards.keyboard.Itog_Callback.filter(F.action == "month_set"))
async def callbacks_num_change_fab(
        callback: types.CallbackQuery,
        callback_data: keyboards.keyboard.Itog_Callback,
        state: FSMContext
) -> None:

    data = await state.get_data()
    date = data["dates"]
    id_tranz = data["id_tranz"]
    text_mes = data["text_mes"]
    dates = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
    select_month = callback_data.val
    d_new = dates.replace(month=select_month)
    await state.update_data(dates=d_new.strftime('%Y-%m-%d %H:%M:%S'))

    await callback.message.edit_text(
        text_mes + "\n<b>Изменить дату на:</b>",
        reply_markup=keyboards.keyboard.get_key_date(id_tranz,d_new.day,d_new.month,d_new.year)
    )


# Обработка редактирование даты
@form_router.callback_query(keyboards.keyboard.Itog_Callback.filter(F.action == "dates_days"))
async def callbacks_num_change_fab(
        callback: types.CallbackQuery,
        state: FSMContext
) -> None:

    data = await state.get_data()
    text_mes = data["text_mes"]
    date = data["dates"]
    id_tranz = data["id_tranz"]
    us_id = data["us_id"]
    dates = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
    days_in_month = calendar.monthrange(dates.year, dates.month)[1]  # 28
    await callback.message.edit_text(
        text_mes + "\n<b>Выбери день:</b>",
        reply_markup=keyboards.keyboard.get_key_days(days_in_month,id_tranz,us_id)
    )

# Установка выбраного дня
@form_router.callback_query(keyboards.keyboard.Itog_Callback.filter(F.action == "days_set"))
async def callbacks_num_change_fab(
        callback: types.CallbackQuery,
        callback_data: keyboards.keyboard.Itog_Callback,
        state: FSMContext
) -> None:

    data = await state.get_data()
    date = data["dates"]
    id_tranz = data["id_tranz"]
    text_mes = data["text_mes"]
    dates = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
    select_day = callback_data.val
    d_new = dates.replace(day=select_day)
    await state.update_data(dates=d_new.strftime('%Y-%m-%d %H:%M:%S'))

    await callback.message.edit_text(
        text_mes + "\n<b>Изменить дату на:</b>",
        reply_markup=keyboards.keyboard.get_key_date(id_tranz,d_new.day,d_new.month,d_new.year)
    )




# Обработка Коментарий trancaction
@form_router.callback_query(keyboards.keyboard.Itog_Callback.filter(F.action == "tr_caments"))
async def callbacks_num_change_fab(
        callback: types.CallbackQuery,
        callback_data: keyboards.keyboard.Itog_Callback,
        state: FSMContext
) -> None:

    id_tranz = callback_data.id_tranz
    user = callback_data.val
    data = await sqlite.sel_tranc(id_tranz,user)

    cash = ""
    cat = ""
    date = ""
    for i in data:
        cash = i[0]
        cat = i[1]
        date = i[2]

    await callback.message.edit_text(
        f"💬 Введите, пожалуйста, комментарий."
    )
    await state.set_state(Form.coments)

    await state.update_data(cat=cat)
    await state.update_data(us_id=user)
    await state.update_data(cash=cash)
    await state.update_data(dates=date)
    await state.update_data(id_tr=id_tranz)


##################################################
############ Коментарий

@form_router.message(Form.coments)
# async def process_name(callback: types.CallbackQuery, state: FSMContext) -> None:
async def process_name(message: Message, state: FSMContext) -> None:
    coments = message.text

    data = await state.get_data()
    cash = data["cash"]
    cat = data["cat"]
    us_id = data["us_id"]
    dates = data["dates"]

    idi = data["id_tr"]



    await sqlite.update_trans_com(coments, idi)

    await message.answer( text=f"👌 Комментарий успешно добавлен.\n Добавлено {cash} ₽ в категорию {cat} \n  операция расход \n {dates}, <i><b>{coments}</b></i>",
          reply_markup=keyboards.keyboard.get_keyboard(idi, message.message_id, us_id)
    )
    await state.clear()
    print(f"ID Mess  coments {coments}")




# Обработка del trancaction
@form_router.callback_query(keyboards.keyboard.Itog_Callback.filter(F.action == "inc_tr_kl"))
async def callbacks_num_change_fab(
        callback: types.CallbackQuery,
        callback_data: keyboards.keyboard.Itog_Callback,
        state: FSMContext
) -> None:
    data = await state.get_data()
    cash = data["cash"]
    sell = data["language"]
    cat = data["name"]
    us_id = data["id_us"]
    flight = data["id_flight"]
    name_flight = data["name_flight"]

    znac = callback_data.val
    mes_id = data["mes_id"]

    # print(f"Del_tranc {znac}")
    if znac == 1:
        print(f"date edit {data}")




async def select_cat(message: types.Message, cat: str, sellect: str, cash: str, us_id: int, edit: int, flight: int, fuel: int):
    with suppress(TelegramBadRequest):

        if edit == 0:
            dann = await sqlite.db_insert_transactions(cat, us_id, cash, now1, flight, fuel)
            idi = 0
            users = 0
            for i in dann:
                idi = i[0]

            await message.edit_text(
                f"Добавлено {cash} ₽ в категорию {cat} операция расход \n {transform_date(now1)} ",
                reply_markup=keyboards.keyboard.get_keyboard(idi, message.message_id, us_id)
            )
            await message.edit_text(
                f"Добавлено {cash} ₽ в категорию {cat} операция расход \n {transform_date(now1)} ",
                reply_markup=keyboards.keyboard.get_keyboard(idi,message.message_id,us_id)
            )
            # print(f"id {id}")
            # print(f"message_id {message.message_id}")




# ОБРАБОТКА К Приходу
@form_router.callback_query(keyboards.keyboard.NumbersCallbackFactory.filter(F.action == "incr"))
async def callbacks_num_change_fab(
        callback: types.CallbackQuery,
        callback_data: keyboards.keyboard.NumbersCallbackFactory,
        state: FSMContext
) -> None:
    data = await state.get_data()
    cash = data["cash"]
    name_flight = data["name_flight"]
    users_id = callback.message.chat.id
# Запрос категории

    data = await sqlite.db_sel_cat(users_id, "incr")

    await callback.message.edit_text(
        f"{name_flight}\nВыбери куда записать: {cash} ₽",
        reply_markup=keyboards.keyboard.gen_markup_deb(data)
    )

# ОБРАБОТКА К Расходу
@form_router.callback_query(keyboards.keyboard.NumbersCallbackFactory.filter(F.action == "decr"))
async def callbacks_num_change_fab(
        callback: types.CallbackQuery,
        callback_data: keyboards.keyboard.NumbersCallbackFactory,
        state: FSMContext
) -> None:
    data = await state.get_data()
    cash = data["cash"]
    users_id = callback.message.chat.id

# Запрос категории
    data= await sqlite.db_sel_cat(users_id, "decr")

    await callback.message.edit_text(
        f"Выбери куда записать: {cash} ₽",
        reply_markup=keyboards.keyboard.gen_markup(data)
    )




async def update_num_text(message: types.Message, new_value: str):
    await message.edit_text(
        f"Уитывать категорию: {new_value} как",
        reply_markup=get_keyboard()
    )
def get_keyboard():
    buttons = [
        [
            types.InlineKeyboardButton(text="Расход", callback_data="num_decr"),
            types.InlineKeyboardButton(text="Приход", callback_data="num_incr")
        ],
        [types.InlineKeyboardButton(text="Подтвердить", callback_data="num_finish")]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

# Обработка del trancaction
@form_router.callback_query(keyboards.keyboard.Itog_Callback.filter(F.action == "tr_cancel"))
async def callbacks_num_change_fab(
        callback: types.CallbackQuery,
        callback_data: keyboards.keyboard.Itog_Callback
) -> None:

    id_tranz = callback_data.id_tranz
    user = callback_data.val
    data = await sqlite.sel_tranc(id_tranz,user)

    cash = ""
    cat = ""
    date = ""
    for i in data:
        cash = i[0]
        cat = i[1]
        date = i[2]

    await sqlite.db_del_transactions(id_tranz, user)
    await callback.message.edit_text(
        f"Добавлено <b>{cat}</b> ₽ в категорию <b>{cash}</b> операция расход \n {date} \n---\n🚫 Отменено"
    )

@form_router.message(Form.fuel_vol)
async def get_info_m(message: types.Message, state: FSMContext) -> None:
    litr = message.text
    litr = litr.replace(",", ".")
    try:
        float(litr)
        data = await state.get_data()
        cash = data["cash"]
        sell = data["language"]
        cat = data["name"]
        us_id = data["id_us"]
        flight = data["id_flight"]
        mes_text = data["mes_text"]

        await select_cat(mes_text, cat, sell, cash, us_id, 0, flight, litr)
        await state.clear()

    except ValueError:
        await state.set_state(Form.fuel_vol)
        await message.reply(
            f'Введённое значение не является числом!\n💬 Введите, количество литров. в формате "112.5"'
        )

# Обработка выбора меню категории
@form_router.callback_query(keyboards.keyboard.NumbersCallbackFactory.filter(F.action == "select"))
async def callbacks_num_change_fab(
        callback: types.CallbackQuery,
        callback_data: keyboards.keyboard.NumbersCallbackFactory,
        state: FSMContext
    ) -> None:

    await state.update_data(name=callback_data.val)
    data = await state.update_data(language=callback_data.value)
    await state.update_data(mes_id=callback.message.message_id)

    cash = data["cash"]
    sell = data["language"]
    cat = data["name"]
    us_id = data["id_us"]
    flight = data["id_flight"]


    if sell == 123:


        await callback.message.edit_text(
            "💬 Введите, количество литров."
        )
        await state.set_state(Form.fuel_vol)
        await state.update_data(mes_text=callback.message)


    else:
        await select_cat(callback.message, cat, sell, cash, us_id, 0, flight,"")
        await state.clear()
        # print("mes_ID")
        # print(callback.message.message_id)

    await callback.answer()

    @form_router.message(F.text.regexp(r"(\d+)", mode=RegexpMode.SEARCH).as_("code"))
    async def handle_code(message: types.Message, code: Match[str], state: FSMContext) -> None:
        await state.update_data(id_us=message.from_user.id)

        dann = await sqlite.db_sel_flight("active", message.from_user.id)
        if not dann:
            await message.answer(
                f"У вас нет активных рейсов!",
                reply_markup=keyboards.keyboard.key_fl_new()
            )
        else:

            for i in dann:
                await state.update_data(name_flight=f"Рейс: <b>{i[1]}</b> от {i[2]} ")
                await state.update_data(id_flight=i[0])

            name = await state.get_data()
            name_flight = name["name_flight"]
            data = await state.update_data(cash=code.group())
            cash = data["cash"]
            await state.set_state(Form.cash)
            data_cat = await sqlite.db_sel_cat(message.from_user.id, "decr")
            if len(data_cat) != 0:
                await message.answer(
                    f"{name_flight}\nВыбери куда записать: <b>{cash}</b> ₽",
                    reply_markup=keyboards.keyboard.gen_markup(data_cat)
                )
            else:
                await message.answer(
                    f"Категорий учета отсутствуют. Предлагаю создать свои каткгории или заполнить списоком по умолчанию, а затем повторить ввод суммы.",
                    reply_markup=keyboards.keyboard.gen_list_cat_nul()
                )

        data = await state.get_data()
        cash = data["cash"]
        name_flight = data["name_flight"]
        # Запрос категории
        data = await sqlite.db_sel_cat(message.from_user.id, "incr")
