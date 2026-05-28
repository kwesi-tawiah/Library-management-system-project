import sqlite3
import random


def finder(ids):
    ix = 0
    state = 0
    if not ids:
        user_id = random.randint(0, 100)
    else:
        limit = len(ids)
        while ix < limit:
            user_id = random.randint(0, 100)
            if not ids:
                return user_id, state
            if ids[ix] == user_id:
                state += 1
            ix += 1
    return user_id, state


def get_connection():
    conn = sqlite3.connect("Library.db")
    cursor = conn.cursor()
    return conn, cursor


def close(conn, cursor):
    if cursor:
        cursor.close()
    if conn:
        conn.close()


def create_table(table_type):
    fault, conn, cursor = False, None, None,
    try:
        conn, cursor = get_connection()

        if table_type.lower() == "users":

            cursor.execute("""
create table if not exists users(
user_id integer,
name text,
sex text,
email text,
phone_number text                                       
  ) 
  """)
            conn.commit()

        elif table_type.lower() == "borrow_history":

            cursor.execute("""
create table if not exists borrow_history(
user_id integer,
name text,
sex text,
email text,
phone_number text,
book_borrowed text,
datetime_borrowed text,
datetime_returned text,
returned text
)
""")
            conn.commit()

        elif table_type.lower() == "books":

            cursor.execute("""
create table if not exists books(
book_id integer,
book_name text,
year text,
author text,
borrow_time integer,
borrowed text                                                                       
)
""")

            conn.commit()

    except sqlite3.Error as error:
        if conn:
            conn.rollback()
        fault = True
        print(f"Connection error: {type(error).__name__}")
        print(error)

    finally:
        close(conn, cursor)
    return fault


def insert_into_users(name, sex, email, phone_number):
    user_id = None
    try:
        conn, cursor = None, None
        conn, cursor = get_connection()

        cursor.execute("""
select user_id from users
""")
        ids = cursor.fetchall()
        user_id, state = finder(ids)
        while True:
            if state != 0:
                user_id, state = finder(ids)
            elif state == 0:
                break

        cursor.execute("""
    insert into users(user_id, name, sex, email, phone_number)
    values(?, ?, ?, ?, ?)
    """, (user_id, name.lower(), sex.lower(), email.lower(), phone_number))
        conn.commit()

    except sqlite3.Error as error:
        if conn:
            conn.rollback()
        print(f"Insertion failed: {type(error).__name__}")
        print(error)

    finally:
        close(conn, cursor)
    return user_id


def insert_into_books(book_name, year, author, borrow_time):
    try:
        conn, cursor, user_id = None, None, None
        conn, cursor = get_connection()

        cursor.execute("""
select book_name, year, author from books""")

        cmps = cursor.fetchall()

        if not cmps:
            cursor.execute("""
select book_id from books
""")

            ids = cursor.fetchall()
            # if ids:
            user_id, state = finder(ids)
            while True:
                if state != 0:
                    user_id, state = finder(ids)
                elif state == 0:
                    break

            cursor.execute("""
insert into books(book_id, book_name, year, author, borrow_time, borrowed)
values(?, ?, ?, ?, ?, ?)
""", (user_id, book_name.lower(), year, author.lower(), borrow_time, "no"))
            conn.commit()

        # else:
        # print(
        #    "Book not added beacause the books ids failed to load. Please try again.")
        else:
            for book in cmps:
                if book[0].lower() == book_name.lower() and book[0].lower() == author.lower() and book[0] == year:
                    pass
            else:
                cursor.execute("""
select book_id from books
""")

            ids = cursor.fetchall()
            # if ids:
            user_id, state = finder(ids)
            while True:
                if state != 0:
                    user_id, state = finder(ids)
                elif state == 0:
                    break

            cursor.execute("""
insert into books(book_id, book_name, year, author, borrow_time, borrowed)
values(?, ?, ?, ?, ?, ?)
""", (user_id, book_name, year, author, borrow_time, "no"))
            conn.commit()

    except sqlite3.Error as error:
        if conn:
            conn.rollback()
        print(f"Insertion failed: {type(error).__name__}")
        print(error)

    finally:
        close(conn, cursor)
    return user_id


def insert_into_borrow_history_b(name, user_id, book_borrowed, datetime_borrowed):
    try:
        conn, cursor = None, None
        conn, cursor = get_connection()

        cursor.execute("""
select sex, email, phone_number from users where name = ? and user_id = ?
""", (name.lower(), user_id))

        person = cursor.fetchone()
        #print(person)
        if person:
            sex = person[0]
            email = person[1]
            phone_number = person[2]
        else:
            print(
                f"During history insertion {name.capitalize()} was not found.")

        cursor.execute("""
insert into borrow_history(user_id, name, sex, email, phone_number, book_borrowed, datetime_borrowed, returned) 
values(?, ?, ?, ?, ?, ?, ?, ?)
""", (user_id, name.lower(), sex.lower(), email.lower(), phone_number, book_borrowed.lower(), datetime_borrowed, "no"))

        cursor.execute("""
update books set borrowed = ? where book_name = ?
""", ("yes", book_borrowed.lower()))

        conn.commit()

    except sqlite3.Error as error:
        if conn:
            conn.rollback()
        print(f"Insertion failed: {type(error).__name__}")
        print(error)

    finally:
        close(conn, cursor)
    if not person:
        return False
    else:
        return True


