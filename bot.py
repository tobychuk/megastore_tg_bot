from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, callback_query
from config import TOKEN
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext


from time import sleep
import os, random


import sql

bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


class Form(StatesGroup):
    mouse_name_all = State()
    total_mouse = State()
    keyboard_name_all = State()
    total_keyboard = State()
    headphones_name_all = State()
    total_headphones = State()


    answer_product_type = State()
    answer_mouse_id = State()
    answer_keyboard_id = State()
    answer_headphones_id = State()


    answer_cart_delete = State()
    answer_cart_id = State()





@dp.message_handler(commands="start")
async def welcome(message: types.Message):
    sti_name = random.choice(os.listdir("stickers"))
    sti = open(f"stickers/{sti_name}","rb")
    text = """Вас приветствует бот магазина Megastore!
У нас вы можете увидеть ассортимент товара и его наличие в разных точках магазинов!

Выберите действие: """
    markup = InlineKeyboardMarkup(row_width=2)
    products_btn = InlineKeyboardButton(text="Товары", callback_data="products")
    profile_btn = InlineKeyboardButton(text="Мой профиль", callback_data="profile")
    markup.add(profile_btn,products_btn)
    await bot.send_sticker(chat_id=message.chat.id, sticker=sti)
    await message.answer(text=text, reply_markup=markup)


@dp.callback_query_handler(lambda c: c.data == "profile")
async def show_profile_buttons(call: types.callback_query):
    message = call.message
    text = """Вы находитесь в собственном профиле.

Выберите действие:"""
    markup = InlineKeyboardMarkup(row_width=2)
    cart_btn = InlineKeyboardButton(text="Моя корзина", callback_data="cart")
    back_btn  = InlineKeyboardButton(text="Назад",callback_data="back_menu")
    cart_add_btn = InlineKeyboardButton(text="Добавить товар в корзину", callback_data="add_cart")
    markup.add(cart_btn,cart_add_btn,back_btn)
    await bot.edit_message_text(message_id=message.message_id, chat_id=message.chat.id,text=text, reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data =="add_cart")
async def add_user_cart_step1(call: types.callback_query):
    message = call.message
    await bot.edit_message_text(chat_id=message.chat.id,
                                message_id=message.message_id,
                                text="Введите тип товара, который вы хотите добавить в корзину(Мышь, Клавиатура, Гарнитура): ")
    await Form.answer_product_type.set()

@dp.message_handler(state=Form.answer_product_type)
async def add_user_cart_step2(message = types.Message, state = FSMContext):
    if message.text.lower() == "мышь":
        await message.answer(text="""
Выбран тип мышь!
Отправьте id товара: 
(если хотите выйти в меню введите 'Меню')""")
        await Form.answer_mouse_id.set()
    elif message.text.lower() == "клавиатура":
            await message.answer(text="""
Выбран тип клавиатура!
Отправьте id товара: 
(если хотите выйти в меню введите 'Меню')""")
            await Form.answer_keyboard_id.set()
    elif message.text.lower() == "гарнитура":
        await message.answer(text="""
Выбран тип гарнитура!
Отправьте id товара: 
(если хотите выйти в меню введите 'Меню')""")
        await Form.answer_headphones_id.set()
    else:
        await message.reply("""Такого типа не существует.
Виды товаров: Мышь, Клавиатура, Гарнитура""")


@dp.message_handler(state=Form.answer_mouse_id)
async def add_mouse(message: types.Message, state = FSMContext):
        try:
            if message.text.lower() == "меню":
                await state.finish()
                await welcome(message)
            else:
                product_data = sql.mouse_manager.found_mouse_with_id(message.text)
                data = {
                "username":message.chat.username,
                "first_name":message.chat.first_name,
                "product_name":product_data[1],
                "product_price":product_data[2]
                }
                sql.cart_manager.add_users_products(data)
                await message.answer(text="Товар добавлен")
                await message.answer(text="""
Выбран тип мышь!
Отправьте id товара: 
(если хотите выйти в меню введите 'Меню')""")
        except:
            await message.reply("Данного id не существует.")



@dp.message_handler(state=Form.answer_keyboard_id)
async def add_keyboard(message: types.Message, state = FSMContext):
        try:
            if message.text.lower() == "меню":
                await state.finish()
                await welcome(message)
            else:
                product_data = sql.keyboard_manager.found_keyboard_with_id(message.text)
                data = {
                "username":message.chat.username,
                "first_name":message.chat.first_name,
                "product_name":product_data[1],
                "product_price":product_data[2]
                }
                sql.cart_manager.add_users_products(data)
                await message.answer(text="Товар добавлен")
                await message.answer(text="""
Выбран тип клавиатура!
Отправьте id товара: 
(если хотите выйти в меню введите 'Меню')""")
        except:
            await message.reply("Данного id не существует.")



