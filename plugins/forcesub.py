import asyncio
from pyrogram import Client, enums
from pyrogram.errors import UserNotParticipant
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from info import FORCE_SUB_CHANNEL, FORCE_SUB_TEXT

async def handle_force_subscribe(bot, message):
    if not FORCE_SUB_CHANNEL:
        return True
    try:
        user = await bot.get_chat_member(FORCE_SUB_CHANNEL, message.from_user.id)
        if user.status == enums.ChatMemberStatus.BANNED:
            await message.reply_text("দুঃখিত, আপনাকে ব্যান করা হয়েছে।")
            return False
        return True
    except UserNotParticipant:
        invite_link = await bot.create_chat_invite_link(FORCE_SUB_CHANNEL)
        await message.reply_text(
            text=FORCE_SUB_TEXT,
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("Join Channel", url=invite_link.invite_link)]]
            )
        )
        return False
    except Exception:
        return True
      
