from asyncio import run
from pyrogram import Client

# USER FILLUP SECTION
API_ID = 123
API_HASH = ""

# DONT TOUCH THIS UNLESS YOU KNOW WHAT ARE YOU DOING
async def main():
    try:
        async with Client("account", API_ID, API_HASH) as ubot:
            await ubot.send_message("me",
                f"**API_ID:** `{API_ID}`\n"
                f"**API_HASH:** `{API_HASH}`\n"
                f"**Session_String:** `{await ubot.export_session_string()}`"
            )
    except Exception as e:
        print(e)

if __name__ == "__main__":
    run(main())
