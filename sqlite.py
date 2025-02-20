import sqlite3 as sq

async def db_connect() -> None:
    global db, cur
    db = sq.connect('my_database.db')
    cur = db.cursor()
    cur.execute("CREATE TABLE categorys (name   TEXT    NOT NULL,user   INTEGER NOT NULL,wiring TEXT  NOT NULL)")
    db.commit()


async def db_select_cat() -> None:
    global db, cur
    db = sq.connect('my_database.db')
    cur = db.cursor()
    cur.execute("SELECT TABLE categorys (name   TEXT    NOT NULL,user   INTEGER NOT NULL,wiring TEXT  NOT NULL)")
    db.commit()

async def db_insert_cat(stroka: str, name_wr: str, us_id: int, fuel: str) -> None:
    global db, cur
    db = sq.connect('my_database.db')
    cur = db.cursor()
    cur.execute("INSERT INTO categorys (name,user,wiring,fuel)VALUES (?,?,?,? )", (stroka, us_id, name_wr, fuel))
    db.commit()


async def db_insert_transactions(cat: int, us_id: int, cash: int, data: str, flight: int, fuel: str):
    global db, cur
    db = sq.connect('my_database.db')
    cur = db.cursor()
    cur.execute("INSERT INTO transactions (category,date,user_id,sum_cash,flight,fuel)VALUES (?,?,?,?,?,? )", (cat, data, us_id, cash, flight, fuel))
    data = cur.execute('''SELECT id FROM transactions WHERE category =? AND user_id =? AND date =? AND sum_cash =? ''', (cat,us_id,data,cash), ).fetchall()
    db.commit()
    return data

async def db_del_transactions(id: int, us_id: int) -> None:
    global db, cur
    db = sq.connect('my_database.db')
    cur = db.cursor()
    cur.execute("DELETE FROM transactions WHERE id = ? AND user_id = ?", (id,us_id))
    db.commit()

async def update_trans_com(coment: str, id: int) -> None:
    global db, cur
    db = sq.connect('my_database.db')
    cur = db.cursor()
    cur.execute("UPDATE transactions SET comments = ? WHERE id = ?", (coment,id))
    db.commit()
async def update_trans_date(date: str, id: int) -> None:
    global db, cur
    db = sq.connect('my_database.db')
    cur = db.cursor()
    cur.execute("UPDATE transactions SET date = ? WHERE id = ?", (date,id))
    db.commit()


async def db_sel_cat(user,wiring):
    global db, cur
    db = sq.connect('my_database.db')
    cur = db.cursor()
    data = cur.execute('''SELECT id, name,fuel FROM categorys WHERE user =? AND wiring =? ''', (user, wiring),).fetchall()

    db.commit()
    return data

async def db_sel_edit_cat(user):
    global db, cur
    db = sq.connect('my_database.db')
    cur = db.cursor()
    data = cur.execute(
        '''SELECT id, name, wiring FROM categorys WHERE user = ? AND (wiring = "decr" OR wiring = "incr") ''',
        (user,),).fetchall()
    db.commit()
    return data


async def db_sel_default_cat():
    global db, cur
    db = sq.connect('my_database.db')
    cur = db.cursor()
    data = cur.execute(
        '''SELECT name, wiring, fuel FROM categorys WHERE user = "default" AND (wiring = "decr" OR wiring = "incr") ORDER BY name ''').fetchall()
    db.commit()
    return data


async def db_sel_flight_name(user):
    global db, cur
    db = sq.connect('my_database.db')
    cur = db.cursor()
    data = cur.execute('SELECT name, in_date, status, id FROM flight WHERE user =? ORDER BY id DESC LIMIT 10',(user,)).fetchall()
    db.commit()
    return data

async def db_sel_nam_point(user):
    global db, cur
    db = sq.connect('my_database.db')
    cur = db.cursor()
    data = cur.execute('SELECT DISTINCT name FROM flight WHERE user =? ORDER BY id DESC LIMIT 8',(user,)).fetchall()
    db.commit()
    return data

