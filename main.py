import aiogram
import aiosqlite

from conf import TOKEN
from keyboards import *
from aiogram.dispatcher import FSMContext
from aiogram import Dispatcher, Bot, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup

storage = MemoryStorage()

admins = [6142402831, 1749015885]

bot: Bot = Bot(token=TOKEN)
dp: Dispatcher = Dispatcher(bot, storage=storage)

class raschetFSM(StatesGroup):
    price = State()
    tovar = State()
    dostavka = State()

class adminFSM(StatesGroup):
    key = State()
    value = State()
    agree = State()

@dp.message_handler(commands="start")
async def startCMD(message: types.Message):
    db = await aiosqlite.connect("data.db")
    cursor = await db.execute('SELECT value FROM data WHERE key="ссылка_на_канал"')
    link = await cursor.fetchone()
    link = link[0]

    cursor = await db.execute('SELECT value FROM data WHERE key="ссылка_на_владельца"')
    owner = await cursor.fetchone()
    owner = owner[0]

    cursor = await db.execute('SELECT value FROM data WHERE key="ссылка_на_отзывы"')
    otzivi = await cursor.fetchone()
    otzivi = otzivi[0]

    cursor = await db.execute('SELECT value FROM data WHERE key="ссылка_на_вопросы_и_ответы"')
    faq = await cursor.fetchone()
    faq = faq[0]

    await message.answer(f"""Привет! Вы запустили бота Mz_Poizon.

Наш канал 👉🏻 https://t.me/{link}""")
    await message.answer("Выберите нужное действие:", reply_markup=startKB(owner=owner, otzivi=otzivi, faq=faq))

    await db.close()

@dp.callback_query_handler(text="gde_brat")
async def gdeBratCMD(call: types.CallbackQuery):
    # await call.message.delete()
    db = await aiosqlite.connect("data.db")
    cursor = await db.execute('SELECT value FROM data WHERE key="ссылка_на_канал"')
    link = await cursor.fetchone()
    link = link[0]

    txt = rf"""Ссылка на скачивание приложения для Android: https://clck.ru/3A4cgR
Нижняя синяя кнопка

Ссылка для скачивания приложения для IOS: https://clck.ru/3A4ckf

Руководства по пользованию приложением есть в нашем канале: https://t.me/{link}

С каталогом также можно ознакомиться на poizon.com"""
    
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("В главное меню", callback_data="main_menu"))
    await call.message.edit_text(txt, reply_markup=kb, disable_web_page_preview=True)
    await db.close()

@dp.callback_query_handler(text="main_menu")
async def mainMenuCMD(call: types.CallbackQuery):
    db = await aiosqlite.connect("data.db")
    cursor = await db.execute('SELECT value FROM data WHERE key="ссылка_на_канал"')
    link = await cursor.fetchone()
    link = link[0]

    cursor = await db.execute('SELECT value FROM data WHERE key="ссылка_на_владельца"')
    owner = await cursor.fetchone()
    owner = owner[0]

    cursor = await db.execute('SELECT value FROM data WHERE key="ссылка_на_отзывы"')
    otzivi = await cursor.fetchone()
    otzivi = otzivi[0]

    cursor = await db.execute('SELECT value FROM data WHERE key="ссылка_на_вопросы_и_ответы"')
    faq = await cursor.fetchone()
    faq = faq[0]

    await call.message.edit_text("Выберите нужное действие:", reply_markup=startKB(owner=owner, faq=faq, otzivi=otzivi))

    await db.close()

@dp.callback_query_handler(text="sroki")
async def srokiCMD(call: types.CallbackQuery):
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("В главное меню", callback_data="main_menu"))
    await call.message.edit_text("""Доставка до нашего склада в Китае занимает от 2 до 6 дней, затем доставка до Московского склада 12-25 дней, в среднем большинство партий идут 14 дней до Москвы.
Далее если необходима пересылка в другой город мы передаем в СДЭК на следующий день.""", reply_markup=kb)

@dp.callback_query_handler(text='raschet')
async def raschetCMD(call: types.CallbackQuery):
    photo = open("image.jpg", "rb").read()
    cap = """Для расчета всегда надо использовать перечеркнутую цену, потому что на нашем аккаунте уже нет скидок нового пользователя"""
    await bot.send_photo(call.from_user.id, photo=photo, caption=cap)
    await call.message.delete()

    db = await aiosqlite.connect("data.db")
    cursor = await db.execute('SELECT value FROM data WHERE key="ссылка_на_владельца"')
    owner = await cursor.fetchone()
    owner = owner[0]
    await db.close()

    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton(text="Где взять цену", callback_data="gde_tsena"))
    kb.add(types.InlineKeyboardButton(text="🔔 Связаться с оператором", url=f"https://t.me/{owner}", callback_data="operator"))
    

    txt = """Введите цену в юанях

❗️<i>Укажите целое число, без дробей, пробелов, букв и знаков валюты. Пример: 1250</i>"""

    await call.message.answer(txt, reply_markup=kb, parse_mode=types.ParseMode.HTML)
    await raschetFSM.price.set()

