from loader import form_router, bot
from aiogram.filters.command import Command
from aiogram.types import Message
from parsing import parsing


@form_router.message(Command("start"))
async def say_hello(message: Message):
    await message.answer("Hello")
