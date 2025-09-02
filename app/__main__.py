from pyrogram import Client, filters
from pyrogram.types import Message
from . import ubot
from .handlers.unzip import func_unzip

@ubot.on_message(filters.command("ping", "-") & filters.me)
async def main(client: Client, message: Message):
    await message.reply(f"IM ALIVE!")


if __name__ == "__main__":
    ubot.run()  # Automatically start() and idle()
