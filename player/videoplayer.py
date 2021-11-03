import os
import re
import asyncio
import subprocess
from pytgcalls import idle
from pytgcalls import PyTgCalls
from pytgcalls import StreamType
from pyrogram import Client, filters
from pytgcalls.types.input_stream import AudioVideoPiped
from pytgcalls.types.input_stream.quality import HighQualityAudio, MediumQualityAudio
from pytgcalls.types.input_stream.quality import HighQualityVideo, MediumQualityVideo, LowQualityVideo
from pyrogram.types import Message
from config import API_ID, API_HASH, SESSION_NAME,ADMIN,CHANNEL
from helper.decorators import authorized_users_only
from youtube_dl import YoutubeDL
from youtubesearchpython import VideosSearch

app = Client(SESSION_NAME, API_ID, API_HASH)
call_py = PyTgCalls(app)
ACTV_CALLS = []
opts = {"format": "best[height=?720]/best", "noplaylist": True}
ydl = YoutubeDL(opts)


@Client.on_message(filters.command("stream"))
@authorized_users_only
async def stream(client, m: Message):
    replied = m.reply_to_message
    if not replied or (replied and not (replied.video or replied.document)):
        if len(m.command) < 2:
            await m.reply("`Reply to some Video File!`")
        else:
            query = m.text.split(None, 1)[1]
            regex = r"^(https?\:\/\/)?(www\.youtube\.com|youtu\.?be)\/.+"
            match = re.match(regex,query)
            if match:
                try:
                    meta = ydl.extract_info(query, download=False)
                    formats = meta.get('formats', [meta])
                    for f in formats:
                        ytstreamlink = f['url']
                    livelink = ytstreamlink
                    search = VideosSearch(query, limit=1)
                    opp = search.result()["result"]
                    oppp = opp[0]
                    thumbid = oppp["thumbnails"][0]["url"]
                    split = thumbid.split("?")
                    photoid = split[0].strip()
                    msg = await m.reply_photo(photo=photoid, caption="`Starting YT Stream...`")
                except Exception as e:
                    msg = await m.reply(f"{e}")
                    return
            else:
                livelink = query
                photoid = "https://telegra.ph/file/b10a65c868444c0611773.jpg"
                msg = await m.reply_photo(photo=photoid, caption="`Starting Video Stream...`")
                    
            chat_id = int(m.chat.id)
            if chat_id in ACTV_CALLS:
                try:
                    await call_py.change_stream(
                        chat_id,
                        AudioVideoPiped(
                            livelink,
                            HighQualityAudio(),
                            HighQualityVideo()
                        ),
                    )
                    await msg.edit_caption(f"**Started [Video Stream]({livelink}) !**")
                    
                except Exception as e:
                    await msg.edit_caption(f"**Error** -- `{e}`")
            else:
                try:
                    await call_py.join_group_call(
                        chat_id,
                        AudioVideoPiped(
                            livelink,
                            HighQualityAudio(),
                            HighQualityVideo()
                        ),
                        stream_type=StreamType().pulse_stream,
                    )
                    await msg.edit_caption(f"**Started [Video Stream]({livelink}) !**")
                    ACTV_CALLS.append(chat_id)
                except Exception as e:
                    await msg.edit_caption(f"**Error** -- `{e}`")
   
    elif replied and (replied.video or replied.document):
        if replied.video.thumbs:
            huehue = replied.video.thumbs[0]
            umm = await client.download_media(huehue['file_id'])
            photoid = umm
        else:
            photoid = "https://telegra.ph/file/62e86d8aadde9a8cbf9c2.jpg"
        msg = await m.reply_photo(photo=photoid, caption="`Downloading...`")
        video = await client.download_media(m.reply_to_message)
        chat_id = int(m.chat.id)
        if chat_id in ACTV_CALLS:
                try:
                    await call_py.change_stream(
                        chat_id,
                        AudioVideoPiped(
                            video,
                            HighQualityAudio(),
                            HighQualityVideo()
                        ),
                    )
                    await msg.edit_caption(f"**Started Video Stream!**")
                    
                except Exception as e:
                    await msg.edit_caption(f"**Error** -- `{e}`")
        else:
                try:
                    await call_py.join_group_call(
                        chat_id,
                        AudioVideoPiped(
                            video,
                            HighQualityAudio(),
                            HighQualityVideo()
                        ),
                        stream_type=StreamType().pulse_stream,
                    )
                    await msg.edit_caption(f"**Started Video Stream!**")
                    ACTV_CALLS.append(chat_id)
                except Exception as e:
                    await msg.edit_caption(f"**Error** -- `{e}`")
   
    else:
        await m.reply("`Reply to some Video!`")


