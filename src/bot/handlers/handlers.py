from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command

router = Router()

@router.message(Command('start'))
async def start_handler(msg: Message):
    await msg.answer('Приветики! Хочешь ухнать свой id? Отправь мне любое сообщение!')

@router.message(F.photo)
async def send_foto_echo(msg: Message):
    await msg.reply_photo(msg.photo[0].file_id)


@router.message()
async def message_handler(msg: Message):
    print(msg.model_dump_json(indent=4, exclude_none=True))
    await msg.answer(f'Твой ID: {msg.from_user.id}')
    