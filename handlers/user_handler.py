"""
en: Module for user handlers / ru: Модуль для обработчиков пользователей
"""
import os
import random

from aiogram import Router, F, types
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import FSInputFile

import config
import phrases
import bot_messages
import db


router = Router()


# en: Handlers for /commands
# ru: Обработчики для /команд

#
class FrameQuiz(StatesGroup):
    quiz = State()


@router.message(F.text, Command('start'))
async def start_handler(message: Message):
    """
    en: Start message
    ru: Стартовое сообщение
    """
    user_id = message.from_user.id
    # en: Check if the user is in the database
    # ru: Проверить, есть ли пользователь в базе данных
    if not user_id == int(config.ADMIN_ID):
        # en: Check if the user is in the database
        # ru: Проверить, есть ли пользователь в базе данных
        check = db.get_data_from_db(config.USERS_TABLE, 'user_id', user_id)
        if not check:
            tmp_dict = {
                'user_id': user_id,
                'username': message.from_user.username,
                'full_name': message.from_user.full_name,
                'date': message.date
            }
            db.insert_into_db('users', tmp_dict)

    header_data = db.get_data_from_db(config.BOT_IMG_TABLE, 'name', 'header_animation')[-1]
    # en: Try to send the animation by file_id
    # ru: Попробовать отправить анимацию по file_id
    try:
        file_id = header_data['file_id']
        await message.answer_animation(animation=file_id, caption=bot_messages.START, parse_mode='HTML')
    # en: If the file_id is not found, send the animation by path and save the file_id to the database
    # ru: Если file_id не найден, отправить анимацию по пути и сохранить file_id в базу данных
    except Exception as e:
        print(e)
        await message.bot.send_message(config.ADMIN_ID, f'Error with "{header_data['name']}": {e}')
        img_path = os.path.join(config.PROJECT_PATH, header_data['file_path'])
        animation = FSInputFile(str(img_path))
        send_animation = await message.answer_animation(
            animation=animation,
            caption=bot_messages.START,
            parse_mode='HTML'
        )
        db.update_value(
            'bot_img',
            'file_id',
            send_animation.video.file_id,
            'id',
            header_data['id']
        )


@router.message(F.text, Command('help'))
async def help_handler(message: Message):
    """
    en: Instructions for commands
    ru: Справка по командам
    """
    help_data = db.get_data_from_db(config.BOT_IMG_TABLE, 'name', 'help')[-1]
    # en: Try to send the animation by file_id
    # ru: Попробовать отправить анимацию по file_id
    try:
        file_id = help_data['file_id']
        await message.answer_photo(photo=file_id, caption=bot_messages.HELP, parse_mode='HTML')
    # en: If the file_id is not found, send the animation by path and save the file_id to the database
    # ru: Если file_id не найден, отправить анимацию по пути и сохранить file_id в базу данных
    except Exception as e:
        print(e)
        await message.bot.send_message(config.ADMIN_ID, f'Error with "{help_data['name']}": {e}')
        img_path = os.path.join(config.PROJECT_PATH, help_data['file_path'])
        animation = FSInputFile(str(img_path))
        send_photo = await message.answer_photo(
            photo=animation,
            caption=bot_messages.HELP,
            parse_mode='HTML'
        )
        db.update_value(
            'bot_img',
            'file_id',
            send_photo.photo[-1].file_id,
            'id',
            help_data['id']
        )


# en: Handlers for text messages
# ru: Обработчики для текстовых сообщений

@router.message(F.text.func(lambda text: any(word in text.lower() for word in phrases.HELLO)))
async def hello_handler(message: Message):
    """
    en: Hello message
    ru: Приветственное сообщение
    """
    await message.answer('en: Hello!\nru: Привет!')


@router.message(F.text.func(lambda text: any(word in text.lower() for word in phrases.HATE)))
async def hate_handler(message: Message):
    """
    en: The word that cannot be pronounced
    ru: Слово, которое нельзя произносить
    """
    await message.answer(bot_messages.HATE)


@router.message(F.text.func(lambda text: any(word in text.lower() for word in phrases.DREAM)))
async def dream_handler(message: Message):
    """
    en: Dream message
    ru: Сообщение о снах
    """
    data = db.get_data_from_db(config.THEME_PHRASE_TABLE, 'theme', 'dream')
    if data:
        # en: Get a random phrase from the database
        # ru: Получить случайную фразу из базы данных
        send_text = random.choice(data)['phrase']
    else:
        send_text = bot_messages.EMPTY_DB
    await message.answer(send_text)


