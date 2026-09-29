import asyncio
import os
from aiogram import Bot, Dispatcher, F, Router
from aiogram.filters import Command
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
)
from dotenv import load_dotenv

load_dotenv()
token = os.getenv('token')

bot = Bot(token=token) if token else None
dp = Dispatcher()
router = Router()

# Негизги клавиатура (Reply Keyboard)
main_menu_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Меню"), KeyboardButton(text="О нас")],
        [KeyboardButton(text="Контакты"), KeyboardButton(text="Корзина")],
    ],
    resize_keyboard=True
)

# Инлайн клавиатура (Меню басылганда чыгуучу)
inline_menu_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🍲 Тамактар", callback_data="foods")],
        [InlineKeyboardButton(text="🧃 Суусундуктар", callback_data="drinks")],
        [InlineKeyboardButton(text="🍰 Десерттер", callback_data="desserts")],
    ]
)


# 1. /start буйругу
@router.message(Command('start'))
async def start_restaurant(message: Message):
    await message.answer(
        'Кош келдиңиз биздин ресторанга😊',
        reply_markup=main_menu_kb
    )



@router.message(F.text == 'Меню')
async def show_menu(message: Message):
    await message.answer(
        'Выберите интересующее направление:',
        reply_markup=inline_menu_kb
    )



@router.message(F.text == 'О нас')
async def show_about(message: Message):
    about_text = (
        'Подробности ресторана: бизде восточный кухня\n'
        'Адрес: Жалал-Абад г: Калмаматов Рахманали №12'
    )
    await message.answer(about_text)


@router.message(F.text == 'Контакты')
async def show_contacts(message: Message):
    await message.answer('Связаться с нами: +996 770 743 061 ')



@router.message(F.text == 'Корзина')
async def show_cart(message: Message):
    await message.answer('Сиздин корзинаңыз.')


# Инлайн баскычтар үчүн callback иштетүү
@router.callback_query(F.data == 'foods')
async def cb_foods(call: CallbackQuery):
    await call.message.answer('🍲 Тамактар бөлүмү тандалды.')
    await call.answer()


@router.callback_query(F.data == 'drinks')
async def cb_drinks(call: CallbackQuery):
    await call.message.answer('🧃 Суусундуктар бөлүмү тандалды.')
    await call.answer()


@router.callback_query(F.data == 'desserts')
async def cb_desserts(call: CallbackQuery):
    await call.message.answer('🍰 Десерттер бөлүмү тандалды.')
    await call.answer()


async def main():
    if not token or token.startswith("YOUR_"):
        print("⚠️ Эскертүү: .env файлына BotFather'ден алган токениңизди жазыңыз!")
    print("ДЗ 3 (Ресторан) боту иштеп жатат...")
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
