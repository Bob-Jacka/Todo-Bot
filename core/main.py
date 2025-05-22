"""
Telegram bot V1.0.0

You can find this bot in telegram, just enter bot name.
Telegram bot name - @GoalGetter_and_DailyDoBot_bot

Knows all about your tasks and your secret desires...
Will notify you about your tasks and delete task if you not want to complete it.
Work only if I start python execution, or you can clone this repository with telegram api key and own your bot.

author - cupcake_wrld
"""

import asyncio
import os
import random
from random import choice

import requests
from aiogram import (
    types,
    Dispatcher,
    Bot
)
from aiogram.enums import ContentType
from aiogram.filters import CommandStart
from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton, InputFile
)
from bs4 import BeautifulSoup

from core.entities.BotLogger import BotLogger
from core.entities.DatabaseController import DatabaseController
from core.entities.ToDoTask import ToDoTask
from core.handlers.OtherHandlers.ByeHandler import ByeHandler
from core.handlers.OtherHandlers.HelpBot import HelpBot
from core.handlers.OtherHandlers.HiHander import HiHandler
from core.handlers.OtherHandlers.NotifyUser import NotifyHandler
from core.handlers.ToDo_handlers.AddTask import AddTask
from core.handlers.ToDo_handlers.AllToDo import AllToDo
from core.handlers.ToDo_handlers.BotCommands import (
    dirty_words,
    commands
)
from core.handlers.ToDo_handlers.ChangeTask import ChangeTask
from core.handlers.ToDo_handlers.DeleteTask import DeleteTask
from core.handlers.ToDo_handlers.ViewTask import ViewTask

telegram_api_key = ''  # Telegram secret api key
dispatcher = Dispatcher()  # Dispatcher entity
bot_entity = Bot(token=telegram_api_key)  # Main bot entity
keyboard: ReplyKeyboardMarkup  # Keyboard for inline buttons in bot

logger = BotLogger("bot_logging")  # Logger entity
base_controller = DatabaseController("Telegram_bot_database", 'local', is_static_base=True)  # Controller of the database.


def random_dirty_word() -> str:
    """
    Function that will hurt you
    :return: random dirty word from tuple
    """
    rand = choice(dirty_words)
    return rand


async def init_keyboard():
    """
    Initializes bot keyboard with predefined buttons.
    Every button responsible for CRUD operation in database.
    :return: initialized keyboard
    """
    button1 = KeyboardButton(text="View to do")
    button2 = KeyboardButton(text="Delete task")
    button3 = KeyboardButton(text="Update task")
    button4 = KeyboardButton(text="Add task")
    buttons: list[list] = list()
    buttons.append(list())
    buttons[0].append(button1)
    buttons[0].append(button2)
    buttons[0].append(button3)
    buttons[0].append(button4)
    custom_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=buttons)
    logger.log("Keyboard initialized.")
    return custom_keyboard


@dispatcher.message(CommandStart())
async def bot_start(message: types.Message = None):
    try:
        global keyboard
        keyboard = init_keyboard()
        base_controller.create_database(str(message.chat.id) + " - database")
        logger.log(base_controller.get_base_name() + " created.")
        logger.log('Bot started working!!')
    except Exception as e:
        logger.log(f"An exception occurred in starting bot entity - {e}")


@dispatcher.message(NotifyHandler())
async def notify_user(message: types.Message):
    """
    Notify user about something event in his life
    :param message: input message from telegram
    :return: dirty word to user
    """
    try:
        logger.log("User notification occurred.")
        chat_id = message.chat.id
        await bot_entity.send_message(chat_id, random_dirty_word())
    except Exception as e:
        logger.log(f"Error occurred in notify user - {e}.")


##############Hi and bye handlers

@dispatcher.message(HiHandler())
async def hi_handler(message: types.Message):
    """
    Bot reaction for hello
    :param message: input message from telegram
    :return: bot answers - hi
    """
    logger.log("Bot received hi action.")
    await message.answer(message.text.removeprefix('/'))


@dispatcher.message(ByeHandler())
async def bye_handler(message: types.Message):
    """
    Bot reaction for bye
    :param message: input message from telegram
    :return: bot answers - bye
    """
    logger.log("Bot received bye action.")
    await message.answer(message.text.removesuffix('/'))