#channel Stream
@Client.on_message(filters.private & filters.user(ADMIN) & filters.command(["cplay"]))
async def chstream(client, m: Message):
    replied = m.reply_to_message
    if not replied:
        if len(m.command) < 2:
            await m.reply("`Reply to some Video File!`")
        else:
            query = m.text.split(None, 1)[1]
            regex = r"^(https?\:\/\/)?(www\.youtube\.com|youtu\.?be)\/.+"
            match = re.match(regex,query)
            if match:
                try:
                    meta = ydl.extract_info(query, download=False)
                    formats = meta.get('formats', [meta])
                    for f in formats:
                        ytstreamlink = f['url']
                    livelink = ytstreamlink
                    msg = await m.reply("`Starting YT Stream...`")
                except Exception as e:
                    msg = await m.reply(f"{e}")
                    return
            else:
                livelink = query
                msg = await m.reply("`Starting Video Stream...`")
                    
            chat_id = CHANNEL
            if chat_id in ACTV_CALLS:
                try:
                    await call_py.change_stream(
                        chat_id,
                        AudioVideoPiped(
                            livelink,
                            HighQualityAudio(),
                            HighQualityVideo()
                        ),
                    )
                    await msg.edit_caption(f"**Started Video Stream!**")
                    
                except Exception as e:
                    await msg.edit_caption(f"**Error** -- `{e}`")
            else:
                try:
                    await call_py.join_group_call(
                        chat_id,
                        AudioVideoPiped(
                            livelink,
                            HighQualityAudio(),
                            HighQualityVideo()
                        ),
                        stream_type=StreamType().pulse_stream,
                    )
                    await msg.edit_caption(f"**Started Video Stream!**")
                    ACTV_CALLS.append(chat_id)
                except Exception as e:
                    await msg.edit_caption(f"**Error** -- `{e}`")

    elif replied.video or replied.document:
        msg = await m.reply("`Downloading...`")
        video = await client.download_media(m.reply_to_message)
        chat_id = CHANNEL
        if chat_id in ACTV_CALLS:
                try:
                    await call_py.change_stream(
                        chat_id,
                        AudioVideoPiped(
                            video,
                            HighQualityAudio(),
                            HighQualityVideo()
                        ),
                    )
                    await msg.edit_caption(f"**Started Video Streaming!**")
                except Exception as e:
                    await msg.edit_caption(f"**Error** -- `{e}`")
        else:
                try:
                    await call_py.join_group_call(
                        chat_id,
                        AudioVideoPiped(
                            video,
                            HighQualityAudio(),
                            HighQualityVideo()
                        ),
                        stream_type=StreamType().pulse_stream,
                    )
                    await msg.edit_caption(f"**Started Video Stream!**")
                    ACTV_CALLS.append(chat_id)
                except Exception as e:
                    await msg.edit_caption(f"**Error** -- `{e}`")
   
    
    else:
        await m.reply("`Reply to some Video!`")

@Client.on_message(filters.private & filters.user(ADMIN) & filters.command(["cstop"]))
async def chstopvideo(client, m: Message):
    chat_id = CHANNEL
    try:
        await call_py.leave_group_call(chat_id)
        await m.reply("**⏹️ Stop Channel Stream!**")
    except Exception as e:
        await m.reply(f"**🚫 Error** - `{e}`")
        
