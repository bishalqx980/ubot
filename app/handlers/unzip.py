import os
from asyncio import sleep

from pyrogram import Client, filters
from pyrogram.types import Message
from app import ubot, logger
from app.modules.utils import Utils

async def progress(current, total, message):
    try:
        percent = float(current * 100 / total)
        await message.edit_text(
            f"Downloading... `{percent:.2f}%`\n"
            f"**Progress:** `{Utils.createProgressBar(int(percent))}`"
        )
    except Exception as e:
        logger.error(e)

@ubot.on_message(filters.command(["unzip", "uz"], "-") & filters.me)
async def func_unzip(_: Client, message: Message):
    re_msg = message.reply_to_message
    password = message.text.removeprefix(f"-{message.command[0]}").strip() or None

    if not re_msg or not re_msg.document:
        await message.edit_text("Reply any `.zip` file to extract the file. E.g. `/unzip password (if needed)`")
        return
    
    if not re_msg.document.file_name.endswith(".zip"):
        await message.edit_text("Replied file isn't a `.zip` file!")
        return
    
    await message.edit_text("Please wait...")
    await message.pin(both_sides=True)
    zipFile = await re_msg.download(re_msg.document.file_name, progress=progress, progress_args=[message])

    # Unzipping
    await message.edit_text("Unziping...")
    response = Utils.unzipFile(zipFile, password)

    # Remove Zip file
    try:
        os.remove(zipFile)
    except Exception as e:
        logger.error(e)
    
    # After Response
    if not isinstance(response, list):
        await message.edit_text(f"Error: {response}")
        return
    
    # File path list
    counter = 0
    uploaded = 0
    uploadfailed = ""
    for i in response:
        counter += 1
        try:
            percent = counter * 100/len(response)
            percentBar = Utils.createProgressBar(percent)
            await message.edit_text((
                f"Uploading... `{percent:.2f}%`\n"
                f"**File:** `{i}`\n"
                f"**Percent:** `{percentBar}`"
            ))
            await message.reply_document(i)
            uploaded += 1
        except Exception as e:
            uploadfailed += f"- {e}: `{i}`\n"
        
        await sleep(0.5)

        try:
            os.remove(i)
        except Exception as e:
            logger.error(e)
    
    await message.edit_text(f"Upload Completed! ({uploaded}/{len(response)})\n{uploadfailed}")
    await message.unpin()
