from pyrogram import Client, filters
from pyrogram.types import Message
from app import ubot

@ubot.on_message(filters.command("setchatphoto", "-") & filters.me)
async def func_set_chat_photo(_: Client, message: Message):
    re_msg = message.reply_to_message

    if not re_msg or not (re_msg.photo or re_msg.document):
        await message.edit_text("Reply a photo!")
        return
    
    if re_msg.document and "image" not in re_msg.document.mime_type:
        await message.edit_text("Reply a photo!")
        return
    
    await message.edit_text("Updating Please wait!!")
    
    doc = None
    
    if re_msg.document:
        image = await re_msg.download("image.png", True)
        doc = True
    else:
        image = re_msg.photo
    
    try:
        await message.chat.set_photo(photo=image if doc else image.file_id)
    except Exception as e:
        await message.edit_text(f"Error: {e}")
        return
    
    await message.edit_text("Chat Photo Updated!")
