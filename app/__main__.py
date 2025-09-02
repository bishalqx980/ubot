from pyrogram import Client, filters
from pyrogram.types import Message
from . import app, logger

@app.on_message(filters.text & filters.me)
async def main(client: Client, message: Message):
    await message.reply(f"IM ALIVE!")


if __name__ == "__main__":
    app.run()  # Automatically start() and idle()
