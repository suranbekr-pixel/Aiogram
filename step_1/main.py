import asyncio
import datetime
import os
from aiogram import Bot, Dispatcher, F, Router
from aiogram.filters import Command, CommandObject
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from dotenv import load_dotenv

load_dotenv()
token = os.getenv('token')

bot = Bot(token=token) if token else None
dp = Dispatcher()
router = Router()

# 1-сүрөттөгүдөй ылдый жакта турчу кнопкалар (Reply Keyboard)
main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Привет")],
        [KeyboardButton(text="кандай")],
        [KeyboardButton(text="/time"), KeyboardButton(text="/help")],
        [KeyboardButton(text="/palindrom")]
    ],
    resize_keyboard=True
)


# 1. /start буйругу: Саламдашуу жана ылдыйкы кнопкаларды чыгаруу
@router.message(Command('start'))
async def start_part(message: Message):
    user_name = message.from_user.first_name or "Колдонуучу"
    await message.answer(
        f'Саламатсызбы {user_name}, кандай жардам бере алам?',
        reply_markup=main_keyboard
    )


# 2. 'привет' кнопкасы же тексти
@router.message(F.text.lower() == 'привет')
async def send_privet(message: Message):
    user_name = message.from_user.first_name or "Колдонуучу"
    await message.answer(f'Привет {user_name}!')


# 3. /time буйругу же кнопкасы
@router.message(Command('time'))
@router.message(F.text == '/time')
async def send_time(message: Message):
    form_time = datetime.datetime.utcnow().strftime('%d-%m-%Y %H:%M:%S')
    await message.answer(f'Убакыт: {form_time}')


# 4. /help буйругу же кнопкасы
@router.message(Command('help'))
@router.message(F.text == '/help')
async def send_help(message: Message):
    help_text = (
        '/start -> баштоо учун\n'
        '/time -> убакыт коруу учун\n'
        '/help -> жардам учун\n'
        '/palindrom -> палиндром учун'
    )
    await message.answer(help_text)


# 5. 'кандай' кнопкасы же тексти
@router.message(F.text.lower() == 'кандай')
async def send_again(message: Message):
    user_name = message.from_user.first_name or "Колдонуучу"
    await message.answer(f'Жакшы озун {user_name}?')


# 6. /palindrom буйругу же кнопкасы
@router.message(Command('palindrom'))
@router.message(F.text == '/palindrom')
async def cmd_palindrom(message: Message, command: CommandObject = None):
    if command and command.args:
        word = command.args.strip().lower()
        if word == word[::-1]:
            await message.answer('Palindrom')
        else:
            await message.answer('Palindrom emes')
    else:
        await message.answer('Палиндром текшерүү үчүн сөз жазыңыз (мисалы: /palindrom казак же жөн эле сөз жөнөтүңүз)')


# 7. Жөнөкөй текст жөнөтүлгөндө палиндром текшерүү (казак, madam, адам)
@router.message(F.text)
async def palindrom(message: Message):
    word = message.text.strip().lower()
    if word == word[::-1]:
        await message.answer('Palindrom')
    else:
        await message.answer('Palindrom emes')


async def main():
    if not token or token.startswith("YOUR_"):
        print("⚠️ Эскертүү: .env файлына BotFather'ден алган токениңизди жазыңыз!")
    print("Бот иштеп жатат...")
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
