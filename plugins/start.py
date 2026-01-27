import random
import humanize
from Script import script
from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from info import URL, LOG_CHANNEL, SHORTLINK, FORCE_SUB_CHANNEL
from urllib.parse import quote_plus
from TechVJ.util.file_properties import get_name, get_hash, get_media_file_size
from TechVJ.util.human_readable import humanbytes
from database.users_chats_db import db
from utils import temp, get_shortlink


# -------- FORCE SUB FUNCTION --------
async def is_subscribed(client, user_id):
    try:
        member = await client.get_chat_member(FORCE_SUB_CHANNEL, user_id)
        if member.status in ["member", "administrator", "creator"]:
            return True
    except:
        return False
    return False


# -------- START COMMAND --------
@Client.on_message(filters.command("start") & filters.incoming)
async def start(client, message):

    # Force Subscribe Check
    if not await is_subscribed(client, message.from_user.id):
        join_btn = InlineKeyboardMarkup(
            [InlineKeyboardButton(
    "🔔 Join Channel",
    url="https://t.me/SGBACKUP"
)]
        )
        await message.reply_text(
            text=(
                "⚠️ <b>Access Denied!</b>\n\n"
                "Please join our channel first to use this bot.\n\n"
                "After joining, come back and press /start again."
            ),
            reply_markup=join_btn,
            parse_mode=enums.ParseMode.HTML
        )
        return

    if not await db.is_user_exist(message.from_user.id):
        await db.add_user(message.from_user.id, message.from_user.first_name)
        await client.send_message(
            LOG_CHANNEL,
            script.LOG_TEXT_P.format(message.from_user.id, message.from_user.mention)
        )

    rm = InlineKeyboardMarkup(
        [[InlineKeyboardButton("✨ Update Channel", url="https://t.me/SGBACKUP")]]
    )

    await client.send_message(
        chat_id=message.from_user.id,
        text=script.START_TXT.format(
            message.from_user.mention,
            temp.U_NAME,
            temp.B_NAME
        ),
        reply_markup=rm,
        parse_mode=enums.ParseMode.HTML
    )


# -------- FILE / VIDEO HANDLER --------
@Client.on_message(filters.private & (filters.document | filters.video))
async def stream_start(client, message):

    # Force Subscribe Check (again)
    if not await is_subscribed(client, message.from_user.id):
        join_btn = InlineKeyboardMarkup(
            [[InlineKeyboardButton("🔔 Join Channel", url=f"https://t.me/{FORCE_SUB_CHANNEL.replace('@','')}")]]
        )
        await message.reply_text(
            text=(
                "⚠️ <b>Access Denied!</b>\n\n"
                "Please join our channel first to generate links.\n\n"
                "Join the channel and try again."
            ),
            reply_markup=join_btn,
            parse_mode=enums.ParseMode.HTML
        )
        return

    file = getattr(message, message.media.value)
    filesize = humanize.naturalsize(file.file_size)
    fileid = file.file_id
    user_id = message.from_user.id
    username = message.from_user.mention

    log_msg = await client.send_cached_media(
        chat_id=LOG_CHANNEL,
        file_id=fileid,
    )

    fileName = quote_plus(get_name(log_msg))

    if SHORTLINK is False:
        stream = f"{URL}watch/{log_msg.id}/{fileName}?hash={get_hash(log_msg)}"
        download = f"{URL}{log_msg.id}/{fileName}?hash={get_hash(log_msg)}"
    else:
        stream = await get_shortlink(
            f"{URL}watch/{log_msg.id}/{fileName}?hash={get_hash(log_msg)}"
        )
        download = await get_shortlink(
            f"{URL}{log_msg.id}/{fileName}?hash={get_hash(log_msg)}"
        )

    rm = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("🖥 Stream", url=stream),
                InlineKeyboardButton("📥 Download", url=download)
            ]
        ]
    )

    msg_text = (
        "<i><u>Your Link Generated!</u></i>\n\n"
        "<b>📂 File Name:</b> <i>{}</i>\n\n"
        "<b>📦 File Size:</b> <i>{}</i>\n\n"
        "<b>📥 Download:</b> <i>{}</i>\n\n"
        "<b>🖥 Watch:</b> <i>{}</i>\n\n"
        "<b>🚸 Note:</b> Links will not expire until deleted."
    )

    await message.reply_text(
        text=msg_text.format(
            get_name(log_msg),
            humanbytes(get_media_file_size(message)),
            download,
            stream
        ),
        quote=True,
        disable_web_page_preview=True,
        reply_markup=rm
    )
