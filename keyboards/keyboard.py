from datetime import datetime
from typing import Optional

from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData

cate_credit_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="тестовая кнопка"),
            InlineKeyboardButton(text="тестовая кнопка2")
        ]

    ]
)

select_yes_now = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="YesSes"),
            KeyboardButton(text="NoNow"),
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    selective=True
)



def get_keyboard(id_tranz,mes_id,us_id):


    builder = InlineKeyboardBuilder()
    builder.button(
        text="📆 Уточнить дату", callback_data=Itog_Callback(action="tr_date", val=us_id, mes_id=mes_id, id_tranz=id_tranz)
    )
    builder.button(
        text="📝 Комментарий", callback_data=Itog_Callback(action="tr_caments", val=us_id, mes_id=mes_id, id_tranz=id_tranz)
    )
    builder.button(
        text="❌ Отмена", callback_data=Itog_Callback(action="tr_cancel", val=us_id, mes_id=mes_id, id_tranz=id_tranz)
    )
    builder.adjust(2)
    return builder.as_markup()

def get_key_date(id_tranz,day,month,year):


    builder = InlineKeyboardBuilder()
    builder.button(
        text=f"{day}", callback_data=Itog_Callback(action="dates_days", id_tranz=id_tranz)
    )
    builder.button(
        text=f"{month}", callback_data=Itog_Callback(action="dates_month", id_tranz=id_tranz)
    )
    builder.button(
        text=f"{year}", callback_data=Itog_Callback(action="dates_year", id_tranz=id_tranz)
    )
    builder.button(
        text="✔️ Готово", callback_data=Itog_Callback(action="dates_finish", id_tranz=id_tranz)
    )
    builder.adjust(3)
    return builder.as_markup()

def get_key_days(days_is,id_tranz,us_id):

    builder = InlineKeyboardBuilder()

    for i in range(days_is):
        builder.button(
               text=f"{i+1}", callback_data=Itog_Callback(action="days_set", val=i+1)
        )

    builder.button(
        text="🔙 Назад", callback_data=Itog_Callback(action="pr_date", val=us_id, mes_id=days_is, id_tranz=id_tranz)
    )
    builder.adjust(7)
    return builder.as_markup()


def get_key_month(id_tranz,us_id):

    builder = InlineKeyboardBuilder()

    for i in range(12):
        builder.button(
               text=f"{i+1}", callback_data=Itog_Callback(action="month_set", val=i+1)
        )

    builder.button(
        text="🔙 Назад", callback_data=Itog_Callback(action="pr_date", val=us_id, id_tranz=id_tranz)
    )
    builder.adjust(4)
    return builder.as_markup()

def get_key_year(year,id_tranz,us_id):

    builder = InlineKeyboardBuilder()

    for i in range(year-11, year+1):
        builder.button(
               text=f"{i}", callback_data=Itog_Callback(action="year_set", val=i)
        )

    builder.button(
        text="🔙 Назад", callback_data=Itog_Callback(action="pr_date", val=us_id, id_tranz=id_tranz)
    )
    builder.adjust(4)
    return builder.as_markup()



def gen_markup(data):
    builder = InlineKeyboardBuilder()

    for i in data:
        if i[2] == "yes":
            builder.button(
                text=f"{i[1]} ",
                callback_data=NumbersCallbackFactory(action="select", value=f"123", val=f"{i[1]}")
            )
        else:
             builder.button(
            text=f"{i[1]} ", callback_data=NumbersCallbackFactory(action="select", value=f"{i[0]}", val=f"{i[1]}")
            )
    builder.button(
        text=f"➕ К Поступлению", callback_data=NumbersCallbackFactory(action="incr", value=f"55", val=f"")
    )
    builder.adjust(1)
    return builder.as_markup()


def gen_markup_deb(data):
    builder = InlineKeyboardBuilder()
    for i in data:
        builder.button(
            text=f"{i[1]} ", callback_data=NumbersCallbackFactory(action="select", value=f"{i[0]}", val=f"{i[1]}")
        )
    builder.button(
        text=f"➖ К Расходам", callback_data=NumbersCallbackFactory(action="decr", value=f"66", val=f"gjhgh")
    )
    builder.adjust(1)
    return builder.as_markup()

class Callback_Point(CallbackData, prefix="fabnum"):
    action: str
    value: Optional[str] = None
class NumbersCallbackFactory(CallbackData, prefix="fabnum"):
    action: str
    value: Optional[int] = None
    val: Optional[str] = None
    name: Optional[str] = None

class Itog_Callback(CallbackData, prefix="fabnum"):
    action: str
    mes_id: Optional[int] = None
    id_tranz: Optional[int] = None
    val: Optional[int] = None


