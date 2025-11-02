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

from main import is_number, now1

form_router = Router()

class Delivery(StatesGroup):
    and_us = State()
    and_phone = State()
    sender = State()
    recipient = State()
    sender_city = State()
    recipient_city = State()
    photo = State()



# # Обработка доставок
@form_router.message(Command("delivery"))
async def buy(message: types.Message, state: FSMContext):
    await message.answer(
        f"Управление доставками",
        reply_markup=keyboards.keyboard.get_dev_pan()
    )

# # Обработка доставок
@form_router.message(Command("ph"))
async def buy(message: types.Message, state: FSMContext):
    await message.answer(
        f"Пришли мне фото",
        reply_markup=keyboards.keyboard.get_dev_pan()
    )


    await state.set_state(Delivery.photo)
    # await  keyboards.keyboard.Div_Call.action = "sdsds"



###########################


@form_router.message(Delivery.photo)
async def process_write_mileage(message: Message, state: FSMContext) -> None:
    us_id = "555115"
    id = message.photo[0].file_id
    # print(message.photo[0].file_id)

    data = await state.get_data()
    id_pac = data["id_pac"]
    user_id = message.from_user.id
    await sqlite.db_isrt_foto(id,id_pac,user_id,now1)

    file_name = f"foto/{id}.jpg"
    await message.bot.download(file=message.photo[-1].file_id, destination=file_name)
    await message.answer(
        "Фото загружено,\n Выбери дальнейшее действие.",
        reply_markup=keyboards.keyboard.get_pac_dev_qu_foto(id_pac)
    )


###########################


