# VideoEncoder - a telegram bot for compressing/encoding videos in h264 format.
# Copyright (c) 2021 WeebTime/VideoEncoder
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
import shutil, psutil
import time
import heroku3
from functools import wraps
from pyrogram import Client, filters
from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant, UsernameNotOccupied, ChatAdminRequired, PeerIdInvalid
from pyrogram.types import Update, Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, ChatPermissions

from .. import (audio, crf, doc_thumb, preset, resolution, sudo_users, tune,
                upload_doc)
from ..utils.utils import check_user, output, start
    
#Heroku Dyno Restart Mod
HEROKU_API_KEY = "6cae9139-be87-4421-bc78-3363f82c58d1"
HEROKU_APP_NAME = "bdhc00mpre"

heroku_client = None
if HEROKU_API_KEY:
    heroku_client = heroku3.from_key(HEROKU_API_KEY)

def check_heroku(func):
    @wraps(func)
    async def heroku_cli(client, message):
        heroku_app = None
        if not heroku_client:
            await message.reply_text("`Please Add HEROKU_API_KEY Key For This To Function To Work!`", parse_mode="markdown")
        elif not HEROKU_APP_NAME:
            await message.reply_text("`Please Add HEROKU_APP_NAME For This To Function To Work!`", parse_mode="markdown")
        if HEROKU_APP_NAME and heroku_client:
            try:
                heroku_app = heroku_client.app(HEROKU_APP_NAME)
            except:
                await message.reply_text(message, "`Heroku Api Key And App Name Doesn't Match!`", parse_mode="markdown")
            if heroku_app:
                await func(client, message, heroku_app)

    return heroku_cli
  
@Client.on_message(filters.command(['reboot', f'reboot@{bot.username}']) & filters.user(sudo_users))
@check_heroku
async def gib_restart(client, message, hap):
    msg_ = await message.reply_text("[Server] - Restarting")
    hap.restart()
  
@Client.on_message(filters.command('start'))
async def start_message(app, message):
    check = await check_user(message)
    if check is None:
        return
    text = f"Hey! I'm <a href='https://telegra.ph/file/11379aba315ba245ebc7b.jpg'>VideoEncoder</a>. I can encode telegram files in x264.\n\nPress /help for my commands :)"
    await message.reply(text=text, reply_markup=start)

#Status Mod
botStartTime = time.time()
SIZE_UNITS = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']

def get_readable_time(seconds: int) -> str:
    result = ''
    (days, remainder) = divmod(seconds, 86400)
    days = int(days)
    if days != 0:
        result += f'{days}d'
    (hours, remainder) = divmod(remainder, 3600)
    hours = int(hours)
    if hours != 0:
        result += f'{hours}h'
    (minutes, seconds) = divmod(remainder, 60)
    minutes = int(minutes)
    if minutes != 0:
        result += f'{minutes}m'
    seconds = int(seconds)
    result += f'{seconds}s'
    return 

def get_readable_file_size(size_in_bytes) -> str:
    if size_in_bytes is None:
        return '0B'
    index = 0
    while size_in_bytes >= 1024:
        size_in_bytes /= 1024
        index += 1
    try:
        return f'{round(size_in_bytes, 2)}{SIZE_UNITS[index]}'
    except IndexError:
        return 'File too large'
      
@Client.on_message(filters.command('status'))
async def stats(app, message):
    currentTime = get_readable_time((time.time() - botStartTime))
    total, used, free = shutil.disk_usage('.')
    total = get_readable_file_size(total)
    used = get_readable_file_size(used)
    free = get_readable_file_size(free)
    cpuUsage = psutil.cpu_percent(interval=0.5)
    memory = psutil.virtual_memory().percent
    stats = f'Bot Uptime: {currentTime}\n' \
            f'Total disk space: {total}\n' \
            f'Used: {used}\n' \
            f'Free: {free}\n' \
            f'CPU: {cpuUsage}%\n' \
            f'RAM: {memory}%\n' \
            f'@BangladeshHoarding'
    await message.reply(text=stats, reply_markup=output)

@Client.on_message(filters.command('help'))
async def help_message(app, message):
    check = await check_user(message)
    if check is None:
        return
    text = f"""<b>Commands:</b>
• AutoDetect Telegram Files.
• /help - Commands List.
• /start - Introduction.
• /vset - View Settings.
• /sthumb - Save Thumb
• /status - Status of the bot
• /guide - See it
• /dthumb - Clear Thumb.
• /logs - check logs."""
    await message.reply(text=text, reply_markup=output)