class Flight_Callback(CallbackData, prefix="my"):
    action: str
    id_fl: Optional[int] = None
    st_fl: Optional[str] = None


class Div_Call(CallbackData, prefix="my"):
    action: str
    div_id: Optional[int] = None
    div_str: Optional[str] = None
    div_dat: Optional[str] = None

def key_flight():
    builder = InlineKeyboardBuilder()
    builder.button(
        text="🛣 Да", callback_data=Flight_Callback(action="fli_okdist")
    )
    builder.button(
        text="❌ Отмена", callback_data=Flight_Callback(action="now_cars")
    )
    builder.adjust(2)
    return builder.as_markup()




def key_flight_confirmation():
    builder = InlineKeyboardBuilder()
    builder.button(
        text="🛣 Да", callback_data=Flight_Callback(action="fli_confirmation")
    )
    builder.button(
        text="❌ Отмена", callback_data=Flight_Callback(action="now_cars")
    )
    builder.adjust(2)
    return builder.as_markup()

def key_fl_config(on,ac,rep_ts):
    builder = InlineKeyboardBuilder()
    builder.button(
        text=on, callback_data=Flight_Callback(action=ac)
    )
    if rep_ts != "":

        for i in rep_ts:
            builder.button(

                text=f"Вернуть ТС в рейс от {i[1]} {(i[2])[:-6]}",
                callback_data=Flight_Callback(action="repair_off", id_fl=f"{i[0]}", st_fl=f"{i[1]} от {(i[2])[:-6]}")
            )
        # builder.button(
        #     text="Вернуть ТС из ремонта", callback_data=Flight_Callback(action="repair_off", id_fl=f"{rep_ts}")
        # )
    builder.button(
        text="🛤 Список Рейсов", callback_data=Flight_Callback(action="list_flights")
    )

    builder.adjust(1)
    return builder.as_markup()


def key_fl_config_activ(on,ac,id_fl,rep_ts):
    builder = InlineKeyboardBuilder()
    builder.button(
        text=on, callback_data=Flight_Callback(action=ac)
    )
    builder.button(
        text="⛽️ Список Заправок", callback_data=Flight_Callback(action="list_fuels", id_fl = f"{id_fl}")
    )
    builder.button(
        text="Список Расходов", callback_data=Flight_Callback(action="list_pay", id_fl = f"{id_fl}")
    )
    builder.button(
        text="Список Поступлений", callback_data=Flight_Callback(action="list_receipt", id_fl = f"{id_fl}")
    )
    builder.button(
        text="🛤 Список Рейсов", callback_data=Flight_Callback(action="list_flights")
    )
    builder.button(
        text="Отчёт", callback_data=Flight_Callback(action="order_flights", id_fl = f"{id_fl}")
    )
    if rep_ts != "":

        for i in rep_ts:
            builder.button(

                text=f"Вернуть ТС в рейс от {i[1]} {(i[2])[:-6]}",
                callback_data=Flight_Callback(action="repair_off", id_fl=f"{i[0]}", st_fl=f"{i[1]} от {(i[2])[:-6]}")
            )
    builder.button(
        text="🛠 Отправить ТС в ремонт", callback_data=Flight_Callback(action="order_repair", id_fl = f"{id_fl}")
    )
    builder.adjust(1)
    return builder.as_markup()

def key_fl_new():
    builder = InlineKeyboardBuilder()
    builder.button(
        text="🛣 Начать", callback_data=Flight_Callback(action="fli_new")
    )
    builder.button(
        text="❌ Отмена", callback_data=Flight_Callback(action="now_cars")
    )
    builder.adjust(2)
    return builder.as_markup()


def gen_select_cars(data):
    builder = InlineKeyboardBuilder()
    for i in data:
        builder.button(

            text=f"{i[1]} {i[2]} {i[3]}", callback_data=NumbersCallbackFactory(action="selcars", value=f"{i[0]}", val=f"{i[1]} {i[3]}")
        )

    builder.button(
            text="❌ Отмена", callback_data=Flight_Callback(action="now_cars")
    )
    builder.adjust(1)
    return builder.as_markup()


def gen_select_point(data):
    builder = InlineKeyboardBuilder()
    for i in data:
        builder.button(

            text=f"{i[0]}", callback_data=Callback_Point(action="point", value=f"{i[0]}")
        )

    builder.adjust(1)
    return builder.as_markup()

def gen_list_flights(data):
    builder = InlineKeyboardBuilder()
    status = ""
    for i in data:
        st = i[2]
        if i[2] == "active":
            status = "(открыт)"
        else:
            status = "(завершен)"
        builder.button(

            text=f"{i[0]} от {i[1]} {status}", callback_data=Flight_Callback(action="order_flights", id_fl=f"{i[3]}", st_fl=f"{i[2]}")
        )


    builder.adjust(1)
    return builder.as_markup()