@dp.message_handler(state=Form.answer_headphones_id)
async def add_headphones(message: types.Message, state = FSMContext):
        try:
            if message.text.lower() == "меню":
                await state.finish()
                await welcome(message)
            else:
                product_data = sql.headphones_manager.found_headphones_with_id(message.text)
                data = {
                "username":message.chat.username,
                "first_name":message.chat.first_name,
                "product_name":product_data[1],
                "product_price":product_data[2]
                }
                sql.cart_manager.add_users_products(data)
                await message.answer(text="Товар добавлен")
                await message.answer(text="""
Выбран тип гарнитура!
Отправьте id товара: 
(если хотите выйти в меню введите 'Меню')""")

        except:
            await message.reply("Данного id не существует.")



@dp.callback_query_handler(lambda c: c.data == "cart")
async def show_user_cart(call: types.callback_query):
    message = call.message
    user_products = sql.cart_manager.get_users_products(message.chat.username)
    await message.answer(f"Корзина {message.chat.username}: ")
    for product in user_products:
        await message.answer(f"""
Номер: {product[0]}
Название: {product[1]}
Цена: {product[3]}""")
    await message.answer("Вы желаете удалить что-то из корзины(Да/Нет) ?")
    await Form.answer_cart_delete.set()


@dp.message_handler(state=Form.answer_cart_delete)
async def delete_from_cart_step1(message: types.Message, state=FSMContext):
    if message.text.lower() == "да":
        await message.answer("Введите номер товара в корзине, который вы хотите удалить:")
        await Form.answer_cart_id.set()
    elif message.text.lower() == "нет":
        await state.finish()
        await welcome(message)
    else:
        await message.answer("Вы желаете удалить что-то из корзины(Да/Нет) ?")


@dp.message_handler(state=Form.answer_cart_id)
async def delete_from_cart_step2(message: types.Message, state=FSMContext):
    sql.cart_manager.del_users_products(message.text)
    await message.reply("Успешно удалено.")
    await Form.answer_cart_delete.set()
    await delete_from_cart_step1(message)



@dp.callback_query_handler(lambda c: c.data == "products")
async def show_products_type(call: types.callback_query):
    message = call.message
    markup = InlineKeyboardMarkup(width=3)
    mouse_btn = InlineKeyboardButton("Мыши:", callback_data="mouses")
    kboard_btn = InlineKeyboardButton("Клавиатуры:", callback_data="kboards")
    hphones_btn = InlineKeyboardButton("Гарнитуры:", callback_data="hphones")
    back_btn = InlineKeyboardButton("Назад", callback_data="back_menu")
    markup.add(mouse_btn, kboard_btn, hphones_btn, back_btn)
    await bot.edit_message_text(text="Выберите тип товаров:",
                                chat_id=message.chat.id,
                                message_id=message.message_id,
                                reply_markup=markup)


@dp.callback_query_handler(lambda c: c.data == "mouses")
async def show_mouses_search_step1(call: types.callback_query):
    message = call.message
    await bot.edit_message_text(text="""Введите название мыши:
Если хотите вывести все мыши отправьте '*' """, chat_id=message.chat.id, message_id=message.message_id)
    await Form.mouse_name_all.set()


@dp.message_handler(state=Form.mouse_name_all)
async def show_mouses_search_step2(message: types.Message, state=FSMContext):
    if message.text == "*":
        mouses = sql.mouse_manager.found_mouse_with_name("")
        for mouse in mouses:
            await message.answer(text=f"{mouse[0]}) {mouse[1]}")
            sleep(0.1)
    else:
        mouses = sql.mouse_manager.found_mouse_with_name(message.text)
        for mouse in mouses:
            await message.answer(text=f"{mouse[0]}) {mouse[1]}")
            sleep(0.1)
    await message.answer(text="""Введите id модели, чтобы узнать подробную информацию:
(если хотите выйти в меню введите 'Меню')""")
    await Form.total_mouse.set()


