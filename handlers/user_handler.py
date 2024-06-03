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

# en: Create a router / ru: Создать роутер
router = Router()

# en: Handlers for /commands
# ru: Обработчики для /команд


# en: Create a state for the quiz / ru: Создать состояние для викторины
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

    header_data = db.get_data_from_db(config.BOT_IMG_TABLE, 'name', 'header_animation')
    if not header_data:
        await message.answer(bot_messages.START, parse_mode='HTML')
        return
    # en: Try to send the animation by file_id
    # ru: Попробовать отправить анимацию по file_id
    try:
        file_id = header_data[-1]['file_id']
        await message.answer_animation(animation=file_id, caption=bot_messages.START, parse_mode='HTML')
    # en: If the file_id is not found, send the animation by path and save the file_id to the database
    # ru: Если file_id не найден, отправить анимацию по пути и сохранить file_id в базу данных
    except Exception as e:
        # en: Send a message to the admin about the error
        # ru: Отправить сообщение администратору об ошибке
        await message.bot.send_message(config.ADMIN_ID, f'Error with «{header_data[-1]["name"]}»:\n{e}')
        img_path = os.path.join(config.PROJECT_PATH, header_data[-1]['file_path'])
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
            header_data[-1]['id']
        )


@router.message(F.text, Command('help'))
async def help_handler(message: Message):
    """
    en: Instructions for commands
    ru: Справка по командам
    """
    help_data = db.get_data_from_db(config.BOT_IMG_TABLE, 'name', 'help')
    if not help_data:
        await message.answer(bot_messages.HELP, parse_mode='HTML')
        await message.answer(bot_messages.HELP_EN, parse_mode='HTML')
        return
    # en: Try to send the animation by file_id
    # ru: Попробовать отправить анимацию по file_id
    try:
        file_id = help_data[-1]['file_id']
        await message.answer_photo(photo=file_id, caption=bot_messages.HELP, parse_mode='HTML')
    # en: If the file_id is not found, send the animation by path and save the file_id to the database
    # ru: Если file_id не найден, отправить анимацию по пути и сохранить file_id в базу данных
    except Exception as e:
        # en: Send a message to the admin about the error
        # ru: Отправить сообщение администратору об ошибке
        await message.bot.send_message(config.ADMIN_ID, f'Error with «{help_data[-1]["name"]}»:\n{e}')
        img_path = os.path.join(config.PROJECT_PATH, help_data[-1]['file_path'])
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
            help_data[-1]['id']
        )
    await message.answer(bot_messages.HELP_EN, parse_mode='HTML')


# en: Handlers for text messages
# ru: Обработчики для текстовых сообщений


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
    quiz_data = db.get_data_from_db(config.FRAME_QUIZ_TABLE)
    if not quiz_data:
        # en: If the database is empty, send a message
        # ru: Если база данных пуста, отправить сообщение
        await message.answer(bot_messages.EMPTY_DB)
        return
    # en: Get a random image from the database
    # ru: Получить случайное изображение из базы данных
    random_data = random.choice(quiz_data)
    # en: Set list for mix the answers
    # ru: Установить список для перемешивания ответов
    variant_answers = [
        random_data['correct'],
        random_data['incorrect_1'],
        random_data['incorrect_2'],
        random_data['incorrect_3']
    ]
    # en: Mix the answers
    # ru: Перемешать ответы
    mix_data = random.sample(variant_answers, len(variant_answers))
    # en: Try to send the image by file_id
    # ru: Попробовать отправить изображение по file_id
    try:
        await message.answer_photo(
            photo=random_data['question_file_id'],
            caption='ru: Отгадай фильм или картину! / en: Guess the movie or picture!'
        )
    # en: If the file_id is not found, send the image by path and save the file_id to the database
    # ru: Если file_id не найден, отправить изображение по пути и сохранить file_id в базу данных
    except Exception as e:
        # en: Send a message to the admin about the error
        # ru: Отправить сообщение администратору об ошибке
        await message.bot.send_message(config.ADMIN_ID, f'Error with «{random_data["question_img"]}»:\n{e}')
        img_path = os.path.join(config.PROJECT_PATH, random_data['question_img'])
        question_img = FSInputFile(str(img_path))
        send_photo = await message.answer_photo(
            photo=question_img,
            caption='ru: Отгадай фильм или картину! / en: Guess the movie or picture!')
        db.update_value(
            'frame_quiz',
            'question_file_id',
            send_photo.photo[-1].file_id,
            'id',
            random_data['id']
        )

    # en: create a poll
    # ru: создать опрос
    send_poll = await message.answer_poll(
        question='ru: Выберите правильный ответ / en: Choose the correct answer',
        options=mix_data,
        correct_option_id=mix_data.index(random_data['correct']),
        type='quiz',
        is_anonymous=False,
        explanation=f'ru: Правильный ответ / en: The correct answer:\n{random_data["correct"]}',
        reply_markup=None
    )

    # en: Save the poll id and the correct answer id to the state
    # ru: Сохранить id опроса и id правильного ответа в состояние
    data = await state.get_data()
    data[send_poll.poll.id] = random_data['id']
    await state.update_data(data)


