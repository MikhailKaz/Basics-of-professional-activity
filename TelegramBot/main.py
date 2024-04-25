import asyncio
import logging
import sys
from os import getenv
from typing import Any, Dict

from aiogram import Bot, Dispatcher, F, Router, html
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)

TOKEN = "6928196552:AAFM9YB0aIjHNL0HbDAYuZgwt2NInhq9g2M"

form_router = Router()


class Form(StatesGroup): # переменные
    name = State()
    date = State()
    time = State()
    doctor = State()


@form_router.message(CommandStart()) # /start
async def command_start(message: Message, state: FSMContext) -> None:
    await state.set_state(Form.name)
    await message.answer(
        "Введите ФИО",
        reply_markup=ReplyKeyboardRemove(),
    )

#@form_router.message(Command("отмена"))
@form_router.message(F.text.casefold() == "Отмена") # отменить любое действие
async def cancel_handler(message: Message, state: FSMContext) -> None:

    current_state = await state.get_state()
    if current_state is None:
        return

    #logging.info("Cancelling state %r", current_state)
    await state.clear()
    await message.answer(
        "Отменено",
        reply_markup=ReplyKeyboardRemove(),
    )

@form_router.message(Form.name)
async def  process_name(message: Message, state: FSMContext) -> None:

    Form.name = message.text  # ------------------
    await state.set_state(Form.doctor)
    await message.answer(f"{html.quote(message.text)} к какому врачу вы хотите записаться?", reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="Терапевт")],
                [KeyboardButton(text="Лор")],
                [KeyboardButton(text="Стоматолог")],
                [KeyboardButton(text="Офтальмолог")],
                [KeyboardButton(text="Хирург")],
            ],
            resize_keyboard=True,
        ),
    )

@form_router.message(Form.doctor, F.text.in_({"Терапевт", "Лор",  "Терапевт",  "Стоматолог",  "Офтальмолог",  "Хирург"}))
async def process_like_write_bots(message: Message, state: FSMContext) -> None:

    Form.doctor = message.text # ------------------
    await state.set_state(Form.date)
    await message.answer(
        "Выберите число приёма на следующий месяц:",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="01"),KeyboardButton(text="02"),KeyboardButton(text="03"),KeyboardButton(text="04"),KeyboardButton(text="05")],
                [KeyboardButton(text="08"),KeyboardButton(text="09"),KeyboardButton(text="10"),KeyboardButton(text="11"),KeyboardButton(text="12")],
                [KeyboardButton(text="15"),KeyboardButton(text="16"),KeyboardButton(text="17"),KeyboardButton(text="18"),KeyboardButton(text="19")],
                [KeyboardButton(text="22"),KeyboardButton(text="23"),KeyboardButton(text="24"),KeyboardButton(text="25"),KeyboardButton(text="26")],
                [KeyboardButton(text="29"),KeyboardButton(text="30"),KeyboardButton(text="31")],
            ],
            resize_keyboard=True,
        ),
    )

@form_router.message(Form.doctor)
async def process_unknown_write_bots(message: Message) -> None:
    await message.reply("Некорректные данные")

@form_router.message(Form.date)
async def process_like_write_bots(message: Message, state: FSMContext) -> None:

    Form.date = message.text # ------------------
    await state.set_state(Form.time)
    await message.answer(
        "Выберите время приёма:",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="08:00"),KeyboardButton(text="13:00")],
                [KeyboardButton(text="09:00"),KeyboardButton(text="14:00")],
                [KeyboardButton(text="10:00"),KeyboardButton(text="15:00")],
                [KeyboardButton(text="11:00"),KeyboardButton(text="16:00")],
                [KeyboardButton(text="12:00"),KeyboardButton(text="17:00")],
            ],
            resize_keyboard=True,
        ),
    )

@form_router.message(Form.time)
async def process_language(message: Message, state: FSMContext) -> None:
    await message.answer(f"{html.quote(Form.name)} вы записаны к {html.quote(Form.doctor)} {html.quote(Form.date)} числа в {html.quote(message.text)}")

async def main():
    bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher()
    dp.include_router(form_router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())