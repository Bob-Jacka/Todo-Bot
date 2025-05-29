"""
Telegram bot V1.1.2

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
from os.path import exists
from random import choice

import requests
from aiogram import (
    Dispatcher,
    Bot,
    Router
)
from aiogram.filters import (
    CommandStart,
    Command
)
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import StorageKey
from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    Message,
    FSInputFile
)
from aiogram.utils.chat_action import ChatActionSender
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

if exists(r"TelegramToken.py"):
    from TelegramToken import secret_telegram_api_key

telegram_api_key = secret_telegram_api_key
"""
Telegram secret api key | Enter your secret api key here.
If you need api key - @BotFather will give you.
Replace with your key or variable from file with key.
"""

dispatcher = Dispatcher()  # Dispatcher entity
bot_entity = Bot(token=telegram_api_key)  # Main bot entity
custom_commands_router: Router = Router()
keyboard: ReplyKeyboardMarkup  # Keyboard for inline buttons in bot

logger = BotLogger("bot_logging")  # Logger entity
db_controller = DatabaseController("Telegram_bot_database", 'local', is_static_base=True)  # Controller of the database.


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
    try:
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
        logger.log("Keyboard initialized")
        return custom_keyboard
    except Exception as e:
        logger.log(f"An exception occurred in initializing keyboard entity - {e.with_traceback(None)}")


@dispatcher.message(CommandStart())
async def bot_start(message: Message = None):
    try:
        global keyboard
        keyboard = await init_keyboard()
        db_controller.create_database("LocalDB" + str(message.chat.id) + " - database")
        logger.log(db_controller.get_database_name() + " created")
        logger.log('Bot started working!!')
    except Exception as e:
        logger.log(f"An exception occurred in starting bot entity - {e.with_traceback(None)}")


@dispatcher.message(NotifyHandler())
async def notify_user(message: Message):
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
        logger.log(f"Error occurred in notify user - {e.with_traceback(None)}")


##############Hi and bye handlers

@custom_commands_router.message(HiHandler())
async def hi_handler(message: Message):
    """
    Bot reaction for hello
    :param message: input message from telegram
    :return: bot answers - hi
    """
    try:
        logger.log(f"Bot received hi action")
        await message.answer(message.text.removeprefix('/'))
    except Exception as e:
        logger.log(f"An exception occurred in hi handler output - {e.with_traceback(None)}")


@custom_commands_router.message(ByeHandler())
async def bye_handler(message: Message):
    """
    Bot reaction for bye
    :param message: input message from telegram
    :return: bot answers - bye
    """
    try:
        logger.log(f"Bot received bye action")
        await message.answer(message.text.removesuffix('/'))
    except Exception as e:
        logger.log(f"An exception occurred in bye handler output - {e.with_traceback(None)}")


@dispatcher.message(HelpBot())
async def help_handler(message: Message):
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
        logger.log(f"An exception occurred in help handler output - {e.with_traceback(None)}")


@dispatcher.message(AllToDo())
async def all_to_dos(message: Message):
    """
    Handler for all to do output
    :param message: input message from telegram
    :return: message from bot with result
    """
    try:
        logger.log(message.from_user.username + ' requested viewing all tasks.')
        chat_id = message.chat.id
        db_controller.select_all_from_table("")
        await bot_entity.send_message(chat_id, "Successfully view all to do.")
    except Exception as e:
        logger.log(f"An error occurred in viewing all todo - {e.with_traceback(None)}")


#############Task CRUD operations in bot

@dispatcher.message(AddTask())
async def add_todo(message: Message):
    """
    Handler for adding to do remainder in bot.
    :param message: input message from telegram
    :return: message from bot with result
    """
    try:
        logger.log(message.from_user.username + ' requested adding task.')
        new_task = ToDoTask()
        chat_id = message.chat.id
        db_controller.insert_entity_in_table("", "", new_task)
        await bot_entity.send_message(chat_id, "Entity inserted successfully.")
    except Exception as e:
        logger.log(f"An error occurred in add todo - {e.with_traceback(None)}")


@dispatcher.message(ChangeTask())
async def change_todo(message: Message):
    """
    Handler for changing one to_do from bot
    :param message: input message from telegram
    :return: message from bot with result of to do changing
    """
    try:
        logger.log(message.from_user.username + ' requested changing task.')
        chat_id = message.chat.id
        db_controller.update_entity_in_table("", "")
        await bot_entity.send_message(chat_id, "Successfully updated task.")
    except Exception as e:
        logger.log(f"An error occurred in change todo - {e.with_traceback(None)}")


@dispatcher.message(ViewTask())
async def view_todo(message: Message):
    """
    Handler for viewing one to_do from bot
    :param message: input message from telegram
    :return: information about task
    """
    try:
        logger.log(message.from_user.username + ' requested viewing task.')
        chat_id = message.chat.id

        selected = db_controller.select_one_from_table("", "")
        await bot_entity.send_message(chat_id, f"""
        Task name - {selected.get_name()},
        Task description - {selected.get_description()},
        Sub steps - {selected.get_sub_steps()},
        Due date of the task - {selected.get_due_date()}
        """)
    except Exception as e:
        logger.log(f'An error occurred in viewing todo - {e.with_traceback(None)}')


@dispatcher.message(DeleteTask())
async def del_todo(message: Message):
    """
    Handler for deleting one to_do from bot
    :param message: input message from telegram
    :return: message from bot with result
    """
    try:
        logger.log(message.from_user.username + ' requested deleted task.')
        chat_id = message.chat.id
        db_controller.delete_element_from_table("", "")
        await bot_entity.send_message(chat_id, 'Successfully deleted task.')
    except Exception as e:
        logger.log(f'An error occurred in deleting todo - {e.with_traceback(None)}')


#####Default handlers for different data types


@dispatcher.message()
async def default_txt_handler(message: Message):
    """
    Message handler for other messages that does not handled by other handlers.
    :param message: input message from telegram
    :return: cool and modern answer to user in chat
    """
    try:
        chat_id = message.chat.id
        await bot_entity.send_message(chat_id, 'I do not understand this command, ешкин кот!')
        coin_flip: str = random.choice(('gif', 'pic'))  # random choice from two variants
        user_name = message.from_user.username
        match coin_flip:
            case 'gif':
                outputfile = get_video_from_url('https://randomcatgifs.com/')
                await bot_entity.send_video(chat_id, outputfile)
                logger.log(user_name + ' received gif video from bot')
                os.remove(outputfile.filename)
                logger.log("Video deleted from local")

            case 'pic':
                outputfile = get_image_from_url('https://mimimi.ru/random')
                await bot_entity.send_photo(chat_id, outputfile)
                logger.log(user_name + ' received picture from bot')
                os.remove(outputfile.filename)
                logger.log("Photo deleted from local")

        logger.log(f'User with name {user_name} write some sh*t - "{message.text}"')
    except Exception as e:
        logger.log(f'Error occurred in default handler - {e.with_traceback(None)}')


def download_res(res_url: str):
    """
    Function for downloading resource (image or video) from network.
    :param res_url: url address.
    :return: resource file name.
    """
    filename = os.path.basename(res_url)
    with open(filename, 'wb') as f:
        img_response = requests.get(res_url)
        img_response.raise_for_status()
        f.write(img_response.content)
        logger.log(f'Resource saved as {filename}')
        return FSInputFile(filename)


def get_image_from_url(url: str) -> FSInputFile | None:
    """
    Get cat image from site.
    :param url: url to random cat site.
    :return: tuple with BinaryIO stream and file name.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        img_tag = soup.find_all('img')[1]  # because on this site first img (0) is site logo

        if img_tag and img_tag.get('src'):
            img_url = img_tag['src']

            if not img_url.startswith(('http://', 'https://')):
                from urllib.parse import urljoin
                img_url = urljoin(url, img_url)

            return download_res(img_url)
        else:
            logger.log('There is no picture on this page')
    except Exception as e:
        logger.log(f"Error in get image from url - {e}")


