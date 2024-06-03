"""
Module for handlers for admin related requests
"""

# en: Message for the start command / ru: Сообщение для команды start
START = ('en: Привет!\n\n'
         'Это бот <b>проекта «ЗАЖИВОЕ»</b>\n\n'
         'В этом боте мы хотим сохранить <b>неповторимые</b> мысли его участников '
         'и передать их манеру вести беседу - <b>всегда непредсказуемую</b>\n\n'
         'Пиши /help, чтобы узнать, что я умею\n\n'
         'Ищи нас в инстаграм:\n'
         '<a href="http://www.instagram.com/zazhivoe_zarisovki">Проект «ЗАЖИВОЕ»</a>\n\n\n'
         'en: Hello!\n\n'
         'This is a bot of the <b>«ZAZHIVOE» project</b>\n\n'
         'In this bot, we want to save the <b>unique</b> thoughts of its participants '
         'and convey their manner of conversation - <b>always unpredictable</b>\n\n'
         'Write /help to find out what I can do\n\n'
         'Find us on Instagram:\n'
         '<a href="http://www.instagram.com/zazhivoe_zarisovki">Project «ZAZHIVOE»</a>')


# en: Message for the help command / ru: Сообщение для команды help
HELP = '1. Можем <b>поиграть</b> - пиши:\n' \
       '<pre>Поиграем?</pre>\n\n' \
       '2. Хочешь <b>услышать</b> историю о Питере Пэне - пиши:\n' \
       '<pre>Питер Пэн</pre>\n\n' \
       '3. Можем поговорить о <b>времени</b>.\n\n' \
       '4. Можем поговорить о <b>снах</b>.\n\n' \
       '5. Если хочешь узнать <b>хорошую новость</b> - пиши:\n' \
       '<pre>Расскажи хорошую новость</pre>\n\n' \
       '6. Можешь написать свою хорошую новость:\n' \
       '<pre>Моя хорошая новость: [хорошая новость]</pre>\n\n' \
       '7. Можешь оставить <b>сообщение</b> для участников проекта. Ребята обязательно прочитают. Пиши:\n' \
       '<pre>Мое послание: [все, что хочется сказать]</pre>\n\n\n' \
       'Всё позабыл - /help\n'

HELP_EN = '1. We can <b>play</b> - write:\n' \
          '<pre>How about to play?</pre>\n\n' \
          '2. Do you want to hear the story of Peter Pan - write:\n' \
          '<pre>Peter Pan</pre>\n\n' \
          '3. We can talk about <b>time</b>.\n\n' \
          '4. We can talk about <b>dreams</b>.\n\n' \
          '5. If you want to know <b>good news</b> - write:\n' \
          '<pre>Tell me good news</pre>\n\n' \
          '6. You can write your good news:\n' \
          '<pre>My good news: [good news]</pre>\n\n' \
          '7. You can leave a <b>message</b> for the project participants. The guys will definitely read it. Write:\n' \
          '<pre>My message: [everything you want to say]</pre>\n\n\n' \
          'Forgot everything - /help\n'

# en: Message for the empty database / ru: Сообщение для пустой базы данных
EMPTY_DB = 'ru: База данных пуста! \n en: The database is empty!'
# en: Message for the word that cannot be pronounced / ru: Сообщение для слова, которое нельзя произносить
HATE = 'en: Don\'t say "let\'s"!!!\nru: Не говори давай!!!'
