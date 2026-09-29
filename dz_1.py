import asyncio
import datetime
import os
from aiogram import Bot, Dispatcher, F, Router
from aiogram.filters import Command, CommandObject
from aiogram.types import Message
from dotenv import load_dotenv

load_dotenv()
token = os.getenv('token')

bot = Bot(token=token) if token else None
dp = Dispatcher()
router = Router()


# 1. /start буйругу: Саламатсызбы {user_name}, кандай жардам бере алам?
@router.message(Command('start'))
async def start_part(message: Message):
    user_name = message.from_user.first_name or "Колдонуучу"
    await message.answer(f'Саламатсызбы {user_name}, кандай жардам бере алам?')


# 2. /time буйругу: Убакыт: 28-09-2026 06:07:16
@router.message(Command('time'))
async def send_time(message: Message):
    form_time = datetime.datetime.utcnow().strftime('%d-%m-%Y %H:%M:%S')
    await message.answer(f'Убакыт: {form_time}')


# 3. /help буйругу: Командалардын тизмеси
@router.message(Command('help'))
async def send_help(message: Message):
    help_text = (
        '/start -> баштоо учун\n'
        '/time -> убакыт коруу учун\n'
        '/help -> жардам учун\n'
        '/palindrom -> палиндром учун'
    )
    await message.answer(help_text)


# 4. 'кандай' суроосу: Жакшы озун {user_name}?
@router.message(F.text.lower() == 'кандай')
async def send_again(message: Message):
    user_name = message.from_user.first_name or "Колдонуучу"
    await message.answer(f'Жакшы озун {user_name}?')


# 5. /palindrom буйругу (мисалы: /palindrom казак)
@router.message(Command('palindrom'))
async def cmd_palindrom(message: Message, command: CommandObject = None):
    if command and command.args:
        word = command.args.strip().lower()
        if word == word[::-1]:
            await message.answer('Palindrom')
        else:
            await message.answer('Palindrom emes')
    else:
        await message.answer('Палиндром текшерүү үчүн сөз жазыңыз (мисалы: /palindrom казак же жөн эле сөз жөнөтүңүз)')


# 6. Жөнөкөй сөз келгенде палиндром текшерүү (казак, madam, адам)
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
    print("ДЗ 1 боту иштеп жатат...")
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