@Client.on_message(filters.command('vset'))
async def vset(app, message):
    check = await check_user(message)
    if check is None:
        return
    text = f'''<b>Encode Settings</b>
Tune: <code>{tune}</code> | <code>Preset: {preset}</code>
Audio: <code>{audio} | <code>CRF: {crf}</code>
Resolution: <code>{resolution}</code>

<b>Upload Settings<b>
Upload Mode: <code>{'Document' if (upload_doc) else 'Video' }</code>
Doc thumb: <code>{'True' if (doc_thumb) else 'False'}</code>

<b>Sudo Users</b>
<code>{sudo_users}</code>
'''
    await message.reply(text=text, reply_markup=start)


@Client.on_message(filters.command('logs'))
async def logs(app, message):
    check = await check_user(message)
    if check is None:
        return
    file = 'VideoEncoder/utils/logs.txt'
    await message.reply_document(file, caption='#Logs')

#ForeceSub On New Membe join
CHANNEL_USERNAME = "@BangladeshHoarding"
WARN_MESSAGE = "দুঃখিত 😐 আপনি এখনো গ্রুপের চ্যানলে জয়েন করেননি,\n\n🔇⭕️আপনাকে সাময়িক মিউট করা হয়েছে⭕️🔇 \n\nগ্রুপের চ্যানেল গুলোতে জয়েন করার পর আনমিউট বাটনে ক্লিক করে আনমিউট হয়ে নিন,\n আনমিউট হওয়ার পর গ্রুপটি ব্যবহার করতে পারবেন।"
static_data_filter = filters.create(lambda _, __, query: query.data == "hukaidaala")

@Client.on_callback_query(static_data_filter)
def _onUnMuteRequest(client, lel):
  user_id = lel.from_user.id
  chat_id = lel.message.chat.id
  chat_u = CHANNEL_USERNAME #channel for force sub
  if chat_u:
    channel = chat_u
    chat_member = client.get_chat_member(chat_id, user_id)
    if chat_member.restricted_by:
      if chat_member.restricted_by.id == (client.get_me()).id:
          try:
            client.get_chat_member(channel, user_id)
            client.unban_chat_member(chat_id, user_id)
            if lel.message.reply_to_message.from_user.id == user_id:
              lel.message.delete()
          except UserNotParticipant:
            client.answer_callback_query(lel.id, text="❗ চ্যানেল গুলোতে জয়েন করার পর আনমিউট বাটন আবার প্রেস করুন", show_alert=True)
      else:
        client.answer_callback_query(lel.id, text="❗ এডমিন আপনাকে আনমিউট করে দিয়েছে....", show_alert=True)
    else:
      if not client.get_chat_member(chat_id, (client.get_me()).id).status == 'administrator':
        client.send_message(chat_id, f"❗ **{lel.from_user.mention} is trying to Unmute himself but I can't unmute him because I am not an admin in this chat.")
      else:
        client.answer_callback_query(lel.id, text="❗ Warning: Don't click the button if you can speak freely.", show_alert=True)

@Client.on_message(filters.text & ~filters.private & ~filters.edited, group=1)
def _check_member(client, message):
  chat_id = message.chat.id
  chat_u = CHANNEL_USERNAME #channel for force sub
  if chat_u:
    user_id = message.from_user.id
    if not client.get_chat_member(chat_id, user_id).status in ("administrator", "creator"):
      channel = chat_u
      try:
        client.get_chat_member(channel, user_id)
      except UserNotParticipant:
         try: #tahukai daala
              chat_u = chat_u.replace('@','')
              tauk = message.from_user.mention
              sent_message = message.reply_text(
                WARN_MESSAGE,
                disable_web_page_preview=True,
                reply_markup=InlineKeyboardMarkup(
                  [[
                  InlineKeyboardButton("📢 𝐉𝐨𝐢𝐧 𝐍𝐨𝐰 1️⃣", url=f"https://t.me/Bangladesh_Hoarding"),
                  InlineKeyboardButton("📢 𝐉𝐨𝐢𝐧 𝐍𝐨𝐰 2️⃣", url=f"https://t.me/{chat_u}")],
                  [InlineKeyboardButton("✅ 𝐔𝐧𝐦𝐮𝐭𝐞 𝐌𝐞 ✅", callback_data="hukaidaala")]]))
              client.restrict_chat_member(chat_id, user_id, ChatPermissions(can_send_messages=False))               
         except ChatAdminRequired:
           sent_message.edit("❗ **I am not an admin here.**\n__Make me admin with ban user permission and add me again.\n#Leaving this chat...__")
           client.leave_chat(chat_id)
      except ChatAdminRequired:
        client.send_message(chat_id, text=f"❗ **I am not an admin in @{channel}**\n__Make me admin in the channel and add me again.\n#Leaving this chat...__")
        client.leave_chat(chat_id)
