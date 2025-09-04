import os
from time import time
from datetime import timedelta
from asyncio import sleep

from pyrogram import Client, filters
from pyrogram.types import Message
from app import ubot, logger
from app.modules.utils import Utils

ACTIVE_DOWNLOADS = []

async def progress(current, total, message: Message, message_text="", startTime=None):
    """
    :param current: Bytes transferred so far
    :param total: Total bytes
    :param message: Message class
    :param message_text: info text (e.g. "Downloading" or "Uploading")
    :param startTime: Progress start timestamp (time.time())
    """
    try:
        if startTime is None:
            startTime = time()
        
        percent = current * 100 / total
        elapsedTime = time() - startTime
        elapsed = timedelta(seconds=int(elapsedTime))

        # Speed in MB/s (bytes -> MB)
        currentSpeed = current / elapsedTime / (1024 * 1024)

        # Remaining time
        remainingSeconds = (total - current) / (currentSpeed * 1024 * 1024)
        remaining = timedelta(seconds=int(remainingSeconds))

        text = (
            f"**{message_text}**\n"
            f"**Speed:** `{currentSpeed:.2f}MB/s`\n"
            f"**Elapsed:** `{elapsed}`\n"
            f"**ETA:** `{remaining}`\n"
            f"**Progress:** `{Utils.createProgressBar(int(percent))}` `{percent:.2f}%`"
        )

        await message.edit_text(text)
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
    
    if ACTIVE_DOWNLOADS:
        await message.edit_text(
            f"<a href='{''.join(ACTIVE_DOWNLOADS)}'>This</a> is being downloading...!\n"
            f"`-clear` to clear download if anything is wrong!"
        )
        return
    
    await message.edit_text("Please wait...")
    await message.pin(both_sides=True)

    startTime = time()
    ACTIVE_DOWNLOADS.append(re_msg.link)

    zipFile = await re_msg.download(re_msg.document.file_name, progress=progress, progress_args=[message, "Downloading...", startTime])
    if not zipFile:
        await message.edit_text("Unable to download!")
        return

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
    startTime = time()
    for i in response:
        counter += 1
        try:
            percent = counter * 100/len(response)
            
            text = (
                f"Uploading...\n"
                f"**File:** `{i}`\n"
                f"**Total Percent:** `{Utils.createProgressBar(int(percent))}` `{percent:.2f}%`"
            )

            try:
                await message.reply_photo(i, progress=progress, progress_args=[message, text, startTime])
            except:
                try:
                    await message.reply_video(i, width=1280, height=720, progress=progress, progress_args=[message, text, startTime])
                except:
                    await message.reply_document(i, progress=progress, progress_args=[message, text, startTime])
            
            uploaded += 1
        except Exception as e:
            uploadfailed += f"- {e}: `{i}`\n"
        
        await sleep(0.5)

        try:
            os.remove(i)
        except Exception as e:
            logger.error(e)
    
    await message.edit_text(f"Upload Completed! ({uploaded}/{len(response)})\n{uploadfailed}")


@ubot.on_message(filters.command("clear", "-") & filters.me)
async def func_clear_active_downloads(_: Client, message: Message):
    ACTIVE_DOWNLOADS.clear()
    await message.edit_text("Active download list has been cleared!")