@dp.message_handler(state=Form.total_mouse)
async def show_info_mouse(message: types.Message, state=FSMContext):
    try:
        if message.text == "Меню":
            await state.finish()
            await welcome(message)
        else:
            mouse = sql.mouse_manager.found_mouse_with_id(message.text)
            await message.reply(
            text=f"""
1)Название: {mouse[1]}

2)Цена: {mouse[2]}

3)Описание: {mouse[3]}

4)Наличие: {mouse[4]}""")
            await message.answer(text="""Введите id модели, чтобы узнать подробную информацию:
(если хотите выйти в меню введите 'Меню')""")
    except:
        await message.answer("Данного id не существует!")
        await message.answer(text="""Введите id модели, чтобы узнать подробную информацию:
(если хотите выйти в меню введите 'Меню')""")


@dp.callback_query_handler(lambda c: c.data == "kboards")
async def show_keyboards_search_step1(call: types.callback_query):
    message = call.message
    await bot.edit_message_text(text="""Введите название клавиатуры:
Если хотите вывести все клавиатуры отправьте '*' """, chat_id=message.chat.id, message_id=message.message_id)
    await Form.keyboard_name_all.set()


@dp.message_handler(state=Form.keyboard_name_all)
async def show_keyboards_search_step2(message: types.Message, state=FSMContext):
    if message.text == "*":
        keyboards = sql.keyboard_manager.found_keyboard_with_name("")
        for keyboard in keyboards:
            await message.answer(text=f"{keyboard[0]}) {keyboard[1]}")
            sleep(0.1)
    else:
        keyboards = sql.keyboard_manager.found_keyboard_with_name(message.text)
        for keyboard in keyboards:
            await message.answer(text=f"{keyboard[0]}) {keyboard[1]}")
            sleep(0.1)
    await message.answer(text="""Введите id модели, чтобы узнать подробную информацию:
(если хотите выйти в меню введите 'Меню')""")
    await Form.total_keyboard.set()


@dp.message_handler(state=Form.total_keyboard)
async def show_info_keyboard(message: types.Message, state=FSMContext):
    try:
        if message.text.lower() == "меню":
            await state.finish()
            await welcome(message)
        else:
            keyboard = sql.keyboard_manager.found_keyboard_with_id(message.text)
            await message.reply(
            text=f"""
1)Название: {keyboard[1]}

2)Цена: {keyboard[2]}

3)Описание: {keyboard[3]}

4)Наличие: {keyboard[4]}"""
        )
            await message.answer(text="""Введите id модели, чтобы узнать подробную информацию:
(если хотите выйти в меню введите 'Меню')""")
    except:
        await message.answer("Данного id не существует!")
        await message.answer(text="""Введите id модели, чтобы узнать подробную информацию:
(если хотите выйти в меню введите 'Меню')""")



@dp.callback_query_handler(lambda c: c.data == "hphones")
async def show_headphones_search_step1(call: types.callback_query):
    message = call.message
    await bot.edit_message_text(text="""Введите название наушников:
Если хотите вывести все наушники отправьте '*' """, chat_id=message.chat.id, message_id=message.message_id)
    await Form.headphones_name_all.set()


@dp.message_handler(state=Form.headphones_name_all)
async def show_headphones_search_step2(message: types.Message, state=FSMContext):
    if message.text == "*":
        headphones = sql.headphones_manager.found_headphones_with_name("")
        for headphone in headphones:
            await message.answer(text=f"{headphone[0]}) {headphone[1]}")
            sleep(0.1)
    else:
        headphones = sql.headphones_manager.found_headphones_with_name(message.text)
        for headphone in headphones:
            await message.answer(text=f"{headphone[0]}) {headphone[1]}")
            sleep(0.1)
    await message.answer(text="""Введите id модели, чтобы узнать подробную информацию:
(если хотите выйти в меню введите 'Меню')""")
    await Form.total_headphones.set()


@dp.message_handler(state=Form.total_headphones)
async def show_info_headphones(message: types.Message, state=FSMContext):
    try:
        if message.text.lower() == "меню":
            await state.finish()
            await welcome(message)
        else:
            headphones = sql.headphones_manager.found_headphones_with_id(message.text)
            await message.reply(
            text=f"""
1)Название: {headphones[1]}

2)Цена: {headphones[2]} 

3)Описание: {headphones[3]}

4)Наличие: {headphones[4]}"""
        )
            await message.answer(text="""Введите id модели, чтобы узнать подробную информацию:
(если хотите выйти в меню введите 'Меню')""")

    except:
        await message.answer("Данного id не существует!")
        await message.answer(text="""Введите id модели, чтобы узнать подробную информацию:
(если хотите выйти в меню введите 'Меню')""")



@dp.callback_query_handler(lambda c: c.data == "back_menu")
async def back(call: types.callback_query):
    await welcome(call.message)



executor.start_polling(dp)