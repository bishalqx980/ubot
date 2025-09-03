from pyrogram import Client, filters
from pyrogram.types import Message
from app import ubot

@ubot.on_message(filters.command("invite", "-") & filters.me)
async def func_invite(_: Client, message: Message):
    username = message.text.removeprefix(f"-{message.command[0]}").strip() or None

    if not username:
        await message.edit_text("Example: `-invite @username`")
        return
    
    try:
        await message.chat.add_members(username)
    except Exception as e:
        await message.edit_text(f"Error: {e}")
        return
    
    await message.edit_text(f"{username} has been added!")