@router.message(F.text.func(lambda text: any(word in text.lower() for word in phrases.TIME)))
async def dream_handler(message: Message):
    """
    en: Time message
    ru: Сообщение о времени
    """
    data = db.get_data_from_db(config.THEME_PHRASE_TABLE, 'theme', 'time')
    if data:
        # en: Get a random phrase from the database
        # ru: Получить случайную фразу из базы данных
        send_text = random.choice(data)['phrase']
    else:
        send_text = bot_messages.EMPTY_DB
    await message.answer(send_text)


@router.message(F.text.func(lambda text: any(word in text.lower() for word in phrases.PLAY)))
async def play_handler(message: Message, state: FSMContext):
    """
    en: Play message: get a random image from the database and create a poll
    ru: Сообщение о игре: получить случайное изображение из базы данных и создать опрос
    """
    data = db.get_data_from_db(config.FRAME_QUIZ_TABLE)
    if not data:
        # en: If the database is empty, send a message
        # ru: Если база данных пуста, отправить сообщение
        await message.answer(bot_messages.EMPTY_DB)
        return
    # en: Get a random image from the database
    # ru: Получить случайное изображение из базы данных
    random_data = random.choice(data)
    # en: Set list for mix the answers
    # ru: Установить список для перемешивания ответов
    variant_answers = [
        random_data['correct'],
        random_data['uncorrect_1'],
        random_data['uncorrect_2'],
        random_data['uncorrect_3']
    ]
    # en: Mix the answers
    # ru: Перемешать ответы
    mix_data = random.sample(variant_answers, len(variant_answers))
    # en: Try to send the image by file_id
    # ru: Попробовать отправить изображение по file_id
    try:
        await message.answer_photo(photo=random_data['question_file_id'], caption='Отгадай фильм или картину!')
    # en: If the file_id is not found, send the image by path and save the file_id to the database
    # ru: Если file_id не найден, отправить изображение по пути и сохранить file_id в базу данных
    except Exception as e:
        print(e)
        await message.bot.send_message(config.ADMIN_ID, f'Error: {e}')
        img_path = os.path.join(config.PROJECT_PATH, random_data['question_img'])
        question_img = FSInputFile(str(img_path))
        send_photo = await message.answer_photo(photo=question_img, caption='Отгадай фильм или картину!')
        db.update_value(
            'frame_quiz',
            'question_file_id',
            send_photo.photo[-1].file_id,
            'id',
            random_data['id']
        )
    # en: save the data to the state
    # ru: сохранить данные в состояние
    # await state.update_data(quiz=random_data['id'])

    # en: create a poll
    # ru: создать опрос
    send_poll = await message.answer_poll(
        question='Выберите правильный ответ',
        options=mix_data,
        correct_option_id=mix_data.index(random_data['correct']),
        type='quiz',
        is_anonymous=False,
        explanation=f'Правильный ответ: {random_data["correct"]}',
        reply_markup=None
    )
    data = await state.get_data()
    data[send_poll.poll.id] = random_data['id']
    await state.update_data(data)


@router.poll_answer()
async def poll_answer_handler(poll_answer: types.PollAnswer, state: FSMContext):
    """
    en: Poll answer handler
    ru: Обработчик ответа на опрос
    """
    """data = await state.get_data()
    print(data.get(poll_answer.poll_id))"""
    # en: Try to send the answer image by file_id
    # ru: Попробовать отправить изображение ответа по file_id
    data = await state.get_data()
    answer_id = data.get(poll_answer.poll_id)
    if not answer_id:
        return
    try:
        file_id = db.get_data_from_db(config.FRAME_QUIZ_TABLE, 'id', answer_id)[-1]['answer_file_id']
        await poll_answer.bot.send_photo(
            chat_id=poll_answer.user.id,
            photo=file_id,
            caption='Было загадано это изображение!'
        )
    # en: If the file_id is not found, send the image by path and save the file_id to the database
    # ru: Если file_id не найден, отправить изображение по пути и сохранить file_id в базу данных
    except Exception as e:
        print(e)
        await poll_answer.bot.send_message(config.ADMIN_ID, f'Error: {e}')
        img_path = os.path.join(
            config.PROJECT_PATH,
            db.get_data_from_db(config.FRAME_QUIZ_TABLE, 'id', answer_id)[-1]['answer_img']
        )
        answer_img = FSInputFile(str(img_path))
        send_photo = await poll_answer.bot.send_photo(
            chat_id=poll_answer.user.id,
            photo=answer_img,
            caption='Было загадано это изображение!'
        )
        db.update_value(
            'frame_quiz',
            'answer_file_id',
            send_photo.photo[-1].file_id,
            'id',
            answer_id
        )

    data.pop(poll_answer.poll_id)
    await state.clear()
    await state.update_data(data)


