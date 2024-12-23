from loader import form_router, bot
from aiogram.filters.command import Command
from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder


@form_router.message(Command("start"))
async def say_hello(message: Message):
    kb = InlineKeyboardBuilder()
    kb.button(text="Магазин",
              url="https://dbb5-37-132-243-122.ngrok-free.app")
    await message.answer("Привет, мы будем "
                         "рады видеть тебя "
                         "в нашем магазине по ссылке ниже",
                         reply_markup=kb.as_markup())
