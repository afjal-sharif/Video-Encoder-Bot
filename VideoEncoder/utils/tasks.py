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

import os
import time
import psutil
import shutil
from pyrogram.errors.exceptions.bad_request_400 import (MessageIdInvalid,
                                                        MessageNotModified)
from pyrogram.types import Message

from .. import data, doc_thumb, download_dir, upload_doc
from .ffmpeg import encode, get_duration, get_thumbnail
from .progress import progress_for_pyrogram
from .utils import output
from .. import (audio, crf, doc_thumb, preset, resolution, sudo_users, tune,
                upload_doc)

server = f"<b>CPU:</b> {psutil.cpu_percent()}% || <b>RAM:</b> {psutil.virtual_memory().percent}%"
donewithcurrentprofile = f"Video Encoded Successfully! \n\n <b>Encode Settings: \n</b><b>Resolution:</b> <code>{resolution}</code> | <b>CRF:</b> <code>{crf}</code> \n <b>Tune:</b> <code>{tune}</code> |  <b>Audio:</b> <code> {audio} </code> \n<b>Preset:</b><code> {preset}</code> \n\n {server}"
async def on_task_complete():
    del data[0]
    if len(data) > 0:
        await handle_task(data[0])

async def handle_task(message: Message):
    try:
        msg = await message.reply_text("<code>Downloading video...</code>")
        c_time = time.time()
        filepath = await message.download(
            file_name=download_dir,
            progress=progress_for_pyrogram,
            progress_args=("🔻Downloading...", msg, c_time))
        print(f'[Download]: {filepath}')
        await msg.edit_text('<code>Encoding...</code>')
        new_file = await encode(filepath)
        if new_file:
            await msg.edit_text("<code>Video Encoded, getting metadata...</code>")
            await handle_upload(new_file, message, msg)
            await msg.edit_text(donewithcurrentprofile)
        else:
            await message.reply_text("<code>Something wents wrong while encoding your file.</code>")
        os.remove(filepath)
    except MessageNotModified:
        pass
    except MessageIdInvalid:
        await msg.edit_text('Download Cancelled!')
    except Exception as e:
        print(f'[Error]: {e}')
        await msg.edit_text(f"<code>{e}</code>")
    await on_task_complete()


async def handle_upload(new_file, message, msg):
    print(f'[Upload]: {new_file}')
    # Variables
    user_id = message.from_user.id
    c_time = time.time()
    filename = os.path.basename(new_file)
    duration = get_duration(new_file)
    thumb = os.path.join(str(user_id), 'thumbnail.jpg')
    height = 720
    width = 1280
    if not os.path.isfile(thumb):
        thumb = get_thumbnail(new_file, download_dir, duration / 4)
    # Upload File
    if upload_doc:
        if doc_thumb:
            thumb = thumb
        else:
            thumb = None
        await message.reply_document(
            new_file,
            thumb=thumb,
            caption=filename,
            reply_markup=output,
            parse_mode=None,
            progress=progress_for_pyrogram,
            progress_args=("🔺Uploading ...", msg, c_time)
        )
    else:
        await message.reply_video(
            new_file,
            supports_streaming=True,
            parse_mode=None,
            reply_markup=output,
            caption=filename,
            thumb=thumb,
            duration=duration,
            width=width,
            height=height,
            progress=progress_for_pyrogram,
            progress_args=("🔺Uploading ...", msg, c_time)
        )
    os.remove(new_file)
