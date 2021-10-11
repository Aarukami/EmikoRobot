import os
from telethon.errors.rpcerrorlist import YouBlockedUserError

from NaoRobot import ubot
from NaoRobot.events import register
from NaoRobot import telethn as tbot, TEMP_DOWNLOAD_DIRECTORY


@register(pattern="^/kamuii ?(.*)")
async def _(fry):
    await fry.edit("`Cringgggg Jadi Benjol...`")
    level = fry.pattern_match.group(1)
    if fry.fwd_from:
        return
    if not fry.reply_to_msg_id:
        await fry.edit("`Mohon Balas Di Sticker`")
        return
    reply_message = await fry.get_reply_message()
    if not reply_message.media:
        await fry.edit("`Gambar tidak di dukung`")
        return
    if reply_message.sender.bot:
        await fry.edit("`Mohon Balas Di Sticker`")
        return
    chat = "@image_deepfrybot"
    message_id_to_reply = fry.message.reply_to_msg_id
    async with ubot.conversation(chat) as conv:
        try:
            msg = await conv.send_message(reply_message)
            if level:
                m = f"/deepfry {level}"
                msg_level = await conv.send_message(
                    m,
                    reply_to=msg.id)
                r = await conv.get_response()
                response = await conv.get_response()
            else:
                response = await conv.get_response()
            """ - don't spam notif - """
            await ubot.send_read_acknowledge(conv.chat_id)
        except YouBlockedUserError:
            await fry.reply("`Mohon Unblock` @image_deepfrybot`...`")
            return
        if response.text.startswith("Forward"):
            await fry.edit("`Mohon Matikan Setelan Forward Privasi...`")
        else:
            downloaded_file_name = await ubot.download_media(
                response.media,
                TEMP_DOWNLOAD_DIRECTORY
            )
            await tbot.send_file(
                fry.chat_id,
                downloaded_file_name,
                force_document=False,
                reply_to=message_id_to_reply
            )
            """ - cleanup chat after completed - """
            try:
                msg_level
            except NameError:
                await fry.ubot.delete_messages(conv.chat_id,
                                                 [msg.id, response.id])
            else:
                await ubot.delete_messages(
                    conv.chat_id,
                    [msg.id, response.id, r.id, msg_level.id])
    await fry.delete()
    return os.remove(downloaded_file_name)