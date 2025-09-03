from pyrogram import Client, filters
from pyrogram.types import Message
from app import ubot

@ubot.on_message(filters.command("del", "-") & filters.me)
async def func_delete_message(_: Client, message: Message):
    re_msg = message.reply_to_message
    await message.edit_text("Started Deleting Messages!!")

    try:
        await ubot.delete_messages(message.chat.id, list(range(re_msg.id, message.id)))
    except Exception as e:
        await message.edit_text(f"Error: {e}")
        return
    
    await message.edit_text(f"Deleted messages from {re_msg.id} to {message.id} !!")
