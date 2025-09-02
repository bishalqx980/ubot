from pyrogram import Client, filters
from pyrogram.types import Message
from . import ubot, SERVER_URL
from .utils.alive import alive
from .modules.utils import Utils
from .handlers.unzip import func_unzip

@ubot.on_message(filters.command("ping", "-") & filters.me)
async def main(client: Client, message: Message):
    await message.edit_text(f"Sending ping: {SERVER_URL}")
    await message.edit_text(f"Response: {await Utils.pingServer(SERVER_URL)}")


if __name__ == "__main__":
    alive()
    ubot.run()  # Automatically start() and idle()
