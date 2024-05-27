from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def startKB(owner, otzivi, faq):
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton(text="💵 Расчет стоимости заказа", callback_data="raschet"))
    kb.add(InlineKeyboardButton(text="📦 Оформить заказ", url=f"https://t.me/{owner}", callback_data="start"))
    kb.add(InlineKeyboardButton(text="🗓️ Сроки доставки", callback_data="sroki"))
    kb.add(InlineKeyboardButton(text="📄 Отзывы о нас", url=f"https://t.me/{otzivi}", callback_data="start"))
    kb.add(InlineKeyboardButton(text="❓ Вопросы и ответы", url=f"https://t.me/{faq}", callback_data="start"))
    kb.add(InlineKeyboardButton(text="☎️ Связаться с оператором", url=f"https://t.me/{owner}", callback_data="start"))
    kb.add(InlineKeyboardButton(text="🤔 Где брать товары?", callback_data="gde_brat"))

    return kb