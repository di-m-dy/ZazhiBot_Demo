# ZazhiBot: README.md

Choose the documentation language:
- [Русский](README.md)
- [English](README_EN.md)

## Project Description

**ZazhiBot** is a social Telegram bot developed on the aiogram platform during the pandemic. The project is an extension of the **“Zazhivoe”** initiative, which brings together people with mental differences and neurotypical participants for collaborative creative work. Participants of the project create theatrical performances, art objects, dance, and other types of performances together.

### Main Idea

The primary goal of the bot is to showcase the peculiarities of communication with neurodivergent individuals. Often, it can be challenging to maintain a conversation on a specific topic: attention drifts, and the conversation veers towards topics interesting to the interlocutor or random facts. To create the bot, project participants observed each other closely, recording frequent responses and preferred topics. The collected data was integrated into the bot’s database, which uses these “live” phrases to respond to user messages.

### Additional Ideas

During creative events, project participants worked on various topics using interviews as one of the immersion methods. The accumulated responses and reflections were integrated into the bot's functionality, allowing users to discuss topics such as time, dreams, and others, regularly added to the database. For example, the "paintings and films" topic is implemented in a quiz format where users need to guess the correct answer based on the participant’s description. The "growing up" topic is presented as an audio podcast based on James Barrie's book "Peter Pan."

### Project Goal

**The goal of ZazhiBot** is to destigmatize people with mental differences. The project emphasizes that communication is always possible when both parties desire it.

## How to Use the Bot

This code is intended to demonstrate the bot's logic. All data and media are replaced with demo versions. If this logic suits your project, you can use this code as a foundation for your bot.

### Bot Features

#### 1. Message Handler on Prepared Topics: Dreams, Time
- Selects a random message from the database on the topic.

#### 2. Good News Handler
- Returns a random “good news” from the database.
- Allows users to submit their own “good news,” which is added to the database.

#### 3. Quiz on "Paintings and Films"
_Guess a movie frame or painting based on a text description or a photograph where participants recreate the pose of the frame or painting._
- The bot sends an image question and answer options as a poll.
- After answering, the bot sends the result as the original image.

#### 4. Offers Users to Listen to the Audio Fairy Tale "Peter Pan."
_Audio fairy tale based on James Barrie's book "Peter Pan," recorded by project participants._
- The bot sends an audio file of the fairy tale.

#### 5. Favorite Phrases of Project Participants
_For requests that do not fall under a specific handler, the bot sends a favorite/typical phrase from one of the project participants. All these phrases are stored in a separate database table._

**_! Request options are stored in the ```phrases``` module and can be modified according to your needs!_**

**_! The bot uses `file_id` for all media involved. The bot writes `file_id` of files to the database during operation. All necessary files are in the `static` directory._**

### How to Run the Bot

1. Clone the repository to your computer.
2. Install the dependencies using `pip install -r requirements.txt`.
3. Create a `.env` file in the project's root directory and add the environment variables:
    ```
    BOT_TOKEN=your_bot_token
    ADMIN_ID=your_admin_id
    ```
4. Rename the file `db/zazhibot_example.db` to `db/zazhibot.db` or copy and rename the copy.
5. Run the bot using `python main.py`.
6. Open Telegram and find the bot by the name you specified during creation.

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

## Support and Collaboration

This bot does not contain anything innovative.

The importance lies in the idea itself of how a simple pet project (which started as a way to learn the basics of the `aiogram` library) can become a modest but significant social project.

I would be happy if anyone finds useful:
- the **idea** of social projects
- my **code** for those who are also just getting acquainted with aiogram

## Links

**Instagram:** [Zazhivoe Project](http://www.instagram.com/zazhivoe_zarisovki)

Telegram Bot: [ZazhiBot](https://t.me/zazhi_bot)