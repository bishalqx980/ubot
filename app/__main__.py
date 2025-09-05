import os
import asyncio

from pyrogram import idle

from . import ubot, logger
from .utils.alive import alive

def load_handlers():
    handlers_dir = "app/handlers"
    for root, dirs, files in os.walk(handlers_dir):
        for filename in files:
            if filename.endswith(".py") and not filename.startswith("_"):
                rel_path = os.path.relpath(root, handlers_dir)
                if rel_path == ".":
                    module_path = f"app.handlers.{filename[:-3]}"
                else:
                    rel_module_path = rel_path.replace(os.sep, ".")
                    module_path = f"app.handlers.{rel_module_path}.{filename[:-3]}"
                __import__(module_path)


async def bot_init():
    try:
        await ubot.send_message("me", "Client Started!")
    except Exception as e:
        logger.error(e)
    
    logger.info("CLIENT STARTED...!")
    await idle()


async def main():
    # Need to load before bot.run()
    load_handlers()
    alive()

    try:
        await ubot.start()
        await bot_init()
    except Exception as e:
        logger.error(e)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