async def sel_tranc(idi,user):
    global db, cur
    db = sq.connect('my_database.db')
    cur = db.cursor()
    data = cur.execute('''SELECT category, sum_cash, date FROM transactions WHERE id =? AND user_id =? ''',
                       (idi, user), ).fetchall()

    db.commit()
    return data

#### Рейс

async def db_insert_flight(name: str,
                           us_id: int,
                           in_fuel: int,
                           in_odometr: int,
                            in_date: str,
                            cars: int,
                            status: str
                            ) -> None:
    global db, cur
    db = sq.connect('my_database.db')
    cur = db.cursor()
    cur.execute("INSERT INTO flight (name,user,in_fuel,in_odometr,in_date,car,status)VALUES (?,?,?,?,?,?,? )", (name, us_id, in_fuel, in_odometr,in_date,cars,status))
    db.commit()

async def db_obdate_flight(id: int, fuel: int, odometr: int , date: str, status: str) -> None:
    global db, cur
    db = sq.connect('my_database.db')
    cur = db.cursor()
#    cur.execute("INSERT INTO flight (name,user,in_fuel,in_odometr,in_date,car)VALUES (?,?,?,?,?,? )", (name, us_id, in_fuel, in_odometr,in_date,cars))
    cur.execute(
        "UPDATE flight SET status = ?, end_date = ?, finish_odometr = ?, fuel_residues = ? WHERE id = ?",
        (status, date, odometr, fuel, id))

    db.commit()

async def db_repair_flight(id: int, status: str) -> None:
    global db, cur
    db = sq.connect('my_database.db')
    cur = db.cursor()
    cur.execute(
        "UPDATE flight SET status = ? WHERE id = ?",
        (status, id))

    db.commit()

async def db_sel_cars():
    global db, cur
    db = sq.connect('my_database.db')
    cur = db.cursor()
    data = cur.execute('''SELECT id, marka, model, nomer FROM cars''').fetchall()
    db.commit()
    return data


async def db_sel_flight(status, user):
    global db, cur
    # status ="active"
    # user = 611844283
    db = sq.connect('my_database.db')
    cur = db.cursor()
    data = cur.execute('''SELECT id, name, in_date, car,in_fuel,in_odometr FROM flight WHERE user =? AND status =? ''',
                       (user, status), ).fetchall()
    db.commit()
    return data

async def db_sel_tr_pay(id,wiring):
    global db, cur
    db = sq.connect('my_database.db')
    cur = db.cursor()
    data = cur.execute(
        'SELECT transactions.id,transactions.category,transactions.sum_cash,transactions.date '
                'FROM transactions '
                'JOIN categorys ON categorys.wiring = ? '
                'WHERE transactions.category = categorys.name AND transactions.user_id = categorys.user AND transactions.flight = ? ',
        (wiring, id)).fetchall()
    db.commit()
    return data

async def db_sel_tr_fuels(id):
    global db, cur
    db = sq.connect('my_database.db')
    cur = db.cursor()
    data = cur.execute('SELECT transactions.id,transactions.date,transactions.fuel, sum_cash '
                        'FROM transactions JOIN categorys ON categorys.fuel ="yes" '
                        'WHERE transactions.category = categorys.name AND transactions.flight = ?'
                        'AND transactions.user_id = categorys.user ORDER BY sum_cash DESC ',
                       (id,)).fetchall()
    db.commit()
    return data

async def db_sel_tr_other(id):
    global db, cur
    db = sq.connect('my_database.db')
    cur = db.cursor()
    data = cur.execute('SELECT transactions.id,transactions.date,transactions.category, sum_cash, comments '
                       'FROM transactions JOIN categorys ON categorys.wiring ="decr" '
                       'WHERE transactions.category = categorys.name AND transactions.fuel = "" '
                       'AND transactions.user_id = categorys.user AND transactions.flight = ? ',
                       (id,)).fetchall()
    db.commit()
    return data