@dp.message_handler(content_types="any", state=raschetFSM.price)
async def raschetFSMCMD(message: types.Message, state: FSMContext):
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton(text='🚫 Отмена', callback_data="otmena"))

    if not (message.text):
        await message.answer("Сообщение должно быть текстовым!", reply_markup=kb)
        return
    
    if not (message.text.isnumeric()):
        await message.answer("Сообщение должно состоять только из цифр!", reply_markup=kb)
        return
    
    db = await aiosqlite.connect('data.db')
    cursor = await db.execute('SELECT value FROM data WHERE key="курс_юаня"')
    uan = await cursor.fetchone()

    async with state.proxy() as data:
        data["price"] = int(int(message.text) * float(uan[0]))
        data["poizon"] = int(int(message.text) * float(uan[0]))

    

    kb1 = types.InlineKeyboardMarkup()
    kb1.add(types.InlineKeyboardButton(text="👟 Кроссовки", callback_data="v:kross"))
    kb1.add(types.InlineKeyboardButton(text="🥾 Кро-ки зимние, OldOrder | Osiris", callback_data="v:winterkros"))
    kb1.add(types.InlineKeyboardButton(text="🥷 Худи, Толчтовки, Спорт. штаны", callback_data="v:hood"))
    kb1.add(types.InlineKeyboardButton(text="👕 Футболки, Шорты, Аксессуары", callback_data="v:futbolk"))
    kb1.add(types.InlineKeyboardButton(text="🧥 Пуховики", callback_data="v:puhoviki"))
    kb1.add(types.InlineKeyboardButton(text="👜 Сумки, Рюкзаки небольшие", callback_data="v:summal"))
    kb1.add(types.InlineKeyboardButton(text="🎒 Сумки, Рюкзаки большие", callback_data="v:sumbol"))
    kb1.add(types.InlineKeyboardButton(text='🚫 Отмена', callback_data="otmena"))
    await message.answer("Выберите товар, чтобы рассчитать массу:", reply_markup=kb1)
    await raschetFSM.next()

@dp.callback_query_handler(text_startswith="v:", state=raschetFSM.tovar)
async def viborCMD(call: types.CallbackQuery, state: FSMContext):

    data = call.data.split(":")[1]
    db = await aiosqlite.connect("data.db")
    cursor = await db.execute(f"SELECT value FROM data WHERE key='{data}'")
    value = await cursor.fetchone()
    value = value[0]

    cursor = await db.execute("SELECT value FROM data WHERE key='цена_за_килограмм'")
    price_per_kg = await cursor.fetchone()
    price_per_kg = price_per_kg[0]
    # print(int(float(value) * int(price_per_kg)))
    async with state.proxy() as data:
        data['price'] += int(float(value) * int(price_per_kg))
        data['msk'] = int(float(value) * int(price_per_kg))

    cursor = await db.execute("SELECT value FROM data WHERE key='цена_СДЭК_Москва'")
    sdek = await cursor.fetchone()
    sdek = int(sdek[0])
    cursor = await db.execute("SELECT value FROM data WHERE key='цена_центральный_регион'")
    center = await cursor.fetchone()
    center = int(center[0])

    cursor = await db.execute("SELECT value FROM data WHERE key='цена_другие_регионы'")
    dr = await cursor.fetchone()
    dr = int(dr[0])

    cursor = await db.execute("SELECT value FROM data WHERE key='цена_самовывоз'")
    sam = await cursor.fetchone()
    sam = int(sam[0])

    cursor = await db.execute("SELECT value FROM data WHERE key='город_самовывоза'")
    city = await cursor.fetchone()


    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton(text=f"СДЭК Москва {sdek}р", callback_data='dost:sdek'))
    kb.add(types.InlineKeyboardButton(text=f"Центральный регион {center}", callback_data='dost:center'))
    kb.add(types.InlineKeyboardButton(text=f"Другие регионы {dr}+", callback_data='dost:other'))
    kb.add(types.InlineKeyboardButton(text=f"Самовывоз", callback_data='dost:sam'))
    kb.add(types.InlineKeyboardButton(text='🚫 Отмена', callback_data="otmena"))

    await call.message.edit_text(f"""Выберите вариант доставки
(точный расчет будет при оформлении заказа)
Самовывоз - бесплатно ({city[0]})""", reply_markup=kb)
    await db.close()
    await raschetFSM.next()


