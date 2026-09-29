import asyncio
import os
from aiogram import Bot, Dispatcher, F, Router
from aiogram.filters import Command
from aiogram.types import Message
from dotenv import load_dotenv

load_dotenv()
token = os.getenv('token')

bot = Bot(token=token) if token else None
dp = Dispatcher()
router = Router()


@router.message(Command('info'))
async def send_info(message: Message):
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    user_id = message.from_user.id
    response = (
        f"Атын: {first_name}\n"
        f"Фамилия: {last_name}\n"
        f"id: {user_id}"
    )
    await message.answer(response)



@router.message(F.text.lower() == 'салам')
async def send_salam(message: Message):
    await message.answer('Салам')



@router.message(F.text.lower().startswith('хочу'))
async def send_want(message: Message):
    # 'хочу' деген сөздү алып салуу
    clean_text = message.text[4:].strip()
    await message.answer(f'Ты хочешь: {clean_text}')


@router.message(F.text)
async def count_words_symbols(message: Message):
    words = len(message.text.split())
    symbols = len(message.text)
    # Скриншоттогудай 2 өзүнчө билдирүү катары жөнөтүлөт:
    await message.answer(f'Words: {words}')
    await message.answer(f'Symbols: {symbols}')


async def main():
    if not token or token.startswith("YOUR_"):
        print("⚠️ Эскертүү: .env файлына BotFather'ден алган токениңизди жазыңыз!")
    print("ДЗ 2 боту иштеп жатат...")
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
