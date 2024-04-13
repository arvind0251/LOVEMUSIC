from pyrogram import filters
from pyrogram.types import Message
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from LOVEMUSIC import app
from LOVEMUSIC.core.call import LOVE
from LOVEMUSIC.utils.database import is_music_playing, music_on
from LOVEMUSIC.utils.decorators import AdminRightsCheck
from LOVEMUSIC.utils.inline import close_markup
from config import BANNED_USERS


@app.on_message(filters.command(["resume", "cresume"]) & filters.group & ~BANNED_USERS)
@AdminRightsCheck
async def resume_com(cli, message: Message, _, chat_id):
    if await is_music_playing(chat_id):
        return await message.reply_text(_["admin_3"])
    await music_on(chat_id)
    await LOVE.resume_stream(chat_id)
    buttons_resume = [
        [
            
            InlineKeyboardButton(
                text="sᴋɪᴘ", callback_data=f"ADMIN Skip|{chat_id}"
            ),
            InlineKeyboardButton(
                text="sᴛᴏᴘ", callback_data=f"ADMIN Stop|{chat_id}"
            ),
        ],
        [
            InlineKeyboardButton(
                text="ᴘᴀᴜsᴇ",
                callback_data=f"ADMIN Pause|{chat_id}",
            ),
        ]
    ]
    await message.reply_text(
        _["admin_4"].format(message.from_user.mention), reply_markup=InlineKeyboardMarkup(buttons_resume)
    )