@dp.callback_query_handler(text_startswith="dost:", state=raschetFSM.dostavka)
async def dostCMD(call: types.CallbackQuery, state: FSMContext):
    data = call.data.split(":")[1]
    db = await aiosqlite.connect("data.db")
    if data == "sdek":
        cursor = await db.execute("SELECT value FROM data WHERE key='цена_СДЭК_Москва'")
    elif data == 'center':
        cursor = await db.execute("SELECT value FROM data WHERE key='цена_центральный_регион'")
    elif data == 'other':
        cursor = await db.execute("SELECT value FROM data WHERE key='цена_другие_регионы'")
    elif data == 'sam':
        cursor = await db.execute("SELECT value FROM data WHERE key='цена_самовывоз'")
    pr = await cursor.fetchone()
    pr = int(pr[0])


    async with state.proxy() as data:
        data["price"] += pr
        price = data['price']
        poizon = int(data["poizon"])
        msk = data['msk']


    await state.finish()

    cursor = await db.execute("SELECT value FROM data WHERE key='доставка_по_китаю'")
    china = await cursor.fetchone()
    china = int(china[0])


    cursor = await db.execute("SELECT value FROM data WHERE key='процент_страховки'")
    strah = await cursor.fetchone()
    strah = int(strah[0])

    cursor = await db.execute("SELECT value FROM data WHERE key='комиссия_сервиса'")
    kom = await cursor.fetchone()
    kom = int(kom[0])

    cursor = await db.execute("SELECT value FROM data WHERE key='процент_предоплаты'")
    pred = await cursor.fetchone()
    pred = int(pred[0]) / 100



    summa = poizon + china + msk + (poizon // 100 * strah) + kom + pr 


    cursor = await db.execute("SELECT value FROM data WHERE key='ссылка_на_владельца'")
    owner = await cursor.fetchone()
    owner = owner[0]
    
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton(text="Оформить заказ", callback_data="end:zakaz"))
    kb.add(types.InlineKeyboardButton(text="Рассчитать стоимость товара", callback_data='end:raschet'))
    kb.add(types.InlineKeyboardButton(text='В главное меню', callback_data="main_menu"))
    kb.add(types.InlineKeyboardButton(text="Связаться с оператором", url=f'https://t.me/{owner}'))

    await call.message.edit_text(f"""Ваш расчет заказа:
- Цена товара на Poizon {poizon} руб.
- Доставка по Китаю {china} руб.
- Доставка до склада в Москве {msk} руб.
- Страховка {strah}% - {poizon // 100 * strah} руб.
- Комиссия сервиса {kom} руб.
- Доставка по РФ {pr} руб.

Общая стоимость заказа: {summa} руб.
Предоплата: {int(summa * pred)} руб.

Комиссию можно снизить до {kom - 300} рублей, подробности уточняйте у операторов :)
Обращаем Ваше внимание: расчет актуален в течение часа, т.к. на Poizon цены часто меняются""", reply_markup=kb)


@dp.callback_query_handler(text_startswith='end:')
async def endCallCMD(call: types.CallbackQuery):
    db = await aiosqlite.connect('data.db')
    data = call.data.split(':')[1]
    if data == "raschet":
        await raschetCMD(call=call)
    elif data ==  "zakaz":
        cursor = await db.execute("SELECT value FROM data WHERE key='ссылка_на_владельца'")
        owner = await cursor.fetchone()
        owner = owner[0]
        kb = types.InlineKeyboardMarkup()
        kb.add(types.InlineKeyboardButton(text="Перейти к оформлению", url=f'https://t.me/{owner}'))
        kb.add(types.InlineKeyboardButton(text="Главное меню", callback_data="main_menu"))
        await call.message.answer("Пожалуйста нажмите кнопку ниже (\"Перейти к оформлению\"), затем кнопку «Начать», чтобы запустить бота с оператором для оформления заказа.", reply_markup=kb)
    

    

@dp.callback_query_handler(text="otmena", state=raschetFSM)
async def otmenaRaschetFSM(call: types.CallbackQuery, state: FSMContext):


    await state.finish()
    db = await aiosqlite.connect("data.db")
    cursor = await db.execute('SELECT value FROM data WHERE key="ссылка_на_канал"')
    link = await cursor.fetchone()
    link = link[0]

    cursor = await db.execute('SELECT value FROM data WHERE key="ссылка_на_владельца"')
    owner = await cursor.fetchone()
    owner = owner[0]

    cursor = await db.execute('SELECT value FROM data WHERE key="ссылка_на_отзывы"')
    otzivi = await cursor.fetchone()
    otzivi = otzivi[0]

    cursor = await db.execute('SELECT value FROM data WHERE key="ссылка_на_вопросы_и_ответы"')
    faq = await cursor.fetchone()
    faq = faq[0]

    await call.message.answer("Выберите нужное действие:", reply_markup=startKB(owner=owner, otzivi=otzivi, faq=faq))

    await db.close()


