import sqlite
import keyboards.keyboard
from aiogram import types
from aiogram import Bot, Dispatcher, F, Router, html
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import Command, CommandStart

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

# Запрос списка категорий для редактирование
@form_router.message(Command("categories"))
async def buy(message: types.Message):

    data= await sqlite.db_sel_edit_cat(message.chat.id)

    if len(data) != 0:
        await message.answer(f"Список категорий", reply_markup=keyboards.keyboard.gen_list_cat(data))
    else:
        await message.answer(
            f"В вашем списке категорий не обнаружено, предлагаю создать свои или заполнить их по умолчанию.",
            reply_markup=keyboards.keyboard.gen_list_cat_nul()
        )

# Заполняем категории по умолчанию
@form_router.callback_query(keyboards.keyboard.NumbersCallbackFactory.filter(F.action == "ins_cat_def"))
async def command_start(callback: types.CallbackQuery) -> None:
    dan = await sqlite.db_sel_default_cat()
    print(dan)
    print(callback.message.chat.id)
    cat = ""
    wr = ""
    for i in dan:
        cat = i[0]
        wr = i[1]
        await sqlite.db_insert_cat(cat,wr, callback.message.chat.id, i[2])

    await callback.message.edit_text(
        "Категории заполнены"
    )


# Переход категорий для редактирование
@form_router.callback_query(keyboards.keyboard.NumbersCallbackFactory.filter(F.action == "edit_cats"))
async def callbacks_num_change_fab(
        callback: types.CallbackQuery,
        callback_data: keyboards.keyboard.NumbersCallbackFactory
        ) -> None:
    name_cat = callback_data.name
    wiring = callback_data.val
    id_cat = callback_data.value
    wiring_e = ""
    wiring_n = ""
    if wiring == "decr":
        wiring_e = "(расход)"
        wiring_n = "приход"
    elif wiring == "incr":
        wiring_e = "(приход)"
        wiring_n = "расход"

    await callback.message.edit_text(
        f"Редактирование категории <b>{name_cat} {wiring_e}</b>",
         reply_markup=keyboards.keyboard.gen_edits_cat(id_cat,wiring_n,name_cat,wiring)
    )

# Запрос списка категорий для редактирование EXIT
@form_router.callback_query(keyboards.keyboard.NumbersCallbackFactory.filter(F.action == "edit_cats_ex"))
async def callbacks_num_change_fab(
        callback: types.CallbackQuery,
) -> None:

    await callback.message.edit_text("Список категорий\n---\n Выход")

# Удаляем категорию
@form_router.callback_query(keyboards.keyboard.NumbersCallbackFactory.filter(F.action == "edit_cats_del"))
async def callbacks_num_change_fab(
        callback: types.CallbackQuery,
        callback_data: keyboards.keyboard.NumbersCallbackFactory
) -> None:
    name_cat = callback_data.name
    id = callback_data.value
    await sqlite.db_del_edit_cat(id)
    await callback.message.edit_text(f'Категория "{name_cat}" \n---\n❌ Удалена')



# Назначаем категорию как топливную
@form_router.callback_query(keyboards.keyboard.NumbersCallbackFactory.filter(F.action == "edit_cats_fuel"))
async def callbacks_num_change_fab(
        callback: types.CallbackQuery,
        callback_data: keyboards.keyboard.NumbersCallbackFactory
) -> None:
    name_cat = callback_data.name
    id = callback_data.value
    await sqlite.db_upg_edit_cat(id,"yes","decr")
    await callback.message.edit_text(f"Назначили {name_cat} как топливную категорию  \n---\n")

# Изменяем в категории операцию
@form_router.callback_query(keyboards.keyboard.NumbersCallbackFactory.filter(F.action == "edit_cats_wiring"))
async def callbacks_num_change_fab(
        callback: types.CallbackQuery,
        callback_data: keyboards.keyboard.NumbersCallbackFactory
) -> None:

    name_cat = callback_data.name
    id = callback_data.value
    wiring = callback_data.val
    wiring_e = ""
    wiring_n = ""
    if wiring == "decr":
        wiring_e = "incr"
        wiring_n = "приходную"
    elif wiring == "incr":
        wiring_e = "decr"
        wiring_n = "расходную"

    await sqlite.db_upg_edit_cat_wr(id,wiring_e)
    await callback.message.edit_text(f'Назначили категорию: "{name_cat}" как {wiring_n}  \n---\n')


@form_router.message(Command("cattegor_incr"))
async def buy(message: types.Message):

    data = await sqlite.db_sel_inc()
    await message.answer(f"Список: {data}", reply_markup=keyboards.keyboard.gen_markup(data))


@form_router.callback_query(keyboards.keyboard.NumbersCallbackFactory.filter(F.action == "ins_cat"))
async def command_start(callback: types.CallbackQuery, state: FSMContext) -> None:
    await state.set_state(Form.cat_new)
    await callback.message.edit_text(
        "Введите название категории"
    )


@form_router.message(Form.cat_new)
async def process_name(message: Message, state: FSMContext) -> None:
    await state.update_data(cat_new=message.text)
    await state.update_data(id_us=message.from_user.id)

    await message.answer(
        f"Как будем учитывать категорию, {html.quote(message.text)} ?",
        reply_markup=get_and_cat()
    )
def get_and_cat():
    buttons = [
        [
            types.InlineKeyboardButton(text="Расход", callback_data="num_decr"),
            types.InlineKeyboardButton(text="Приход", callback_data="num_incr")
        ],

    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


@form_router.message(Command("list_cat"))
async def process_name(message: Message, state: FSMContext) -> None:
    dann = await sqlite.db_sel_flight("active",message.from_user.id)
    await message.answer(
        "List categor",
        reply_markup=keyboards.keyboard.gen_list_cat()
    )


###################################################
@form_router.callback_query(F.data.startswith("num_"))
async def callbacks_num(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    us_id = data["id_us"]
    cat_new = data["cat_new"]
    action = callback.data.split("_")[1]
    await state.clear()

    if action == "incr":
        await sqlite.db_insert_cat(cat_new, "incr", us_id," ")
        await callback.message.edit_text(f'Добавлена категория : <b>"{cat_new}"</b> как поступление.')

    elif action == "decr":
        await sqlite.db_insert_cat(cat_new, "decr", us_id,"")
        await callback.message.edit_text(f'Добавлена категория : <b>"{cat_new}"</b> как расход.')

    elif action == "finish":
        await sqlite.db_insert_cat(cat_new, "finish", us_id)
        await callback.message.edit_text(f"Итого: {us_id} finish {cat_new}")

    await callback.answer()
