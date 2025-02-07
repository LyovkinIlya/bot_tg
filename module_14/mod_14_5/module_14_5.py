from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from crud_func_5 import *
import asyncio

api = ""
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

# Возвращает все записи из таблицы Products
pr = get_all_products()

kb1 = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Рассчитать'),
            KeyboardButton(text='Информация'),
        ],
        [
            KeyboardButton(text='Купить'),
            KeyboardButton(text='Регистрация')
        ]
    ], resize_keyboard=True
)

kb2 = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')],
        [InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')]
    ]
)

kb3 = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text=product1, callback_data="product_buying")],
        [InlineKeyboardButton(text=product2, callback_data="product_buying")],
        [InlineKeyboardButton(text=product3, callback_data="product_buying")],
        [InlineKeyboardButton(text=product4, callback_data="product_buying")]
    ]
)

@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer("Привет! Я бот помогающий твоему здоровью.", reply_markup=kb1)

@dp.message_handler(text="Купить")
async def get_buying_list(message):
    for i in pr:
        id, title, description, price = i
        await message.answer(f"Название: {title} |"
                             f"Штук в упаковке: {description} |"
                             f"Цена: {price}")
        with open(f'files_14/{id}.jpg', 'rb') as img:
             await message.answer_photo(img)
    await message.answer("Выберите продукт для покупки:", reply_markup=kb3)

@dp.callback_query_handler(text="product_buying")
async def send_confirm_message(call):
    await call.message.answer("Вы успешно приобрели продукт!")
    await call.answer()

@dp.message_handler(text='Рассчитать')
async def main_menu(message):
    await message.answer("Выберите опцию:", reply_markup=kb2)

@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    await call.message.answer('10 x вес(кг) + 6.25 х рост(см) - 5 х возраст(г) + 5')
    await call.answer()

class UserState(StatesGroup):
    age = State() # Возраст
    growth = State() # Рост
    weight = State() # Вес

@dp.callback_query_handler(text="calories")
async def set_age(call):
    await call.message.answer('Введите свой возраст:')
    await UserState.age.set()

@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer('Введите свой рост:')
    await UserState.growth.set()

@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer('Введите свой вес:')
    await UserState.weight.set()

@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    cal = 10 * float(data['weight']) + 6.25 * float(data['growth']) - 5 * float(data['age']) + 5
    await message.answer(f'Ваша норма калорий {cal}')
    await state.finish()

class RegistrationState(StatesGroup):
    username = State()
    email = State()
    age = State()

@dp.message_handler(text=["Регистрация"])
async def sing_up(message):
    await message.answer("Введите имя пользователя (только латинский алфавит):")
    await RegistrationState.username.set()

@dp.message_handler(state=RegistrationState.username)
async def set_username(message, state):
    if is_included(message.text):
        await message.answer("Пользователь существует, введите другое имя")
        return
    await state.update_data(username=message.text)
    await message.answer("Введите свой email:")
    await RegistrationState.email.set()

@dp.message_handler(state=RegistrationState.email)
async def set_email(message, state):
    await state.update_data(email=message.text)
    await message.answer("Введите свой возраст:")
    await RegistrationState.age.set()

@dp.message_handler(state=RegistrationState.age)
async def set_age(message, state):
    await state.update_data(age=message.text)
    data = await state.get_data()
    add_user(data['username'], data['email'], data['age'])
    await message.answer(f"Регистрация прошла успешно!")
    await state.finish()


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)