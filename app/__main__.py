import json
import importlib

from pyrogram import Client, filters
from pyrogram.types import Message

from . import ubot, COMMANDS_FILE_PATH
from .utils.alive import alive

def load_handlers():
    with open(COMMANDS_FILE_PATH, "r") as f:
        config = json.load(f)
    
    for module_path in config["modules"]:
        importlib.import_module(module_path, __package__)

@ubot.on_message(filters.command("ping", "-") & filters.me)
async def main(client: Client, message: Message):
    await message.edit_text("IM ALIVE")


if __name__ == "__main__":
    load_handlers()
    alive()
    ubot.run()  # Automatically start() and idle()