def gen_list_pay(data):
    builder = InlineKeyboardBuilder()
    status = ""
    for i in data:

        date = datetime.strptime((i[3]), '%Y-%m-%d %H:%M:%S')

        builder.button(

            text=f"{i[1]} от {date.strftime('%d-%m-%y %H:%M')} на: {i[2]}р.", callback_data=Callback_Point(action="pays", value=f"{i[0]}")
        )

    builder.adjust(1)
    return builder.as_markup()


def gen_key_exel(flight_id):
    builder = InlineKeyboardBuilder()

    builder.button(
        text="📋 Создать Exel отчёт", callback_data=Flight_Callback(action="order_flights_exel", id_fl=f"{flight_id}")
    )
    builder.button(
        text="📄 Создать Pdf отчёт", callback_data=Flight_Callback(action="order_flights_pdf", id_fl=f"{flight_id}")
    )

    builder.adjust(1)
    return builder.as_markup()

def gen_list_fuels(data):
    builder = InlineKeyboardBuilder()

    for i in data:
        date = datetime.strptime((i[1]), '%Y-%m-%d %H:%M:%S')
        builder.button(

            text=f"{date.strftime('%d-%m %H:%M')} на: {i[3]}р, {i[2]}л.", callback_data=Callback_Point(action="fuelse", value=f"{i[0]}")
        )


    builder.adjust(1)
    return builder.as_markup()

def gen_list_cat(data):
    builder = InlineKeyboardBuilder()
    wiring = ""
    for i in data:
        if i[2] == "decr":
            wiring = "(расход)"

        elif i[2] == "incr":
            wiring = "(приход)"
        builder.button(

            text=f"{i[1]} {wiring}", callback_data=NumbersCallbackFactory(action="edit_cats", name=f"{i[1]}",value=f"{i[0]}", val=f"{i[2]}")
        )
    builder.button(
            text="💼 Добавить категорию", callback_data=NumbersCallbackFactory(action="ins_cat")
    )
    builder.button(
            text="🔚 Выход", callback_data=NumbersCallbackFactory(action="edit_cats_ex")
    )
    builder.adjust(1)
    return builder.as_markup()

def gen_list_cat_nul():
    builder = InlineKeyboardBuilder()
    wiring = ""

    builder.button(
            text="💼 Добавить категорию", callback_data=NumbersCallbackFactory(action="ins_cat")
    )
    builder.button(
        text="📔 Заполнить по умолчанию", callback_data=NumbersCallbackFactory(action="ins_cat_def")
    )
    builder.button(
            text="🔚 Выход", callback_data=NumbersCallbackFactory(action="edit_cats_ex")
    )
    builder.adjust(1)
    return builder.as_markup()

def gen_edits_cat(id, wiring_n,name_cat,wiring):
    builder = InlineKeyboardBuilder()

    builder.button(
            text = "Удалить", callback_data = NumbersCallbackFactory(action="edit_cats_del", value=f"{id}", name=f"{name_cat}")
    )
    builder.button(
            text=f"В {wiring_n}", callback_data=NumbersCallbackFactory(action="edit_cats_wiring", value=f"{id}", name=f"{name_cat}", val =f"{wiring}")
    )
    builder.button(
            text="Как топливо", callback_data=NumbersCallbackFactory(action="edit_cats_fuel", value=f"{id}", name=f"{name_cat}")
    )
    builder.button(
            text="🔚 Выход", callback_data=NumbersCallbackFactory(action="edit_cats_ex")
    )
    builder.adjust(1)
    return builder.as_markup()

    # action: str
    # value: Optional[int] = None
    # val: Optional[str] = None
    # name: Optional[str] = None
def get_dev_us_and(name,phone,sen_rec):
    name_oper = ""
    if name == "nul":
        name_oper = "us_dev_and_name"
    elif phone == "nul":
        name_oper = "us_dev_and_phone"

    builder = InlineKeyboardBuilder()
    builder.button(
        text="Создать", callback_data=NumbersCallbackFactory(action=name_oper, val=sen_rec)
    )
    builder.button(
        text="❌ Отмена", callback_data=NumbersCallbackFactory(action="tr_cancel")
    )
    builder.adjust(2)
    return builder.as_markup()


   # action: str
    # value: Optional[int] = None
    # val: Optional[str] = None
    # name: Optional[str] = None
def get_dev_us_sel(data,action):
    builder = InlineKeyboardBuilder()
    wiring = ""
    for i in data:
        builder.button(

            text=f"{i[1]}", callback_data=NumbersCallbackFactory(action=action, name=f"{i[1]}",value=f"{i[0]}")
        )

    builder.button(
            text="🔚 Выход", callback_data=NumbersCallbackFactory(action="edit_cats_ex")
    )
    builder.adjust(1)
    return builder.as_markup()


