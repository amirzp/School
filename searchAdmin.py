import sqlite3


# #############SQLite3#################
conn = sqlite3.connect('file/database.db')
conn.execute("create table if not exists admin(id integer primary key, username text, password text)")
cursor = conn.cursor()


def sql_register(un, pw, _id):
    txt = "INSERT INTO admin(username, password) VALUES(?, ?)"
    txt_2 = "update admin set username=?, password=? where id=?"
    try:
        data = cursor.execute("select * from admin where username=?", (un, )).fetchone()
        if not data:
            if _id:
                cursor.execute(txt_2, (un, pw, _id))
            else:
                cursor.execute(txt, (un, pw))
            conn.commit()
            return True
        else:
            if _id:
                data_2 = cursor.execute("select * from admin where id=?", (_id,)).fetchone()
                if un == data_2[1]:
                    cursor.execute(txt_2, (un, pw, _id))
                    conn.commit()
                    return True
                else:
                    return False
            else:
                return False

    except sqlite3.IntegrityError:
        return False


######################################
def login(user, password):
    db = cursor.execute("SELECT username, password FROM admin where username = ?", (user, )).fetchone()
    if db:
        if password == db[1]:
            return True
    return False


def register(username, password, confirm_password, _id):
    if not (password == confirm_password):
        return None
    else:
        if sql_register(username, password, _id):
            return True
        else:
            return False
