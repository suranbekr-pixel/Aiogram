import asyncio
import datetime
import logging
import os
from aiogram import Bot, Dispatcher, F, Router
from aiogram.filters import Command
from aiogram.types import Message
from dotenv import load_dotenv

load_dotenv()
token = os.getenv('token')
logging.basicConfig(level=logging.INFO)

bot = Bot(token=token) if token else None
dp = Dispatcher()
router = Router()


@router.message(Command('start'))
async def start_part(message: Message):
    first_name = message.from_user.first_name
    await message.answer(f'Салам {first_name}, кандай жардам керек?')


@router.message(F.text.lower() == 'салам')
async def send_salam(message: Message):
    await message.answer('Салам')


@router.message(F.text.startswith('хочу'))
async def send_want(message: Message):
    new_text = message.text.replace('хочу', '').strip()
    await message.answer(f'Ты хочешь: {new_text}')


@router.message(F.photo)
async def get_image(message: Message):
    await message.answer('Сонун сурот экен')
    image_id = message.photo[-1].file_id
    await message.answer(f'File ID: {image_id}')


@router.message(F.document)
async def get_document(message: Message):
    size_file = message.document.file_size
    file_name = message.document.file_name
    await message.answer(f'File name 😊: {file_name}, File size: {size_file} KB')


async def main():
    if not token:
        print("Ката: .env файлында 'token' табылган жок. Сураныч, .env файлына токениңизди жазыңыз!")
        return
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