async def db_sel_other_shapka(id):
    global db, cur
    db = sq.connect('my_database.db')
    cur = db.cursor()
    data = cur.execute('SELECT '
                       'flight.name,cars.marka,cars.model,cars.nomer,'
                       'flight.in_date,flight.end_date,'
                       'flight.in_odometr, flight.finish_odometr,'
                       'flight.in_fuel,flight.fuel_residues,users.username '
                       'FROM flight JOIN cars ON flight.car = cars.id JOIN users ON flight.user = users.tg_id '
                       'WHERE flight.id = ? ',
                       (id,)).fetchall()
    db.commit()
    return data
async def db_del_edit_cat(id: int) -> None:
    global db, cur
    db = sq.connect('my_database.db')
    cur = db.cursor()
    cur.execute("DELETE FROM categorys WHERE id = ?", (id,))
    db.commit()

async def db_upg_edit_cat(id: int,fuels: str,wiring: str) -> None:
    global db, cur
    db = sq.connect('my_database.db')
    cur = db.cursor()
    # cur.execute("DELETE FROM categorys WHERE id = ?", (id,)

    cur.execute(
        "UPDATE categorys SET wiring = ?, fuel = ? WHERE id = ?",
        (wiring, fuels, id))

    db.commit()


async def db_upg_edit_cat_wr(id: int,wiring: str) -> None:
    global db, cur
    db = sq.connect('my_database.db')
    cur = db.cursor()

    cur.execute(
        "UPDATE categorys SET wiring = ? WHERE id = ?",
        (wiring, id))

    db.commit()

async def db_sel_tr_order(id:int, wiring:str):
    global db, cur
    db = sq.connect('my_database.db')
    cur = db.cursor()
    data = cur.execute(
        'SELECT transactions.id,transactions.category, SUM(sum_cash),SUM(transactions.fuel) '
                     'FROM transactions '
                     'JOIN categorys ON categorys.wiring = ? '
                     'WHERE transactions.category = categorys.name '
                     'AND transactions.user_id = categorys.user AND transactions.flight = ? '
                     'GROUP BY category ORDER BY sum_cash DESC ',
        (wiring, id)).fetchall()

    db.commit()
    return data


async def db_order_info(id_fl: int):
    global db, cur
    db = sq.connect('my_database.db')
    cur = db.cursor()
    data = cur.execute(
        'SELECT flight.in_fuel, flight.fuel_residues, flight.in_odometr, flight.finish_odometr, flight.in_date, flight.end_date, cars.marka,cars.model '
        'FROM flight JOIN cars '
        'WHERE flight.car = cars.id AND flight.id = ? ',
        (id_fl,)).fetchall()
    db.commit()
    return data
async def db_sel_driver(id: int):
    global db, cur
    db = sq.connect('my_database.db')
    cur = db.cursor()
    data = cur.execute(
        'SELECT username FROM users WHERE tg_id = ?',
        (id,)).fetchall()
    db.commit()
    return data

async def db_insert_driver(id_tg: int, user_name: str):
    global db, cur
    db = sq.connect('my_database.db')
    cur = db.cursor()
    cur.execute("INSERT INTO users (username,tg_id)VALUES (?,? )",
                (user_name, id_tg))

    db.commit()


async def db_dev_user_ph(phone: str) -> None:
    global db, cur
    db = sq.connect('my_database.db')
    cur = db.cursor()
    data = cur.execute(
        "SELECT id, name FROM dev_users WHERE phone = ?",
        (phone, )).fetchall()
    db.commit()
    return data

async def db_dev_user_name(name: str) -> None:
    global db, cur
    db = sq.connect('my_database.db')
    cur = db.cursor()
    data = cur.execute(
        "SELECT id, name FROM dev_users WHERE name LIKE ?",
        (name, )).fetchall()
    db.commit()
    return data