@dp.callback_query_handler(text="gde_tsena", state=raschetFSM)
async def gdeTsenaCMD(call: types.CallbackQuery):
    

    db = await aiosqlite.connect("data.db")
    cursor = await db.execute('SELECT value FROM data WHERE key="ссылка_на_канал"')
    link = await cursor.fetchone()
    link = link[0]

    txt = rf"""Ссылка на скачивание приложения для Android: https://clck.ru/3A4cgR
Нижняя синяя кнопка

Ссылка для скачивания приложения для IOS: https://clck.ru/3A4ckf

Руководства по пользованию приложением есть в нашем канале: https://t.me/{link}

С каталогом также можно ознакомиться на poizon.com"""
    
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton(text="Назад", callback_data="back"))
    
    await call.message.answer(txt, disable_web_page_preview=True, reply_markup=kb)
    await call.message.delete()

@dp.callback_query_handler(text="back", state=raschetFSM)
async def backCMD(call: types.CallbackQuery):
    db = await aiosqlite.connect("data.db")
    cursor = await db.execute('SELECT value FROM data WHERE key="ссылка_на_владельца"')
    owner = await cursor.fetchone()
    owner = owner[0]
    await db.close()

    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton(text="Где взять цену", callback_data="gde_tsena"))
    kb.add(types.InlineKeyboardButton(text="🔔 Связаться с оператором", url=f"https://t.me/{owner}", callback_data="operator"))
    

    txt = """Введите цену в юанях

❗️<i>Укажите целое число, без дробей, пробелов, букв и знаков валюты. Пример: 1250</i>"""

    await call.message.answer(txt, reply_markup=kb, parse_mode=types.ParseMode.HTML)
    await db.close()
    await call.message.delete()

@dp.message_handler(commands=['admin'])
async def adminCMD(message: types.Message):
    if not message.from_user.id in admins:
        return
    db = await aiosqlite.connect("data.db")

    cursor = await db.execute("SELECT key FROM data")
    alldata = await cursor.fetchall()

    kb = types.ReplyKeyboardMarkup()

    for i in alldata:
        kb.add(types.KeyboardButton(i[0]))
    

    await message.answer("Выберите значение:", reply_markup=kb)
    await adminFSM.key.set()

    await db.close()

@dp.message_handler(content_types=['text'], state=adminFSM.key)
async def adminKeyCMD(message: types.Message, state: FSMContext):
    db = await aiosqlite.connect("data.db")

    cursor = await db.execute("SELECT key FROM data")
    alldata = await cursor.fetchall()
    alldata = [i[0] for i in alldata]

    if not message.text in alldata:
        await message.answer("Такого значения нет в списке", reply_markup=types.ReplyKeyboardRemove())
        await state.finish()
        return
    
    async with state.proxy() as data:
        data['key'] = message.text

    await db.close()
    await message.answer(f"Изменить значение {message.text} на ...", reply_markup=types.ReplyKeyboardRemove())
    await adminFSM.next()


@dp.message_handler(content_types='text', state=adminFSM.value)
async def adminValueCMD(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['value'] = message.text
        key = data['key']

    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton(text="Да", callback_data="admin:yes"))
    kb.insert(types.InlineKeyboardButton(text="Нет", callback_data="admin:no"))
    await message.answer(f"Вы действительно хотите изменить значение {key} на {message.text}", reply_markup=kb)
    await adminFSM.next()

@dp.callback_query_handler(text_startswith="admin:", state=adminFSM.agree)
async def agreeAdminFSM(call: types.CallbackQuery, state: FSMContext):
    data = call.data.split(':')[1]
    if data == 'yes':
        db = await aiosqlite.connect("data.db")
        async with state.proxy() as data:
            value = data['value']
            key = data['key']

        await db.execute(f'UPDATE data SET value="{value}" WHERE key="{key}"')
        await db.commit()
        await db.close()
        await call.message.answer(f"Значение \"{key}\" успешно изменено")
    else:
        await call.message.answer("Изменение отменено...")
    await state.finish()


if __name__ == "__main__":
    aiogram.executor.start_polling(dispatcher=dp, skip_updates=True)     