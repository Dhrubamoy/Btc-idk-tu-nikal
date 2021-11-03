from pyrogram import Client, filters
from pyrogram.types import Message
from pytgcalls import PyTgCalls
from player.videoplayer import call_py
from helper.decorators import authorized_users_only

@Client.on_message(filters.command(["stopstream", "stop"]))
@authorized_users_only
async def stopvideo(client, m: Message):
    chat_id = m.chat.id
    try:
        await call_py.leave_group_call(chat_id)
        await m.reply("**⏹️ Stopped Video Stream!**")
    except Exception as e:
        await m.reply(f"`{e}`")
        
@Client.on_message(filters.command("pause"))
@authorized_users_only
async def pausevideo(client, m: Message):
    chat_id = m.chat.id
    try:
        await call_py.pause_stream(chat_id)
        await m.reply("**⏸️ Paused Video Stream!**")
    except Exception as e:
        await m.reply(f"`{e}`")
        
@Client.on_message(filters.command("resume"))
@authorized_users_only
async def resumevideo(client, m: Message):
    chat_id = m.chat.id
    try:
        await call_py.resume_stream(chat_id)
        await m.reply("**▶ Resumed Video Stream!**")
    except Exception as e:
        await m.reply(f"`{e}`")
