from aiogram import types
from aiogram.dispatcher.storage import FSMContext
from aiogram.utils.exceptions import BadRequest

from handlers.users.Dialogflow import Dialogflow
from keyboards.inline.users.main import MainForm_CB, Main
from loader import dp, bot
from states.users.mainState import MainState


@dp.message_handler(commands=["start"], state=MainState.all_states)
async def registration_start(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(text="Я бот который поможет тебе с часто задаваемыми вопросами",
                         reply_markup=await Main.start_ikb())


@dp.message_handler(commands=["start"])
async def registration_start(message: types.Message):
    await message.answer(text="Привет, я бот который поможет тебе с часто задаваемыми вопросами",
                         reply_markup=await Main.start_ikb())


@dp.callback_query_handler(MainForm_CB.filter())
@dp.callback_query_handler(MainForm_CB.filter(), state=MainState.all_states)
async def process_callback(callback: types.CallbackQuery, state: FSMContext = None):
    await Main.main_form(callback=callback, state=state)


@dp.message_handler(state=MainState.all_states, content_types=["text"])
async def process_message(message: types.Message, state: FSMContext = None):
    await Main.main_form(message=message, state=state)