def update_borrow_history_r(name, user_id, date, book_borrowed):
    conn, cursor, further = None, None, False
    try:
        returned = "yes"
        conn, cursor = get_connection()

        cursor.execute("""
update borrow_history set datetime_returned = ?, returned = ? where name = ? and user_id = ? and book_borrowed = ? and returned = ?
""", (date, returned, name.lower(), user_id, book_borrowed.lower(), "no"))

        conn.commit()

        cursor.execute("""
update books set borrowed = ? where book_name = ?
""", ("no", book_borrowed))

        conn.commit()

    except sqlite3.Error as error:
        if conn:
            conn.rollback()
        print(f"Update failed: {type(error).__name__}")
        print(error)
        further = True

    finally:
        close(conn, cursor)

    return further


def show_table(table_type):

    Users, fault = None, False

    conn, cursor = None, None

    try:
        conn, cursor = get_connection()

        if table_type.lower() == "users":

            cursor.execute("""
select * from users
""")
            Users = cursor.fetchall()

        elif table_type.lower() == "borrow_history":

            cursor.execute("""
select * from borrow_history
""")

            Users = cursor.fetchall()

        elif table_type.lower() == "books":

            cursor.execute("""
select * from books
""")
            Users = cursor.fetchall()

    except sqlite3.Error as error:
        print(
            f"Selection from table failed. Error type: {type(error).__name__}")
        print(error)
        fault = True

    finally:
        close(conn, cursor)

    return Users, fault


def load_users():

    Users, fault = None, False

    conn, cursor = None, None

    try:

        conn, cursor = get_connection()

        cursor.execute("""
select user_id, name from users
""")
        Users = cursor.fetchall()

    except sqlite3.Error as error:
        if conn:
            conn.rollback()
        print(f"Selection failed: {type(error).__name__}")
        print(error)
        fault = True
    finally:
        close(conn, cursor)

    return Users, fault


def load_books():

    books, fault = None, False

    conn, cursor = None, None

    try:

        conn, cursor = get_connection()

        cursor.execute("""
select book_id, book_name, year, author, borrow_time, borrowed from books
""")

        books = cursor.fetchall()

    except sqlite3.Error as error:
        if conn:
            conn.rollback()
        print(f"Selection failed: {type(error).__name__}")
        print(error)
        fault = True
    finally:
        close(conn, cursor)

    return books, fault


def show_user_borrow_history(user, user_id):

    users, fault = None, False
    try:
        conn, cursor = None, None
        conn, cursor = get_connection()

        cursor.execute("""
select * from borrow_history where name = ? and user_id = ?
""", (user.lower(), user_id))

        users = cursor.fetchall()

    except sqlite3.Error as error:
        print(
            f"Selecting user borrow history failed. Error type: {type(error).__name__}")
        print(error)
        fault = True

    finally:
        close(conn, cursor)

    return users, fault


def delete(table):
    conn, cursor, fault = None, None, None
    try:

        conn, cursor = get_connection()

        if table.lower() == "books":

            cursor.execute("""
select * from books
""")
            fault = cursor.fetchone()
            if fault:
                cursor.execute("""
delete from books
""")
                conn.commit()
                print("Books deleted!")
            else:
                print("Books is already empty.")

        elif table.lower() == "borrow_history":

            cursor.execute("""
select * from borrow_history
""")
            fault = cursor.fetchone()
            if fault:
                cursor.execute("""
delete from borrow_history
""")
                conn.commit()
                print("Borrow_history deleted!")
            else:
                print("Borrow_history is already empty.")

        elif table.lower() == "users":

            cursor.execute("""
select * from users
""")
            fault = cursor.fetchone()
            if fault:
                cursor.execute("""
delete from users
""")
                conn.commit()
                print("Users deleted!")
            else:
                print("Users is already empty.")
        else:
            print("Invalid input. Try again.")

    except sqlite3.Error as error:
        if conn:
            conn.rollback()
        print(f"Deletion failed: {type(error).__name__}")
        print(error)
    finally:
        close(conn, cursor)


def reset():
    fault, conn, cursor = False, None, None
    try:
        conn, cursor = get_connection()

        cursor.execute("""
delete from borrow_history
""")
        conn.commit()
        
        cursor.execute("""
delete from users""")
        
        conn.commit()
        
        cursor.execute("""
select book_id, book_name from books""")
        
        books = cursor.fetchall()
        if books:
            for book in books:
                cursor.execute("""
update books set borrowed = ? where book_name = ? and book_id = ?
""", ("no", book[1], book[0]))
                conn.commit()
        else:
            print("There are no books in library.")

    except sqlite3.Error as error:
        if conn:
            conn.rollback()
        print(f"An error occurred: {type(error).__name__}")
        print(error)
        fault = True

    finally:
        close(conn, cursor)
    return fault


def get_id(book_name):
    conn, cursor, user_id = None, None, None
    try:
        conn, cursor = get_connection()

        cursor.execute("""
select user_id from borrow_history where book_borrowed = ? and returned = ?
""", (book_name, "no"))
        
        user_id = cursor.fetchone()

    except sqlite3.Error as error:
        print(f"Selection error: {type(error).__name__}")
        print(error)
    finally:
        close(conn, cursor)
    return user_id


def get_datetime(book_name):
    conn, cursor, book = None, None, None
    try:
        conn, cursor = get_connection()

        cursor.execute("""
select datetime_borrowed from borrow_history where book_borrowed = ? and returned = ?
""", (book_name.lower(), "no"))
        book = cursor.fetchall()
        #print(book)

    except sqlite3.Error as error:
        if conn:
            conn.rollback()
        print(f"Selection error: {type(error).__name__}")
        print(error)
    finally:
        close(conn, cursor)
    return book
