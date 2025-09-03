from pyrogram import Client, filters
from pyrogram.types import Message
from app import ubot

@ubot.on_message(filters.command(["start", "help"], "-") & filters.me)
async def func_start(_: Client, message: Message):
    text = (
        "[`-start`, `-help`] - To see this menu\n"
        "[`-unzip`, `-uz`] - to unzip any zip file\n"
        "[`-invite`] - invite `@username` in current chat\n"
        "[`-del`] - Delete all messages from replied to current\n"
        "[`-setchatphoto`] - to change chat photo"
    )

    await message.edit_text(text)
