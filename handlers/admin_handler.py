"""
en: Handlers for admin related requests
ru: Обработчики для запросов, связанных с администратором
"""
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from config import ADMIN_ID

router = Router()


# en: Decorators / ru: Декораторы
def is_admin(func):
    """
    en: Check if the user is a god
    ru: Проверить, является ли пользователь администратором
    """
    async def wrapper(message: Message):
        if message.from_user.id == int(ADMIN_ID):
            await func(message)
        else:
            await message.answer('You are not a admin!')
    return wrapper


# en: Handlers / ru: Обработчики
@router.message(F.text.startswith('/check_id'))
@is_admin
async def check_id_handler(message: Message):
    """
    en: Check the id of the user
    ru: Проверить id пользователя
    """
    await message.answer(f'Your id is {message.from_user.id}')


@router.message(F.photo)
@is_admin
async def get_photo_id(message: Message):
    """
    en: Get the id of the photo
    ru: Получить id фото
    """
    fid = f"Photo id: {message.photo[-1].file_id}"
    await message.answer(fid)


@router.message(F.audio)
@is_admin
async def get_audio_id(message: Message):
    """
    en: Get the id of the sound
    ru: Получить id аудиофайла
    """

    fid = f"Audio id: {message.audio.file_id}"
    await message.answer(fid)


@router.message(F.text == '/get_chat_id')
@is_admin
async def get_chat_id_handler(message: Message):
    """
    en: Get the id of the chat
    ru: Получить id чата
    """
    await message.answer(f'Chat id is {message.chat.id}')
