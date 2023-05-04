from aiogram import types
from aiogram.dispatcher.storage import FSMContext

from crud.applicant_forms import CRUDUser
from keyboards.inline.users.main import MainForm_CB, Main
from loader import dp, bot
from schemas import UsersSchema
from states.users.mainState import MainState


@dp.message_handler(commands=["start"], state=MainState.all_states)
async def registration_start(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(text="Я бот который поможет тебе с часто задаваемыми вопросами",
                         reply_markup=await Main.start_ikb())


@dp.message_handler(commands=["start"])
async def registration_start(message: types.Message):
    user = await CRUDUser.get(user_id=message.from_user.id)
    text = "Привет, я бот который поможет тебе с часто задаваемыми вопросами"
    if user:
        await message.answer(text=text,
                             reply_markup=await Main.start_ikb())
    else:
        await CRUDUser.add(user=UsersSchema(user_id=message.from_user.id))
        await message.answer(text=text,
                             reply_markup=await Main.start_ikb())


@dp.message_handler(content_types="any")
async def echo(message: types.Message):
    user = await CRUDUser.get(user_id=message.from_user.id)
    if not message.reply_to_message:
        if user.specialist:
            await bot.forward_message(chat_id=-832964493,
                                      from_chat_id=message.from_user.id,
                                      message_id=message.message_id)
            user.specialist = False
            await CRUDUser.update(user=user)
    else:
        await bot.send_message(chat_id=message.reply_to_message.forward_from.id,
                               text=message.text,
                               reply_markup=await Main.replyExpert_ikb())


@dp.callback_query_handler(MainForm_CB.filter())
@dp.callback_query_handler(MainForm_CB.filter(), state=MainState.all_states)
async def process_callback(callback: types.CallbackQuery, state: FSMContext = None):
    await Main.main_form(callback=callback, state=state)


@dp.message_handler(state=MainState.all_states, content_types=["text", 'any'])
async def process_message(message: types.Message, state: FSMContext = None):
    await Main.main_form(message=message, state=state)
