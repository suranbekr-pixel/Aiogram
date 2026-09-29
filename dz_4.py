import asyncio
import os
from aiogram import Bot, Dispatcher, F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import KeyboardButton, Message, ReplyKeyboardMarkup, ReplyKeyboardRemove
from dotenv import load_dotenv

load_dotenv()
token = os.getenv('token')

bot = Bot(token=token) if token else None
dp = Dispatcher(storage=MemoryStorage())
router = Router()


# FSM Абалдары (Катталуу үчүн)
class Register(StatesGroup):
    name = State()
    phone = State()
    email = State()
    age = State()


# Баштапкы клавиатура
start_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Катталуу")]
    ],
    resize_keyboard=True
)


# 1. /start буйругу
@router.message(Command('start'))
async def start_reg(message: Message):
    await message.answer(
        'Катталуу учун "Катталуу" баскычын басыныз!',
        reply_markup=start_kb
    )


# 2. 'Катталуу' басылганда катталуу процесси башталат
@router.message(F.text == 'Катталуу')
async def begin_register(message: Message, state: FSMContext):
    await state.set_state(Register.name)
    await message.answer(
        'Катталуу башталды!\nАтынызды жазыныз:',
        reply_markup=ReplyKeyboardRemove()
    )


# 3. Атын кабыл алуу -> Телефон суроо
@router.message(Register.name)
async def process_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text.strip())
    await state.set_state(Register.phone)
    await message.answer('Байланыш номер жазыныз:')


# 4. Телефон номерин текшерүү (+996 код менен башталышы керек)
@router.message(Register.phone)
async def process_phone(message: Message, state: FSMContext):
    phone = message.text.strip()
    if not phone.startswith('+996'):
        error_msg = (
            'Телефон номер алдында "+996" код болушу шарт!\n'
            'Мисалы: +996 701 090 909'
        )
        await message.answer(error_msg)
        return

    await state.update_data(phone=phone)
    await state.set_state(Register.email)
    await message.answer('Почтанызды жазыныз')


# 5. Почтаны кабыл алуу -> Жашын суроо
@router.message(Register.email)
async def process_email(message: Message, state: FSMContext):
    await state.update_data(email=message.text.strip())
    await state.set_state(Register.age)
    await message.answer('Жашынды жаз:')


# 6. Жашын кабыл алуу жана катталууну жыйынтыктоо
@router.message(Register.age)
async def process_age(message: Message, state: FSMContext):
    await state.update_data(age=message.text.strip())
    data = await state.get_data()

    finish_text = (
        'Катталуу аякталды!\n'
        f"Аты: {data.get('name')}\n"
        f"Телефон номер: {data.get('phone')}\n"
        f"Почта: {data.get('email')}\n"
        f"Жашы: {data.get('age')}"
    )
    await message.answer(finish_text, reply_markup=start_kb)
    await state.clear()


async def main():
    if not token or token.startswith("YOUR_"):
        print("⚠️ Эскертүү: .env файлына BotFather'ден алган токениңизди жазыңыз!")
    print("ДЗ 4 (Катталуу FSM) боту иштеп жатат...")
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