# class Div_Call(CallbackData, prefix="my"):
#     action: str
#     div_id: Optional[int] = None
#     div_str: Optional[str] = None
#     div_dat: Optional[str] = None

def get_dev_us_sel2(data,action):
    builder = InlineKeyboardBuilder()
    wiring = ""
    for i in data:
        builder.button(

            text=f"{i[1]}", callback_data=Div_Call(action=action, div_str=f"{i[1]}",div_id=f"{i[0]}")
        )

    builder.button(
            text="🔚 Выход", callback_data=NumbersCallbackFactory(action="edit_cats_ex")
    )
    builder.adjust(1)
    return builder.as_markup()

def get_dev_fin():
    builder = InlineKeyboardBuilder()
    builder.button(
        text="✅ Да", callback_data=NumbersCallbackFactory(action="devi_insert")
    )
    builder.button(
            text="🙅‍♂️ Нет", callback_data=NumbersCallbackFactory(action="edit_cats_ex")
    )
    builder.adjust(1)
    return builder.as_markup()


def get_dev_pan():

    builder = InlineKeyboardBuilder()
    builder.button(
        text="📦 Принять в доставку", callback_data=Div_Call(action="dev_add")
    )
    builder.button(
        text="🚚 Выдать доставку", callback_data=Div_Call(action="dev_end")
    )

    builder.adjust(1)
    return builder.as_markup()



def get_keyboard_dev(id_tranz,mes_id):
    builder = InlineKeyboardBuilder()
    builder.button(
        text="📆 Уточнить дату", callback_data=Div_Call(action="tr_date", div_id=id_tranz)
    )
    builder.button(
        text="📝 Комментарий", callback_data=Div_Call(action="tr_caments", div_id=id_tranz)
    )
    builder.button(
        text="📸 Прикрепить фото",
        callback_data=Div_Call(action="dev_photo", div_id=id_tranz)
    )
    builder.button(
        text="❌ Отмена", callback_data=Div_Call(action="del_tr_deliv", div_id=id_tranz)
    )
    builder.adjust(2)
    return builder.as_markup()

def get_dev_delivir_sel(data):
    builder = InlineKeyboardBuilder()
    action = "to_deliver"
    pay = ""
    for i in data:
        if i[3] != None:
            pay = "💲 "
        else:
            pay = ""
            # print(i[3])
        builder.button(

            text=f"{pay}({i[0]}) {i[2]}", callback_data=Div_Call(action="open_pack",div_id=i[4])
        )

    builder.button(
            text="🔚 Выход", callback_data=NumbersCallbackFactory(action="edit_cats_ex")
    )
    builder.adjust(1)
    return builder.as_markup()

def get_pac_dev(id_tranz,photo):


    builder = InlineKeyboardBuilder()
    builder.button(
        text="📦 Выдать", callback_data=Div_Call(action="pack_issue", div_id=id_tranz)
    )
    builder.button(
        text="💵 Принять оплату", callback_data=Div_Call(action="ыв", div_id=id_tranz)
    )
    builder.button(
        text="📸 Добавить Фото", callback_data=Div_Call(action="dev_photo", div_id=id_tranz)
    )
    if photo == 1:
        builder.button(
            text="📷 Просмотреть фото",
            callback_data=Div_Call(action="open_pack_foto", div_id=id_tranz)
        )
    builder.button(
        text="📝 Уст. Размеры", callback_data=Div_Call(action="dev_set_size", div_id=id_tranz)
    )
    builder.button(
        text="📝 Указать вес", callback_data=Div_Call(action="dev_set_weight", div_id=id_tranz)
    )

    builder.button(
        text="❌ Назад", callback_data=Div_Call(action="dev_end")
    )
    builder.adjust(2)
    return builder.as_markup()


# class Div_Call(CallbackData, prefix="my"):
#     action: str
#     div_id: Optional[int] = None
#     div_str: Optional[str] = None
#     div_dat: Optional[str] = None

def get_pac_dev_qu(id_tranz):


    builder = InlineKeyboardBuilder()
    builder.button(
        text="📦 Выдать", callback_data=Div_Call(action="devi_insert", div_id=id_tranz)
    )
    builder.button(
        text="❌ Отмена", callback_data=Div_Call(action="open_pack", div_id=id_tranz)
    )
    builder.adjust(2)
    return builder.as_markup()

def get_pac_dev_qu_foto(id_tranz):
    builder = InlineKeyboardBuilder()
    builder.button(
        text="📦 К отправлению", callback_data=Div_Call(action="open_pack", div_id=id_tranz)
    )
    builder.button(
        text="❌ Выход", callback_data=Div_Call(action="", div_id=id_tranz)
    )
    builder.adjust(2)
    return builder.as_markup()