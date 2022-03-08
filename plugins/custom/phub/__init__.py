""" Inline pornhub search """

# Inline PornHub Search by @kirito6969 for Userge
# @PhycoNinja13b is OP AF

import re
import time
import base64
import struct
from typing import Dict, Tuple, List
from pornhub_api import PornhubApi
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InlineQueryResultArticle, InputTextMessageContent

from userge import userge, filters, Config

CB_PATTERN = re.compile(r"PS(\d+):([\-\w]+)")
time_token = lambda: base64.urlsafe_b64encode(
    struct.pack("<I", int(time.time()))
).decode("utf-8").strip("=")
SAVE: Dict[Tuple[int, str], Tuple[str, List]] = {}


def navigation_builder(index: int, total: int, data: str):
    nav_row = []
    if index > 0:
        nav_row.append(InlineKeyboardButton(text="Back", callback_data=data.format(index - 1)))
    nav_row.append(InlineKeyboardButton(text=f"{index + 1}/{total}", callback_data="null"))
    if index < total:
        nav_row.append(InlineKeyboardButton(text="Next", callback_data=data.format(index + 1)))
    return nav_row


def page_data(match: re.Match, user_id: int):
    index, ct_id = match.groups()
    index = int(index)
    _, data = SAVE.get((user_id, ct_id), (None, None))
    if data is None:
        return None, None
    return _, data[index]


@userge.bot.on_callback_query(filters.regex(CB_PATTERN))
async def _ph_ps_callback_handler(_, event):
    user_id = event.from_user.id
    input_str, vid = page_data(event.matches[0], user_id)
    if not vid:
        return await event.answer("Not found for YOU!")
    index, ct_id = event.matches[0].groups()
    index = int(index)
    data = SAVE.get((user_id, ct_id))
    total = len(data[1])
    cb_data = f"PS{{}}:{ct_id}"
    await event.edit_message_text(
        text=(
            f"[𝙋𝙤𝙧𝙣𝙃𝙪𝙗 𝙎𝙚𝙖𝙧𝙘𝙝] \n**Sᴇᴀʀᴄʜ Qᴜᴇʀʏ :** __{input_str}__ \n"
            f"**Vɪᴅᴇᴏ Tɪᴛʟᴇ :** __{vid.title}__ \n"
            "**Vɪᴅᴇᴏ Lɪɴᴋ :** __https://www.pornhub.com/"
            f"view_video.php?viewkey={vid.video_id}__"
        ),
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(
                "𝙎𝙀𝘼𝙍𝘾𝙃 𝘼𝙂𝘼𝙄𝙉", switch_inline_query_current_chat="ph "
            )],
            navigation_builder(index, total, cb_data)
        ])
    )
    await event.answer(f"Moved to result ({index + 1}/{total})")


@userge.bot.on_inline_query(filters.regex("ph(.*)"), group=-1)
async def inline_id_handler(_, event):
    if event.from_user.id not in Config.OWNER_ID:
        resultm = [InlineQueryResultArticle(
            title="• [NIKAL LAWDE] •",
            input_message_content=InputTextMessageContent("!!!!!NONE!!!!!"),
            description="You Can't Use This Bot. \nDeploy Your Own Userge",
        )]
        await event.answer(results=resultm)
        return
    results = []
    input_str = event.matches[0].group(1)
    api = PornhubApi()
    data = api.search.search(input_str, ordering="mostviewed")
    ok = 1
    ct_id = time_token()
    SAVE[(event.from_user.id, ct_id)] = (input_str, list(data.videos))
    cb_data = f"PS{{}}:{ct_id}"
    total = len(SAVE[(event.from_user.id, ct_id)][1])
    for index, vid in enumerate(data.videos):
        if ok <= 5:
            lul_m = (
                f"[𝙋𝙤𝙧𝙣𝙃𝙪𝙗 𝙎𝙚𝙖𝙧𝙘𝙝] \n**Sᴇᴀʀᴄʜ Qᴜᴇʀʏ :** __{input_str}__ \n"
                f"**Vɪᴅᴇᴏ Tɪᴛʟᴇ :** __{vid.title}__ \n"
                "**Vɪᴅᴇᴏ Lɪɴᴋ :** __https://www.pornhub.com/"
                f"view_video.php?viewkey={vid.video_id}__"
            )
            results.append(
                InlineQueryResultArticle(
                    title=vid.title,
                    input_message_content=InputTextMessageContent(lul_m),
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton(
                            "𝙎𝙀𝘼𝙍𝘾𝙃 𝘼𝙂𝘼𝙄𝙉", switch_inline_query_current_chat="ph "
                        )],
                        navigation_builder(index, total, cb_data)
                    ]),
                )
            )
        else:
            pass
    await event.answer(results=results)
    event.stop_propagation()
