# Copyright (C) 2020-2021 by DevsExpo@Github, < https://github.com/DevsExpo >.
#
# This file is part of < https://github.com/DevsExpo/FridayUserBot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/DevsExpo/blob/master/LICENSE >
#
# All rights reserved.

import os
from pygments import highlight
from pygments.lexers import guess_lexer
from pygments.formatters import HtmlFormatter, JpgImageFormatter
from userge.utils import runcmd
from userge import userge, Message


@userge.on_cmd('pcode', about={
               "header": "Convert Python Codes To Highlighted Html / Image",
               "usage": "{tr}cih (replying to py file)"})
async def convert_to_image_or_html(message: Message):
    force_html = False
    msg_ = await message.edit("`Please Wait!`")
    t = message.input_str
    if t:
        force_html = True
    if not message.reply_to_message:
        await msg_.edit("`Please Reply To A Python Document.`")
        return
    if not message.reply_to_message.document:
        await msg_.edit("`Please Reply To A Python Document.`")
        return
    if message.reply_to_message.document.mime_type != "text/x-python":
        await msg_.edit("`Please Reply To A Python Document.`")
        return
    file_ = await message.reply_to_message.download()
    output_ = await create_html_or_img(file_, force_html)
    await message.reply_to_message.reply_document(output_, quote=True)
    await msg_.delete()
    os.remove(output_)

async def create_html_or_img(file, force_html=False):
    file_t = open(file, "r")
    file_z = file_t.readlines()
    if len(file_z) >= 79:
        force_html = True
    if force_html:
        file_name = "code.html"
        await runcmd(f"pygmentize -f html -O full -o {file_name} {file}")
        return file_name
    else:
        data = "\n".join(file_z)
        file_name = "code.jpg"
        f_jpg = open(file_name, 'wb')
        lexer = guess_lexer(data)
        f_jpg.write(highlight(data, lexer, JpgImageFormatter()))
        return file_name