@router.poll_answer()
async def poll_answer_handler(poll_answer: types.PollAnswer, state: FSMContext):
    """
    en: Poll answer handler
    ru: Обработчик ответа на опрос
    """

    # en: Try to send the answer image by file_id
    # ru: Попробовать отправить изображение ответа по file_id
    data = await state.get_data()
    answer_id = data.get(poll_answer.poll_id)
    if not answer_id:
        return
    answer_data = db.get_data_from_db(config.FRAME_QUIZ_TABLE, 'id', answer_id)
    if not answer_data:
        await poll_answer.bot.send_message(poll_answer.user.id, bot_messages.EMPTY_DB)
        return
    file_id = answer_data[-1]['answer_file_id']
    # en: Try to send the image by file_id
    # ru: Попробовать отправить изображение по file_id
    try:
        await poll_answer.bot.send_photo(
            chat_id=poll_answer.user.id,
            photo=file_id,
            caption='ru: Было загадано это изображение!\n\n'
                    'en: This image was guessed!'
        )
    # en: If the file_id is not found, send the image by path and save the file_id to the database
    # ru: Если file_id не найден, отправить изображение по пути и сохранить file_id в базу данных
    except Exception as e:
        # en: Send a message to the admin about the error
        # ru: Отправить сообщение администратору об ошибке
        await poll_answer.bot.send_message(config.ADMIN_ID, f'Error with «{answer_data[-1]["answer_img"]}»:\n{e}')
        img_path = os.path.join(
            config.PROJECT_PATH,
            answer_data[-1]["answer_img"]
        )
        answer_img = FSInputFile(str(img_path))
        send_photo = await poll_answer.bot.send_photo(
            chat_id=poll_answer.user.id,
            photo=answer_img,
            caption='ru: Было загадано это изображение!\n\n'
                    'en: This image was guessed!'
        )
        db.update_value(
            'frame_quiz',
            'answer_file_id',
            send_photo.photo[-1].file_id,
            'id',
            answer_id
        )

    # en: Delete the poll id from the state
    # ru: Удалить id опроса из состояния
    data.pop(poll_answer.poll_id)
    await state.clear()
    await state.update_data(data)


@router.message(F.text.func(lambda text: any(word in text.lower() for word in phrases.PITER_PAN)))
async def peter_pan_handler(message: Message):
    """
    en: Peter Pan message
    ru: Сообщение о Питере Пэне
    """
    piter_data = db.get_data_from_db(config.PITER_TABLE)
    if not piter_data:
        # en: If the database is empty, send a message
        # ru: Если база данных пуста, отправить сообщение
        await message.answer(bot_messages.EMPTY_DB)
        return
    random_data = random.choice(piter_data)
    description = random_data['description']

    # en: Try to send the audio by file_id
    # ru: Попробовать отправить аудио по file_id
    try:
        track = random_data['file_id']
        await message.answer_audio(audio=track, caption=description)
    # en: If the file_id is not found, send the audio by path and save the file_id to the database
    # ru: Если file_id не найден, отправить аудио по пути и сохранить file_id в базу данных
    except Exception as e:
        # en: Send a message to the admin about the error
        # ru: Отправить сообщение администратору об ошибке
        await message.bot.send_message(config.ADMIN_ID, f'Error with «{random_data["file_path"]}»:\n{e}')
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
        good_news = ('ru: Еще никто не делился хорошими новостями. Поделись первым! Пиши_боту:\n'
                     '<pre>Моя хорошая новость: [ваш текст]</pre>\n\n'
                     'en: No one has shared good news yet. Be the first to share! Write_to_bot:\n'
                     '<pre>My good news: [your text]</pre>')
    await message.answer(good_news, parse_mode='HTML')


@router.message(F.text.func(lambda text: any(text.lower().startswith(word.lower()) for word in phrases.SET_GOOD_NEWS)))
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
        await message.answer('ru: Спасибо, что поделился хорошей новостью!'
                             '\n\nen: Thank you for sharing the good news!')
    else:
        await message.answer(
            'ru: Пожалуйста, введите хорошую новость в формате:\n'
            '<pre>Моя хорошая новость: [ваш текст]</pre>'
            'en: Please, enter the good news in the format:\n'
            '<pre>My good news: [your text]</pre>',
            parse_mode='HTML'
        )


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
        await message.answer('ru: Спасибо, что оставил сообщение!\n\nen: Thank you for leaving a message!')
    else:
        await message.answer(
            'ru: Пожалуйста, введите сообщение в формате:\n'
            '<pre>Мое послание: [ваш текст]</pre>\n\n'
            'en: Please, enter the message in the format:\n'
            '<pre>My message: [your text]</pre>',
            parse_mode='HTML'
        )


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