async def db_dev_user_insert_us(phone: str, user_name: str):
    global db, cur
    db = sq.connect('my_database.db')
    cur = db.cursor()
    cur.execute("INSERT INTO dev_users (name,phone)VALUES (?,? )",
                (user_name, phone))
    db.commit()

async def db_dev_sel_id_user(name: str, phone) -> None:
    global db, cur
    db = sq.connect('my_database.db')
    cur = db.cursor()
    data = cur.execute(
        "SELECT id, name FROM dev_users WHERE name = ? AND phone = ?",
        (name,phone )).fetchall()
    db.commit()
    return data

async def db_dev_insert(sender_id: str, adres_in: str, date_and: str, recipient: id, adres_ex: str, status: str):
    global db, cur
    db = sq.connect('my_database.db')
    cur = db.cursor()
    cur.execute("INSERT INTO delivery (sender,adres_in,date_and,recipient,adres_ex,status)VALUES (?,?,?,?,?,? )",
                (sender_id, adres_in,date_and,recipient,adres_ex,status))
    id = cur.lastrowid
    db.commit()
    return id

async def db_dev_for_issuance():
    global db, cur
    db = sq.connect('my_database.db')
    cur = db.cursor()
    data = cur.execute(
        "SELECT o.adres_ex, u.name AS sender_name, u1.name AS recipient_name, o.payment, o.id "
        "FROM delivery AS o "
        "JOIN dev_users AS u ON o.sender = u.id "
        "JOIN dev_users AS u1 ON o.recipient = u1.id "
        "WHERE (o.status != 'доставлен' AND o.status != '') "
        ).fetchall()
    db.commit()
    return data

async def db_dev_delliv(id: str):
    global db, cur
    db = sq.connect('my_database.db')
    cur = db.cursor()

    data2 = cur.execute(
        "SELECT o.adres_in, u.name AS sender_name, o.adres_ex, u1.name AS recipient_name "
        "FROM delivery AS o "
        "JOIN dev_users AS u ON o.sender = u.id "
        "JOIN dev_users AS u1 ON o.recipient = u1.id "
        "WHERE (o.status != 'доставлен' OR o.status != '') AND o.id = ? ", (id, )).fetchall()

    cur.execute(
        "DELETE FROM delivery WHERE id = ?  ",
        (id, )).fetchall()

    db.commit()
    return data2

async def db_sel_pack(id: int):
    global db, cur
    db = sq.connect('my_database.db')
    cur = db.cursor()

    data = cur.execute(
        "SELECT o.adres_in, u.name AS sender_name, u1.name AS recipient_name,o.adres_ex, o.payment, o.date_and, o.name_foto, u.phone, u1.phone "
        "FROM delivery AS o "
        "JOIN dev_users AS u ON o.sender = u.id "
        "JOIN dev_users AS u1 ON o.recipient = u1.id "
        "WHERE (o.status != 'доставлен' OR o.status != '') AND o.id = ? ", (id, )).fetchall()

    db.commit()
    return data

async def db_sel_pack_foto(id: int):
    global db, cur
    db = sq.connect('my_database.db')
    cur = db.cursor()

    data = cur.execute(
        "SELECT tg_id,date FROM foto WHERE id_delivery = ? ",
        (id, )).fetchall()
    db.commit()

    return data


async def db_issue_pack(id: int,status: str):
    global db, cur
    db = sq.connect('my_database.db')
    cur = db.cursor()
    cur.execute(
        "UPDATE delivery SET status = ? WHERE id = ?",
        (status,id ))
    db.commit()
    # return data

async def db_isrt_foto(tg_id: int,id_delivery: int,user: int,date: str):
    global db, cur
    db = sq.connect('my_database.db')
    cur = db.cursor()
    # cur.execute(
    #     "UPDATE delivery SET status = ? WHERE id = ?",
    #     (status,id ))

    cur.execute("INSERT INTO foto (tg_id,id_delivery,user,date)VALUES (?,?,?,? )",
                (tg_id, id_delivery, user, date))


    db.commit()
    # return data
