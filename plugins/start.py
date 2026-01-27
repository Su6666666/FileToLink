import humanize
from Script import script
from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from info import (
    URL, LOG_CHANNEL, SHORTLINK,
    FORCE_SUB_CHANNEL_ID, FORCE_SUB_CHANNEL_USERNAME
)
from urllib.parse import quote_plus
from TechVJ.util.file_properties import get_name, get_hash, get_media_file_size
from TechVJ.util.human_readable import humanbytes
from database.users_chats_db import db
from utils import temp, get_shortlink


# 🔒 FORCE SUB CHECK (SAFE METHOD)
async def force_sub_check(client, user_id):
    try:
        await client.send_message(FORCE_SUB_CHANNEL_ID, ".", disable_notification=True)
        return True
    except:
        return False


def join_message():
    return InlineKeyboardMarkup(
        [[
            InlineKeyboardButton(
                "🔔 Join Channel",
                url=f"https://t.me/{FORCE_SUB_CHANNEL_USERNAME}"
            )
        ]]
    )


@Client.on_message(filters.command("start") & filters.incoming)
async def start(client, message):

    if not await force_sub_check(client, message.from_user.id):
        await message.reply_text(
            "⚠️ **Access Denied!**\n\n"
            "Please join our channel first to use this bot.\n\n"
            "After joining, come back and press /start again.",
            reply_markup=join_message()
        )
        return

    if not await db.is_user_exist(message.from_user.id):
        await db.add_user(message.from_user.id, message.from_user.first_name)
        await client.send_message(
            LOG_CHANNEL,
            script.LOG_TEXT_P.format(message.from_user.id, message.from_user.mention)
        )

    rm = InlineKeyboardMarkup(
        [[InlineKeyboardButton("✨ Update Channel", url="https://t.me/sgbackup")]]
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


@Client.on_message(filters.private & (filters.document | filters.video))
async def stream_start(client, message):

    if not await force_sub_check(client, message.from_user.id):
        await message.reply_text(
            "⚠️ **Access Denied!**\n\n"
            "Please join our channel first to generate links.",
            reply_markup=join_message()
        )
        return

    file = getattr(message, message.media.value)

    log_msg = await client.send_cached_media(
        chat_id=LOG_CHANNEL,
        file_id=file.file_id,
    )

    name = quote_plus(get_name(log_msg))

    if not SHORTLINK:
        stream = f"{URL}watch/{log_msg.id}/{name}?hash={get_hash(log_msg)}"
        download = f"{URL}{log_msg.id}/{name}?hash={get_hash(log_msg)}"
    else:
        stream = await get_shortlink(f"{URL}watch/{log_msg.id}/{name}?hash={get_hash(log_msg)}")
        download = await get_shortlink(f"{URL}{log_msg.id}/{name}?hash={get_hash(log_msg)}")

    rm = InlineKeyboardMarkup(
        [[
            InlineKeyboardButton("🖥 Stream", url=stream),
            InlineKeyboardButton("📥 Download", url=download)
        ]]
    )

    await message.reply_text(
        text=(
            "<b>Your Link Generated!</b>\n\n"
            f"<b>📂 File:</b> <i>{get_name(log_msg)}</i>\n"
            f"<b>📦 Size:</b> <i>{humanbytes(get_media_file_size(message))}</i>"
        ),
        reply_markup=rm,
        disable_web_page_preview=True
    )