@dispatcher.message(HelpBot())
async def help_handler(message: types.Message):
    """
    Handler for help command
    :param message: input message from telegram
    :return: help menu
    """
    try:
        logger.log(message.from_user.username + ' requested - get help menu.')
        chat_id = message.chat.id
        await bot_entity.send_message(chat_id, """
            This bot is needed when you have some important tasks.
            1) You can add, delete, view and change task
            2) Bot will notify you if it is time to action
            3) three is too many points in help menu, you know
            """)
        await bot_entity.send_message(chat_id, "Available list of bot commands:")
        for command in commands.values():
            await bot_entity.send_message(chat_id, command)
    except Exception as e:
        logger.log(f"An exception occurred in help handler output - {e}.")


@dispatcher.message(AllToDo())
async def all_to_dos(message: types.Message):
    """
    Handler for all to do output
    :param message: input message from telegram
    :return: message from bot with result
    """
    try:
        logger.log(message.from_user.username + ' requested viewing all tasks.')
        chat_id = message.chat.id
        base_controller.select_all_from_table("")
        await bot_entity.send_message(chat_id, "Successfully view all to do.")
    except Exception as e:
        logger.log(f"An error occurred in viewing all todo - {e}.")


#############Task CRUD operations in bot

@dispatcher.message(AddTask())
async def add_todo(message: types.Message):
    """
    Handler for adding to do remainder in bot.
    :param message: input message from telegram
    :return: message from bot with result
    """
    try:
        logger.log(message.from_user.username + ' requested adding task.')
        new_task = ToDoTask()
        chat_id = message.chat.id
        base_controller.insert_entity_in_table("", "", new_task)
        await bot_entity.send_message(chat_id, "Entity inserted successfully.")
    except Exception as e:
        logger.log(f"An error occurred in add todo - {e}.")


@dispatcher.message(ChangeTask())
async def change_todo(message: types.Message):
    """
    Handler for changing one to_do from bot
    :param message: input message from telegram
    :return: message from bot with result of to do changing
    """
    try:
        logger.log(message.from_user.username + ' requested changing task.')
        chat_id = message.chat.id
        base_controller.update_entity_in_table("", "")
        await bot_entity.send_message(chat_id, "Successfully updated task.")
    except Exception as e:
        logger.log(f"An error occurred in change todo - {e}.")


@dispatcher.message(ViewTask())
async def view_todo(message: types.Message):
    """
    Handler for viewing one to_do from bot
    :param message: input message from telegram
    :return: information about task
    """
    try:
        logger.log(message.from_user.username + ' requested viewing task.')
        chat_id = message.chat.id

        selected = base_controller.select_one_from_table("", "")
        await bot_entity.send_message(chat_id, f"""
        Task name - {selected.get_name()},
        Task description - {selected.get_description()},
        Sub steps - {selected.get_sub_steps()},
        Due date of the task - {selected.get_due_date()}
        """)
    except Exception as e:
        logger.log(f'An error occurred in viewing todo - {e}.')


@dispatcher.message(DeleteTask())
async def del_todo(message: types.Message):
    """
    Handler for deleting one to_do from bot
    :param message: input message from telegram
    :return: message from bot with result
    """
    try:
        logger.log(message.from_user.username + ' requested deleted task.')
        chat_id = message.chat.id
        base_controller.delete_element_from_table("", "")
        await bot_entity.send_message(chat_id, 'Successfully deleted task.')
    except Exception as e:
        logger.log(f'An error occurred in deleting todo - {e}.')


#####Default handlers for different data types

@dispatcher.message(ContentType('text'))
async def default_txt_handler(message: types.Message):
    """
    Message handler for other messages
    :param message: input message from telegram
    :return: cool and modern answer to user in chat
    """
    try:
        chat_id = message.chat.id
        await bot_entity.send_message(chat_id, 'I do not understand this command, ешкин кот!')
        coin_flip: str = random.choice(('gif', 'pic'))
        match coin_flip:
            case 'gif':
                await bot_entity.send_video(chat_id, InputFile(get_video_from_url('https://randomcatgifs.com/')))
                logger.log(message.from_user.username + ' received gif from bot.')
            case 'pic':
                await bot_entity.set_chat_photo(chat_id, InputFile(get_image_from_url('https://mimimi.ru/random')))
                logger.log(message.from_user.username + ' received picture from bot.')

        logger.log(f'User with name {message.from_user.username} write some sh*t - {message.text}')
    except Exception as e:
        logger.log(f'Error occurred in default handler - {e}.')