@form_router.callback_query(keyboards.keyboard.Div_Call.filter(F.action == "dev_add"))
async def callbacks_num(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text("Введи номер или Фамилию отправителя")
    await state.set_state(Delivery.sender)

@form_router.message(Delivery.sender)
async def process_write_mileage(message: Message, state: FSMContext) -> None:
    print(message.text)
    text = message.text
    if is_number(text):

        data = await sqlite.db_dev_user_ph(text)
        if len(data) == 0:
            await message.reply(
                f"Контакт по номеру <b>{text}</b> не найден, Рекомендуется проверить данные если нужно исправить их или создать запись по кнопке.",
                reply_markup=keyboards.keyboard.get_dev_us_and("nul",text,"sender")
            )
            # await state.clear()
            await state.update_data(phone=text)
            # await state.set_state(Delivery.sender)
        else:
            for i in data:
                print(i[1])
            await message.reply(
                f"Найдены :",
                reply_markup=keyboards.keyboard.get_dev_us_sel(data,"senders")
            )

    else:

        data = await sqlite.db_dev_user_name(f"%{text.capitalize()}%")
        print(data)
        if len(data) == 0:
            await message.reply(
                f"Контакт по ФИО <b>{text}</b> не найден, Рекомендуется проверить данные если нужно исправить их или создать запись по кнопке.",
                reply_markup=keyboards.keyboard.get_dev_us_and(text,"nul", "sender")
            )
            await state.update_data(name=text)
            await state.set_state(Delivery.sender)
        else:
            for i in data:
                print(i[1])
            await message.reply(
                f"Найдены:",
                reply_markup=keyboards.keyboard.get_dev_us_sel(data,"senders")
            )


@form_router.callback_query(keyboards.keyboard.NumbersCallbackFactory.filter(F.action == "us_dev_and_phone"))
async def process_name_flight(
        callback: types.CallbackQuery,
        callback_data: keyboards.keyboard.NumbersCallbackFactory,
        state: FSMContext) -> None:

    await state.update_data(sen_rec=callback_data.val)

    data = await state.get_data()
    name = data["name"]
    await callback.message.edit_text(f'Наименование {name}.\nВведите номер в формате "+71231234567"')
    await state.set_state(Delivery.and_phone)

@form_router.callback_query(keyboards.keyboard.NumbersCallbackFactory.filter(F.action == "us_dev_and_name"))
async def process_name_flight(
        callback: types.CallbackQuery,
        callback_data: keyboards.keyboard.NumbersCallbackFactory,
        state: FSMContext) -> None:

    await state.update_data(sen_rec=callback_data.val)
    sen_rec = callback_data.val
    data = await state.get_data()
    phone = data["phone"]

    if sen_rec == "sender":

        await callback.message.edit_text(f'Номер тел. {phone}.\nВведите ФИО Отпровителя')
        await state.set_state(Delivery.and_us)

    elif sen_rec == "recipient":

        await callback.message.edit_text(f'Номер тел. {phone}.\nВведите ФИО Получателя')
        await state.set_state(Delivery.and_us)

@form_router.message(Delivery.and_us)
async def process_write_mileage(message: Message, state: FSMContext) -> None:
    name = message.text
    print(f"name {name}")
    data = await state.get_data()
    phone = data["phone"]
    sen_rec = data["sen_rec"]

    await sqlite.db_dev_user_insert_us(phone, name)

    if sen_rec == "sender":
        await message.answer(f'Добавлен отпровитель с данными:\nНомер тел.: {phone}.\nФИО: {name}')
        await state.set_state(Delivery.sender_city)
        await message.answer(f'Введите город отправления или выбрать')

        dat = await sqlite.db_dev_sel_id_user(name, phone)
        for i in dat:
            id = i[0]
            name_s = i[1]

            await state.update_data(senders_id=id)
            await state.update_data(senders_name=name_s)

    elif sen_rec == "recipient":
        await message.answer(f'Добавлен получатель с данными:\nНомер тел.: {phone}.\nФИО: {name}')
        await message.answer(f'Ввести город получения или выбрать')

        await state.set_state(Delivery.recipient_city)

        dat = await sqlite.db_dev_sel_id_user(name, phone)
        for i in dat:
            id = i[0]
            name_s = i[1]

            await state.update_data(recipient_id=id)
            await state.update_data(recipient_name=name_s)



@form_router.message(Delivery.and_phone)
async def process_write_mileage(message: Message, state: FSMContext) -> None:
    phone = message.text
    data = await state.get_data()
    name = data["name"]
    sen_rec = data["sen_rec"]

    await sqlite.db_dev_user_insert_us(phone,name)
    dat = await sqlite.db_dev_sel_id_user(name,phone)
    id = 0
    name_s =""
    for i in dat:

        id = i[0]
        name_s = i[1]

    if sen_rec == "sender":
        await message.answer(f'Добавлен отпровитель с данными:\nНомер тел.: {phone}.\nФИО: {name}')
        await state.set_state(Delivery.sender_city)
        await message.answer(f'Введите город отправления или выбрать')
        await state.update_data(senders_id=id)
        await state.update_data(senders_name=name_s)


    elif sen_rec == "recipient":
        await message.answer(f'Добавлен получатель с данными:\nНомер тел.: {phone}.\nФИО: {name}')
        await state.set_state(Delivery.recipient_city)
        await message.answer(f'Ввести город получения или выбрать')
        await state.update_data(recipient_id=id)
        await state.update_data(recipient_name=name_s)



@form_router.message(Delivery.sender_city)
async def process_write_mileage(message: Message, state: FSMContext) -> None:
    await state.update_data(sender_city=message.text)
    await message.answer(f'Введи номер или ФИО получателя')
    await state.set_state(Delivery.recipient)


@form_router.message(Delivery.recipient)
async def process_write_mileage(message: Message, state: FSMContext) -> None:
    recipient = message.text
    print(message.text)
    if is_number(recipient):
        data = await sqlite.db_dev_user_ph(recipient)
        if len(data) == 0:
            await message.reply(
                f"Контакт по номеру <b>{recipient}</b> не найден, Рекомендуется проверить данные если нужно исправить их или создать запись по кнопке.",
                reply_markup=keyboards.keyboard.get_dev_us_and("nul", recipient, "recipient")
            )
            await state.update_data(phone=recipient)
        else:
            for i in data:
                print(i[1])
            await message.reply(
                f"Найдены:",
                reply_markup=keyboards.keyboard.get_dev_us_sel2(data, "recipient")
            )
    else:

        data = await sqlite.db_dev_user_name(f"%{recipient.capitalize()}%")
        print(data)
        if len(data) == 0:
                await message.reply(
                    f"Контакт по ФИО <b>{recipient}</b> не найден, Рекомендуется проверить данные если нужно исправить их или создать запись по кнопке.",
                    reply_markup=keyboards.keyboard.get_dev_us_and(recipient, "nul", "recipient")
                )
                await state.update_data(name=recipient)

        elif len(data) != 0:
            # for i in data:
            #     print(i[1])
            await message.reply(
                 f"Найдены:",
                 reply_markup=keyboards.keyboard.get_dev_us_sel2(data, "recipient")
            )
            # await state.set_state(Delivery.sender_city)



@form_router.callback_query(keyboards.keyboard.Div_Call.filter(F.action == "recipient"))
async def process_name_flight(
        callback: types.CallbackQuery,
        callback_data: keyboards.keyboard.Div_Call,
        state: FSMContext) -> None:
    recipient_id = callback_data.div_id
    recipient_name = callback_data.div_str
    await state.update_data(recipient_id=recipient_id)
    await state.update_data(recipient_name=recipient_name)
    await callback.message.edit_text(f'Введите город получения или выбрать')
    await state.set_state(Delivery.recipient_city)



@form_router.message(Delivery.recipient_city)
async def process_write_mileage(message: Message, state: FSMContext) -> None:
    recipient_city = message.text
    await state.update_data(recipient_city=recipient_city)
    data = await state.get_data()
    senders_name = data["senders_name"]
    sender_city = data["sender_city"]
    recipient_name = data["recipient_name"]
    recipient_city = data["recipient_city"]
    print(data)
    await message.answer(
        f'Отпровитель: {senders_name} из {sender_city} \nПолучатель: {recipient_name} в {recipient_city}\n Офрмить ?',
        reply_markup=keyboards.keyboard.get_dev_fin()
    )

@form_router.callback_query(keyboards.keyboard.NumbersCallbackFactory.filter(F.action == "devi_insert"))
async def callbacks_num_change_fab(
        callback: types.CallbackQuery,
        state: FSMContext) -> None:

    data = await state.get_data()
    senders_name = data["senders_name"]
    sender_city = data["sender_city"]
    recipient_name = data["recipient_name"]
    recipient_city = data["recipient_city"]
    senders_id = data["senders_id"]
    recipient_id = data["recipient_id"]
    id = await sqlite.db_dev_insert(senders_id,sender_city,now1,recipient_id,recipient_city,"Принят")
    #
    # text_ms = f"Получатель {recipient_name} в {recipient_city}"

    await callback.message.edit_text(
        f"Добавлено №: {id} \n "
        f"Отпровитель: {senders_name} из {sender_city} \n"
        f"Получатель: {recipient_name} в {recipient_city}\n",
        reply_markup=keyboards.keyboard.get_keyboard_dev(id,callback.message.message_id)
    )
    await state.clear()

@form_router.callback_query(keyboards.keyboard.NumbersCallbackFactory.filter(F.action == "senders"))
async def process_name_flight(
        callback: types.CallbackQuery,
        callback_data: keyboards.keyboard.NumbersCallbackFactory,
        state: FSMContext) -> None:
    # await sqlite
    senders_id = callback_data.value
    senders_name = callback_data.name
    await state.update_data(senders_name=senders_name)
    await state.update_data(senders_id=senders_id)
    await callback.message.edit_text(f'Введите город отправления или выбрать')
    await state.set_state(Delivery.sender_city)


@form_router.callback_query(keyboards.keyboard.Div_Call.filter(F.action == "dev_end"))
async def process_name_flight(
        callback: types.CallbackQuery,
        callback_data: keyboards.keyboard.Div_Call,
        state: FSMContext) -> None:
    data = await sqlite.db_dev_for_issuance()
    await callback.message.edit_text(
        "Выбери отправления:",
        reply_markup=keyboards.keyboard.get_dev_delivir_sel(data)
    )
    print(f"data {data}")


## Перейти в посылку
@form_router.callback_query(keyboards.keyboard.Div_Call.filter(F.action == "open_pack"))
async def process_name_flight(
        callback: types.CallbackQuery,
        callback_data: keyboards.keyboard.Div_Call,
        state: FSMContext) -> None:
        # await handle_command_pic(callback)

        id_pac = callback_data.div_id
        photo = 0
        data = await sqlite.db_sel_pack(id_pac)
        data_foto = await sqlite.db_sel_pack_foto(id_pac)
        if len(data_foto) != 0:
            photo = 1
        else:
            photo = 0

        text_ms =""
        id_photo=""

        for i in data:

            print(i[0])
            # text_ms =f" из {i[0]} от \n{i[1]} \nв {i[3]} для <b>{i[2]}</b>\nДата отправления: {i[5]}\n📱  Телефон: \nК оплатте: <b>{i[4]}</b>"
            text_ms = f"\n🏠 Отпровитель: {i[0]} от \n{i[1]} \n📱  Телефон: {i[7]}\n\nПолучатель: <b>{i[2]}</b>\n📱  Телефон: {i[8]}\n🏠 Адрес: <b>{i[3]}</b>\n\nДата отправления: {i[5]}\n\nК оплатте: <b>{i[4]}</b>"

        await callback.message.edit_text(
            f"Отправление №{id_pac}\n {text_ms}",
            reply_markup=keyboards.keyboard.get_pac_dev(id_pac,photo)
        )


@form_router.callback_query(keyboards.keyboard.Div_Call.filter(F.action == "open_pack_foto"))
async def process_name_flight(
        callback: types.CallbackQuery,
        callback_data: keyboards.keyboard.Div_Call,
        state: FSMContext) -> None:
    # await handle_command_pic(callback)

    id_pac = callback_data.div_id

    data = await sqlite.db_sel_pack(id_pac)
    data_foto = await sqlite.db_sel_pack_foto(id_pac)


    ph1 = ()
    id_photo = ""
    text_ms = ""
    photos = []
    for ii in data_foto:
        photos.append(types.InputMediaPhoto(type='photo',media=ii[0],caption=ii[1]))


    await callback.message.reply_media_group(
         media=photos
    )  # Отправка фото


    # f"foto/{id}.jpg"
    #
    # for i in data:
    #     # print(i[0])
    #     id_photo = f"{i[6]}"
    #     print(i[6])
    #     text_ms = f" из {i[0]} от \n{i[1]} \nв {i[3]} для <b>{i[2]}</b>\nДата отправления: {i[5]}\nК оплатте: <b>{i[4]}</b>"

    # if id_photo != None:
    #     # await callback.message.reply_photo(
    #     #     photo=id_photo,
    #     #     caption=f"{text_ms}",
    #     #     reply_markup=keyboards.keyboard.get_pac_dev(id_pac,1)
    #     # )
    #     # await callback.message.reply_media_group(media=data_foto)
    #     await callback.message.edit_text(
    #         f"Фото отсутствует.\nОтправление №{id_pac} {text_ms}",
    #         reply_markup=keyboards.keyboard.get_pac_dev(id_pac)
    #     )
    #
    # else:
    #     await callback.message.edit_text(
    #         f"Фото отсутствует.\nОтправление №{id_pac} {text_ms}",
    #         reply_markup=keyboards.keyboard.get_pac_dev(id_pac)
    #     )


@form_router.callback_query(keyboards.keyboard.Div_Call.filter(F.action == "pack_issue"))
async def process_name_flight(
        callback: types.CallbackQuery,
        callback_data: keyboards.keyboard.Div_Call,
        state: FSMContext) -> None:

        id_pac = callback_data.div_id

        await callback.message.edit_text(
            "Вы действительно хотите выдать посылку ?",
            reply_markup=keyboards.keyboard.get_pac_dev_qu(id_pac)
        )

        # await state.set_state(Delivery.photo)


@form_router.callback_query(keyboards.keyboard.Div_Call.filter(F.action == "pack_issue1"))
async def process_name_flight(
        callback: types.CallbackQuery,
        callback_data: keyboards.keyboard.Div_Call,
        state: FSMContext) -> None:
    id_pac = callback_data.div_id

    await sqlite.db_issue_pack(id_pac,"доставлен")

    await callback.message.edit_text(
        f'Статус отправления №{id_pac} изменен на "Выдано"'
    )

@form_router.callback_query(keyboards.keyboard.Div_Call.filter(F.action == "dev_photo"))
async def process_name_flight(
        callback: types.CallbackQuery,
        callback_data: keyboards.keyboard.Div_Call,
        state: FSMContext) -> None:

        id_pac = callback_data.div_id
        await state.update_data(id_pac = id_pac)
        await callback.message.edit_text("Отправь фото")
        await state.set_state(Delivery.photo)

@form_router.callback_query(keyboards.keyboard.Div_Call.filter(F.action == "del_tr_deliv"))
async def process_name_flight(
        callback: types.CallbackQuery,
        callback_data: keyboards.keyboard.Div_Call,
        state: FSMContext) -> None:

        id = callback_data.div_id
        mes_txt = f"Отправление №:{id} из: "
        mes = await sqlite.db_dev_delliv(id)
        for i in mes:
                mes_txt = mes_txt + i[0]
                mes_txt = mes_txt + " от "+i[1]
                mes_txt = mes_txt + " в "+ i[2]
                mes_txt = mes_txt +" для "+i[3]

        print(f"mes: {mes} mes_txt: {mes_txt}")
        await callback.message.edit_text(f"🚫 Отменено\n---\n{mes_txt} \n---\n")

