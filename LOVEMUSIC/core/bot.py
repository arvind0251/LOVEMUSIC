import asyncio
import threading

import uvloop
from flask import Flask
from pyrogram import Client, idle, errors
from pyrogram.enums import ChatMemberStatus
from pyrogram.types import (
    BotCommand,
    BotCommandScopeAllChatAdministrators,
    BotCommandScopeAllGroupChats,
    BotCommandScopeAllPrivateChats,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

import config
from logging import getLogger

LOGGER = getLogger(__name__)

uvloop.install()

# Flask app initialize
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running"

def run():
    app.run(host="0.0.0.0", port=8000, debug=False)

# LOVEBot Class
class LOVEBot(Client):
    def __init__(self):
        LOGGER.info("Starting Bot")
        super().__init__(
            "VIPMUSIC",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            bot_token=config.BOT_TOKEN,
        )

    async def start(self):
        await super().start()
        get_me = await self.get_me()
        self.username = get_me.username
        self.id = get_me.id
        self.name = f"{get_me.first_name} {get_me.last_name or ''}"
        self.mention = get_me.mention

        button = InlineKeyboardMarkup(
            [[InlineKeyboardButton(text="๏ ᴀᴅᴅ ᴍᴇ ɪɴ ɢʀᴏᴜᴘ ๏", url=f"https://t.me/{self.username}?startgroup=true")]]
        )

        if config.LOG_GROUP_ID:
            try:
                await self.send_photo(
                    config.LOG_GROUP_ID,
                    photo=config.START_IMG_URL,
                    caption=f"🎉 Bot Started: {self.name} (@{self.username})",
                    reply_markup=button,
                )
            except errors.ChatWriteForbidden:
                LOGGER.error("Bot cannot write to the log group.")
                try:
                    await self.send_message(config.LOG_GROUP_ID, "🎉 Bot Started!", reply_markup=button)
                except Exception as e:
                    LOGGER.error(f"Failed to send message in log group: {e}")
            except Exception as e:
                LOGGER.error(f"Unexpected error: {e}")

        if config.SET_CMDS:
            try:
                await self.set_bot_commands(
                    commands=[BotCommand("start", "Start the bot"), BotCommand("help", "Get the help menu"), BotCommand("ping", "Check if the bot is alive")],
                    scope=BotCommandScopeAllPrivateChats(),
                )
                await self.set_bot_commands(
                    commands=[BotCommand("play", "Start playing requested song"), BotCommand("stop", "Stop the current song")],
                    scope=BotCommandScopeAllGroupChats(),
                )
                await self.set_bot_commands(
                    commands=[BotCommand("admin", "Admin commands"), BotCommand("settings", "Get the settings")],
                    scope=BotCommandScopeAllChatAdministrators(),
                )
            except Exception as e:
                LOGGER.error(f"Failed to set bot commands: {e}")

        if config.LOG_GROUP_ID:
            try:
                chat_member_info = await self.get_chat_member(config.LOG_GROUP_ID, self.id)
                if chat_member_info.status != ChatMemberStatus.ADMINISTRATOR:
                    LOGGER.error("Bot is not an Admin in Logger Group")
            except Exception as e:
                LOGGER.error(f"Error checking bot status: {e}")

        LOGGER.info(f"MusicBot Started as {self.name}")

# Define the async boot function
async def anony_boot():
    bot = LOVEBot()
    await bot.start()
    await idle()

if __name__ == "__main__":
    LOGGER.info("Starting Flask server...")

    # Start Flask server in a new thread
    t = threading.Thread(target=run)
    t.daemon = True
    t.start()

    LOGGER.info("Starting LOVEBot...")

    # Run the bot using asyncio event loop
    asyncio.get_event_loop().run_until_complete(anony_boot())

    LOGGER.info("Stopping LOVEBot...")
