from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from aiogram.utils.exceptions import BadRequest

from handlers.users.Dialogflow import Dialogflow
from loader import bot
from states.users.mainState import MainState

MainForm_CB = CallbackData("MainPage", "target", "action", "id", "editId")


class Main:

    @staticmethod
    async def back_ikb():
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="◀️ Назад", callback_data=MainForm_CB.new("MainMenu", 0, 0, 0)
                                         )
                ]
            ]
        )

    @staticmethod  # Главное меню
    async def start_ikb() -> InlineKeyboardMarkup:
        """
        Самая стартовая клавиатура  главного меню
        :return:
        """
        data_start = {
            "Задать вопрос": "askQuestion"
        }
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text=menu,
                                         callback_data=MainForm_CB.new(menu_target, "getQuestion", 0, 0)
                                         )
                ] for menu, menu_target in data_start.items()
            ]
        )

    @staticmethod
    async def main_form(callback: CallbackQuery = None, message: Message = None, state: FSMContext = None) -> None:
        if callback:
            if callback.data.startswith('MainPage'):
                data = MainForm_CB.parse(callback_data=callback.data)

                if data.get("target") == "MainMenu":
                    await state.finish()
                    await callback.message.edit_text(text="Я бот который поможет тебе с часто задаваемыми вопросами",
                                                     reply_markup=await Main.start_ikb())

                elif data.get("target") == "askQuestion":
                    if data.get("action") == "getQuestion":
                        await callback.message.edit_text(text="Введите ваш вопрос ⬇️",
                                                         reply_markup=await Main.back_ikb())
                        await MainState.Answer.set()

        if message:
            await message.delete()

            try:
                await bot.delete_message(
                    chat_id=message.from_user.id,
                    message_id=message.message_id - 1
                )
            except BadRequest:
                pass

            if state:
                if await state.get_state() == "MainState:Answer":
                    dialogflow = Dialogflow(text=message.text)
                    answer = await dialogflow.get_dialogflow_response()
                    await message.answer(text=answer,
                                         reply_markup=await Main.back_ikb())
                    await state.finish()
