# ЗажиБот: README.md

Выберите язык документации:
- [Русский](README.md)
- [English](README_EN.md)

## Описание проекта

**ЗажиБот** — это социальный Telegram-бот, разработанный на платформе aiogram в период пандемии. Проект стал продолжением инициативы **«Заживое»**, которая объединяет людей с ментальными особенностями и нормотипичных участников для совместной творческой работы. Участники проекта вместе создают театральные постановки, художественные объекты, танцевальные и другие виды перформансов.

### Главная идея

Основная цель бота — показать особенности общения с нейроотличными людьми. Часто бывает трудно поддерживать разговор по определённой теме: внимание ускользает, и разговор скатывается на темы, интересные собеседнику, или переходит к случайным фактам. Для создания бота участники проекта внимательно наблюдали друг за другом, записывая частые ответы и предпочтительные темы. Собранные данные были интегрированы в базу данных бота, который использует эти «живые» фразы для ответов на сообщения пользователей.

### Дополнительные идеи

В процессе творческих мероприятий участники проекта работали над различными темами, используя интервью как один из методов погружения. Накопленные ответы и размышления были интегрированы в функционал бота, позволяя пользователям обсуждать такие темы, как время, сны и другие, регулярно добавляемые в базу. Например, тема «картины и фильмы» реализована в формате викторины, где пользователи должны угадать правильный ответ по описанию участника. Тема «взросление» представлена в виде аудиоподкаста по книге Джеймса Барри «Питер Пэн».

### Цель проекта

**Целью ЗажиБота** является дестигматизация людей с ментальными особенностями. Проект подчёркивает, что общение возможно всегда, когда обе стороны этого желают.

## Как использовать бота

Этот код предназначен для демонстрации логики бота. Все данные и медиа заменены на демонстрационные. Если эта логика подходит для вашего проекта, вы можете использовать этот код как основу для своего бота.

### Что он умеет

#### 1. Обработчик сообщений на заготовленные темы: сны, время
- Выбирает рандомное сообщение из базы данных по теме
 
#### 2. Обработчик хороших новостей
- Возвращает рандомную «хорошую новость» из базы данных
- Можно отправить свою «хорошую новость» которая добавляется в базу данных

#### 3. Викторина по теме «картины и фильмы»
_Отгадать кадр из фильма или произведение живописи по текстовому описанию или по фотографии, на которой участники воспроизводят позу кадра или картины_
- Бот присылает изображение-вопрос и варианты ответов в виде опроса
- После ответа бот присылает результат в виде оригинала изображения

#### 4. Предлагает пользователю послушать аудио сказку «Питер Пэн».
_Аудио-сказка по мотивам книги Джеймса Барри «Питер Пэн», записанная участниками проекта_
- Бот присылает аудио-файл сказки

#### 5.  Любимые фразы участников проекта
_На те запросы, которые не попадают под обработчик, бот высылает любимую/типичную фразу одного из участников проекта. Все эти фразы хранятся в отдельной таблице базы данных_

**_! Варианты запросов хранятся в модуле ```phrases``` и могут быть изменены в соответствии с вашими потребностями !_**

**_! Бот использует `file_id` всех медиа, которые задействованы в боте. Бот прописывает `file_id` файлов в базу данных в процессе работы. Все необходимые файлы - в директории `static`._**


### Как запустить бота

1. Склонируйте репозиторий на свой компьютер.
2. Установите зависимости, используя `pip install -r requirements.txt`.
3. Создайте файл `.env` в корневой папке проекта и добавьте в него переменные окружения:
    ```
    BOT_TOKEN=your_bot_token
    ADMIN_ID=your_admin_id
    ```
4. Переименуйте файл `db/zazhibot_example.db` в `db/zazhibot.db`. Либо скопируйте его и переименуйте копию.
5. Запустите бота, используя `python main.py`.
6. Откройте Telegram и найдите бота по имени, который вы указали при создании.

### Requirements:
* aiofiles==23.2.1
* aiogram==3.6.0
* aiohttp==3.9.5
* aiosignal==1.3.1
* annotated-types==0.7.0
* attrs==23.2.0
* certifi==2024.2.2
* frozenlist==1.4.1
* idna==3.7
* magic-filter==1.0.12
* multidict==6.0.5
* pydantic==2.7.2
* pydantic_core==2.18.3
* python-dotenv==1.0.1
* typing_extensions==4.12.0
* yarl==1.9.4

## Поддержка и сотрудничество

В этом боте нет чего-то инновационного.

Здесь важна сама идея того, как можно из простого пет-проекта (который начинался ради изучения азов библиотеки `aiogram`) сделать скромный, но важный социальный проект.


Буду рад, если кому-то пригодится:
- сама **идея** социальных проектов
- мой **код** для тех, кто еще также только знакомится с aiogram

## Ссылки

**Инстаграм:** [проект «ЗаЖивое»](http://www.instagram.com/zazhivoe_zarisovki)

**Телеграм-бот:** [телеграм-бот «ЗаЖиБот»](https://t.me/zazhi_bot)