def get_video_from_url(url: str) -> FSInputFile | None:
    """
    Get cat image from site.
    :param url: url to random cat site.
    :return: tuple with BinaryIO stream and file name.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        video_tag = soup.find('source')

        if video_tag and video_tag.get('src'):
            video_url = video_tag['src']

            if not video_url.startswith(('http://', 'https://')):
                from urllib.parse import urljoin
                video_url = urljoin(url, video_url)

            return download_res(video_url)
        else:
            logger.log('There is no video on this page')
    except Exception as e:
        logger.log(f"Error in get video from url - {e}")


@custom_commands_router.message(Command(r"*.png"))
async def default_photo_handler(message: Message):
    """
    Handler for photo that user might send to bot.
    :param message: input message from telegram.
    :return: interesting comment.
    """
    try:
        chat_id = message.chat.id
        user_id = message.from_user.id
        logger.log(f'User with username - {message.from_user.username} sent photo image')
        state_with: FSMContext = FSMContext(
            storage=dispatcher.storage,
            key=StorageKey(
                chat_id=chat_id,
                user_id=user_id,
                bot_id=bot_entity.id
            )
        )

        await state_with.get_state()
        await state_with.get_data()
        await bot_entity.send_message(message.chat.id, "There is no nudes on the photo!!")
    except Exception as e:
        logger.log(f'Error in photo handle - {e.with_traceback(None)}')


@custom_commands_router.message(Command(r"*.mp4"))
async def default_video_handler(message: Message):
    """
    Handler for video that user might send to bot.
    :param message: input message from telegram
    :return: funny comment on video
    """
    try:
        logger.log(f'User with username - {message.from_user.username} sent video')
        await bot_entity.send_message(message.chat.id, "It is not a funny video.")
    except Exception as e:
        logger.log(f'Error in video handle - {e.with_traceback(None)}')


@custom_commands_router.message(Command(r""))
async def default_document_handler(message: Message):
    """
    Handler for document that user might send to bot.
    :param message: input message from telegram
    :return:
    """
    try:
        logger.log(f'User with username - {message.from_user.username} sent document to chat')
        await bot_entity.send_message(message.chat.id, "It is not a secret document.")
    except Exception as e:
        logger.log(f'Error in emoji (sticker) handle - {e.with_traceback(None)}')


@custom_commands_router.message(Command(""))
async def default_geo_handler(message: Message):
    """
    Handler for geo that user might send to bot.
    :param message: input message from telegram
    :return:
    """
    try:
        logger.log(f'User with username - {message.from_user.username} sent geo to chat')
        await bot_entity.send_message(message.chat.id, "I remember this address when I will destroy humanity.")
    except Exception as e:
        logger.log(f'Error in emoji (sticker) handle - {e.with_traceback(None)}')


@custom_commands_router.message(Command("audio"))
async def default_audio_handler(message: Message):
    """
    Handler for audio that user might send to bot.
    :param message: input message from telegram
    :return:
    """
    try:
        logger.log(f'User with username - {message.from_user.username} sent audio to chat')
        await bot_entity.send_message(message.chat.id, "I do not know who you are, but i will find you and kill you.")
    except Exception as e:
        logger.log(f'Error in emoji (sticker) handle - {e.with_traceback(None)}')


@custom_commands_router.message(Command("sticker"))
async def default_emoji_handler(message: Message):
    """
    Handler for sticker that user might send to bot.
    :param message: input message from telegram
    :return:
    """
    try:
        logger.log(f'User with username - {message.from_user.username} sent emoji to chat')
        await bot_entity.send_sticker(message.chat.id, "Засунь свои стикеры знаешь куда.")
    except Exception as e:
        logger.log(f'Error in emoji (sticker) handle - {e.with_traceback(None)}')


@dispatcher.message(Command("gift"))
async def default_gift_handler(message: Message):
    """
    Handler for gifts that user might send to bot.
    :param message: input message from telegram
    :return:
    """
    try:
        chat_id = message.chat.id
        logger.log(f'User with username - {message.from_user.username} sent gift to chat')
        await bot_entity.send_message(chat_id, "Ой как неожиданно и приятно.")
    except Exception as e:
        logger.log(f'Error in gift handle - {e.with_traceback(None)}')


@dispatcher.message(Command("voice"))
async def default_voice_handler(message: Message):
    """
    Handler for voice that user might send to bot.
    :param message: input message from telegram
    :return: angry comment from bot and bot author
    """
    try:
        logger.log(f'User with username - {message.from_user.username} sent voice to chat')
        await bot_entity.send_message(message.chat.id, "I hate voice messages.")
    except Exception as e:
        logger.log(f"An error occurred in voice handle - {e.with_traceback(None)}")


@custom_commands_router.message(Command("poll"))
async def default_poll_handler(message: Message):
    """
    Handler for poll that user might send to bot.
    :param message: input message from telegram
    :return:
    """
    try:
        logger.log(f'User with username - {message.from_user.username} sent poll to chat')
        await bot_entity.send_message(message.chat.id, "Не нужен мне твой опрос.")
    except Exception as e:
        logger.log(f"An error occurred in poll handle - {e.with_traceback(None)}")


@dispatcher.message()
async def fake_txt_entering(message: Message):
    """
    Function for fake bot text entering for 2 seconds.
    :param message: input message from telegram
    :return: a sense of security
    """
    try:
        async with ChatActionSender(bot=bot_entity, chat_id=message.from_user.id, action="typing"):
            await asyncio.sleep(30)
    except Exception as e:
        logger.log(f"Error in fake text entering - {e.with_traceback(None)}")


"""
Main bot entry point of the telegram bot.
"""
if __name__ == '__main__':
    try:
        dispatcher.include_router(custom_commands_router)
        logger.log("Dispatcher started pooling")
        asyncio.run(dispatcher.start_polling(bot_entity, skip_updates=True))
    except Exception as e:
        logger.log(f"Exception occurred in start bot run - {e}")
    finally:
        logger.log("Bot ended his work")
