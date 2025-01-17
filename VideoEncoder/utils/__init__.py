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

from pyrogram import filters
from pyrogram.errors import RPCError

from .. import app as a
from . import ffmpeg, progress, tasks, utils

sauce = '''Encode Settings Guide 
RESOLUTION: 
>> Source 
>> 1080 
>> 720 
>> 480 
>> 360 

PRESET:
>> uf = ultrafast
>> sf = superfast
>> vf = veryfast
>> f = fast
>> m = medium

AUDIO (Codec):
>> opus
>> aac
>> copy

CRF: It's percentage of compress rate
>>  15 - 40 
'''


@a.on_message(filters.command('guide'))
async def g_s(_, message):
    try:
        await message.reply(text=sauce, reply_markup=utils.output)
    except RPCError:
        pass