def get_image_from_url(url: str):
    """
    Get cat image from site.
    :param url: url to random cat site.
    :return: image
    """
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    img_tag = soup.find('img')

    if img_tag and img_tag.get('src'):
        img_url = img_tag['src']

        if not img_url.startswith(('http://', 'https://')):
            from urllib.parse import urljoin
            img_url = urljoin(url, img_url)

        img_response = requests.get(img_url)
        img_response.raise_for_status()

        filename = os.path.basename(img_url)
        with open(filename, 'wb') as f:
            f.write(img_response.content)
            logger.log(f'Picture saved as {filename}.')
            return f
    else:
        logger.log('There is no picture on this page.')


def get_video_from_url(url: str):
    """
    Get cat image from site.
    :param url: url to random cat site.
    :return: image
    """
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    video_tag = soup.find('video')

    if video_tag and video_tag.get('src'):
        video_url = video_tag['src']

        if not video_url.startswith(('http://', 'https://')):
            from urllib.parse import urljoin
            video_url = urljoin(url, video_url)

        img_response = requests.get(video_url)
        img_response.raise_for_status()

        filename = os.path.basename(video_url)
        with open(filename, 'wb') as f:
            f.write(img_response.content)
            logger.log(f'Picture saved as {filename}.')
            return f
    else:
        logger.log('There is no picture on this page.')


@dispatcher.message(ContentType('photo'))
async def default_photo_handler(message: types.Message):
    """
    Handler for photo that user might send to bot.
    :param message: input message from telegram
    :return: interesting comment
    """
    logger.log(f'User with username - {message.from_user.username} sent photo image.')
    await bot_entity.send_message(message.chat.id, "There is no nudes on the photo!!.")


@dispatcher.message(ContentType('video'))
async def default_video_handler(message: types.Message):
    """
    Handler for video that user might send to bot.
    :param message: input message from telegram
    :return:
    """
    logger.log(f'User with username - {message.from_user.username} sent video.')
    await bot_entity.send_message(message.chat.id, "It is not a funny video.")


@dispatcher.message(ContentType('document'))
async def default_document_handler(message: types.Message):
    """
    Handler for document that user might send to bot.
    :param message: input message from telegram
    :return:
    """
    logger.log(f'User with username - {message.from_user.username} sent document to chat.')
    await bot_entity.send_message(message.chat.id, "It is not a secret document.")


@dispatcher.message(ContentType("geo"))
async def default_geo_handler(message: types.Message):
    """
    Handler for geo that user might send to bot.
    :param message: input message from telegram
    :return:
    """
    logger.log(f'User with username - {message.from_user.username} sent geo to chat.')
    await bot_entity.send_message(message.chat.id, "I remember this address when I will destroy humanity.")


@dispatcher.message(ContentType("audio"))
async def default_audio_handler(message: types.Message):
    """
    Handler for audio that user might send to bot.
    :param message: input message from telegram
    :return:
    """
    logger.log(f'User with username - {message.from_user.username} sent audio to chat.')
    await bot_entity.send_message(message.chat.id, "I do not know who you are, but i will find you and kill you.")


@dispatcher.message(ContentType("sticker"))
async def default_emoji_handler(message: types.Message):
    """
    Handler for sticker that user might send to bot.
    :param message: input message from telegram
    :return:
    """
    logger.log(f'User with username - {message.from_user.username} sent emoji to chat.')
    await bot_entity.send_sticker(message.chat.id, "")


@dispatcher.message(ContentType("gift"))
async def default_gift_handler(message: types.Message):
    """
    Handler for gifts that user might send to bot.
    :param message: input message from telegram
    :return:
    """
    logger.log(f'User with username - {message.from_user.username} sent gift to chat.')


@dispatcher.message(ContentType("voice"))
async def default_gift_handler(message: types.Message):
    """
    Handler for voice that user might send to bot.
    :param message: input message from telegram
    :return: angry comment from bot and bot author
    """
    logger.log(f'User with username - {message.from_user.username} sent voice to chat.')
    await bot_entity.send_message(message.chat.id, "I hate voice messages.")


@dispatcher.message(ContentType("poll"))
async def default_poll_handler(message: types.Message):
    """
    Handler for poll that user might send to bot.
    :param message: input message from telegram
    :return:
    """
    logger.log(f'User with username - {message.from_user.username} sent poll to chat.')
    await bot_entity.send_message(message.chat.id, "")


"""
Main bot entry point of the telegram bot.
"""
if __name__ == '__main__':
    try:
        asyncio.run(dispatcher.start_polling(bot_entity, skip_updates=True))
    except Exception as e:
        logger.log(f"Exception occurred in start bot run - {e}.")
    finally:
        logger.log("Bot ended his work.")
