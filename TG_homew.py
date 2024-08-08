from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio


api = ""
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

keyB = ReplyKeyboardMarkup(resize_keyboard=True)
Bbutt_1 = KeyboardButton(text='Информация')
Bbutt_2 = KeyboardButton(text='Рассчитать')
keyB.add(Bbutt_1)
keyB.add(Bbutt_2)

Kboard = InlineKeyboardMarkup()
Kbutt_1 = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
Kbutt_2 = InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')
Kboard.add(Kbutt_1)
Kboard.add(Kbutt_2)
# kb.insert kb.row




@dp.message_handler(text='Рассчитать')
async def main_menu(mess):
    await mess.answer(text='Выберите опцию:', reply_markup=Kboard)


@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    await call.message.answer(text='10 х вес(кг) + 6,25 x рост(см) – 5 х возраст(г) + 5')
    await call.answer()


@dp.message_handler(text='Информация')
async def info(mess):
    await mess.answer('Тут будет информация о боте')


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@dp.callback_query_handler(text='calories')
async def set_age(call):
    await call.message.answer('Введите свой возраст')
    await UserState.age.set()
    await call.answer()


@dp.message_handler(state=UserState.age)
async def set_growth(mess, state):
    await state.update_data(age=mess.text)
    await mess.answer('Введите свой рост')
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(mess, state):
    await state.update_data(growth=mess.text)
    await mess.answer('Введите свой вес')
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(mess, state):
    await state.update_data(weight=mess.text)
    data = await state.get_data()
    calories = 10 * int(data['weight']) + 6.25 * int(data['growth']) - 5 * int(data['age']) + 5
    await mess.answer(f'Ваши калории {calories}')
    await state.finish()


@dp.message_handler(commands=['start'])
async def consol_command(messe):
    await messe.answer('Привет! Я бот помогающий твоему здоровью.', reply_markup=keyB)


@dp.message_handler()
async def other_message(mess):
    await mess.answer('Введите команду /start, чтобы начать общение.')


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