@router.message(F.text.func(lambda text: any(word in text.lower() for word in phrases.PITER_PAN)))
async def peter_pan_handler(message: Message):
    """
    en: Peter Pan message
    ru: Сообщение о Питере Пэне
    """
    data = db.get_data_from_db(config.PITER_TABLE)
    if not data:
        # en: If the database is empty, send a message
        # ru: Если база данных пуста, отправить сообщение
        await message.answer(bot_messages.EMPTY_DB)
        return
    random_data = random.choice(data)
    description = random_data['description']

    # en: Try to send the audio by file_id
    # ru: Попробовать отправить аудио по file_id
    try:
        track = random_data['file_id']
        await message.answer_audio(audio=track, caption=description)
    # en: If the file_id is not found, send the audio by path and save the file_id to the database
    # ru: Если file_id не найден, отправить аудио по пути и сохранить file_id в базу данных
    except Exception as e:
        print(e)
        await message.bot.send_message(config.ADMIN_ID, f'Error: {e}')
        file_path = os.path.join(config.PROJECT_PATH, random_data['file_path'])
        send_audio = await message.answer_audio(audio=FSInputFile(str(file_path)), caption=description)
        db.update_value(
            'piter',
            'file_id',
            send_audio.audio.file_id,
            'id',
            random_data['id']
        )


@router.message(F.text.lower().in_(phrases.GET_GOOD_NEWS))
async def good_news_handler(message: Message):
    """
    en: Good news message
    ru: Сообщение с хорошими новостями
    """
    data = db.get_data_from_db(config.GOOD_NEWS_TABLE)
    if data:
        good_news = random.choice(data)['news']
    else:
        good_news = ('Еще никто не делился хорошими новостями. Поделись первым!\n'
                     '```пиши_боту: моя хорошая новость: <текст>```')
    await message.answer(good_news, parse_mode='Markdown')


@router.message(F.text.lower().startswith(phrases.SET_GOOD_NEWS))
async def set_good_news_handler(message: Message):
    """
    en: Set good news message
    ru: Сообщение о хороших новостях
    """
    good_news = ':'.join(message.text.split(':')[1:]).strip()
    # en: If the user correct entered the news, save it to the database
    # ru: Если пользователь правильно ввел новость, сохранить ее в базу данных
    if good_news:
        db.insert_into_db('good_news', {'news': good_news.capitalize()})
        await message.answer('Спасибо, что поделился хорошей новостью!')
    else:
        await message.answer('Пожалуйста, введите хорошую новость в формате '
                             '<pre>пиши_боту: моя хорошая новость: [ваш текст]</pre>', parse_mode='HTML')


@router.message(F.text.func(lambda text: any(text.lower().startswith(word.lower()) for word in phrases.SET_MESSAGE)))
async def set_message_handler(message: Message):
    """
    en: Set message handler
    ru: Обработчик установки сообщения
    """
    message_text = ':'.join(message.text.split(':')[1:]).strip()
    temp_dict = {
        'user_id': message.from_user.id,
        'username': message.from_user.username,
        'full_name': message.from_user.full_name,
        'message': message_text.capitalize(),
        'date': message.date
    }
    # en: If the user correct entered the message, save it to the database
    # ru: Если пользователь правильно ввел сообщение, сохранить его в базу данных
    if message_text:
        db.insert_into_db('users_messages', temp_dict)
        await message.answer('Спасибо, что оставил сообщение!')
    else:
        await message.answer('Пожалуйста, введите сообщение в формате '
                             '<pre>пиши_боту: мое послание: [ваш текст]</pre>', parse_mode='HTML')


@router.message(F.text)
async def message_handler(message: Message):
    """
    en: Regular message handler
    ru: Обработчик обычных сообщений
    """
    data = db.get_data_from_db(config.REGULAR_PHRASE_TABLE)
    if data:
        random_data = random.choice(data)['phrase']
    else:
        random_data = bot_messages.EMPTY_DB
    await message.answer(random_data)
