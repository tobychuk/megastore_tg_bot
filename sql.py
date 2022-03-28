import mysql.connector
from megastore_sql.mouse_sql import MouseSQL
from megastore_sql.keyboard_sql import KeyboardSQL
from megastore_sql.headphones_sql import HeadphonesSQL
from megastore_sql.user_cart_sql import CartSQL

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Ggmasterkg123",
    db="megastore",
    autocommit = True)
cursor = db.cursor()

mouse_manager = MouseSQL(cursor=cursor)
keyboard_manager = KeyboardSQL(cursor=cursor)
headphones_manager = HeadphonesSQL(cursor=cursor)
cart_manager = CartSQL(cursor=cursor)


def update_mouses_data(data):
    mouse_manager.update_mouse_table(data=data)
def update_keyboards_data(data):
    keyboard_manager.update_keyboard_table(data=data)
def update_headphones_data(data):
    headphones_manager.update_headphones_table(data=data)

