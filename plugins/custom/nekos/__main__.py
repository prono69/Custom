from .. import nekos
import os

from anekos import NekosLifeClient, SFWImageTags
from pyrogram.errors import MediaEmpty, WebpageCurlFailed
from wget import download
from userge import Message, userge

client = NekosLifeClient()

SFW = [z for z in dir(SFWImageTags) if not z.startswith("__")]


neko_help = "<b>NSFW</b> :  "
neko_help += "\n\n<b>SFW</b> :  "
for m in SFW:
    neko_help += f"<code>{m.lower()}</code>   "


@userge.on_cmd(
    "ne",
    about={
        "header": "Get SFW stuff from nekos.life",
        "flags": {"ne": "For random SFW"},
        "usage": "{tr}ne\n{tr}ne [Choice]",
        "Choice": neko_help,
    },
)
async def neko_life(message: Message):
    choice = message.input_str
    if choice:
        input_choice = (choice.strip()).upper()
        if input_choice in SFW:
            link = (await client.image(SFWImageTags[input_choice])).url
        else:
            await message.err(
                "Choose a valid Input !, See Help for more info.", del_in=5
            )
            return
    else:
        link = (await client.random_image()).url

    await message.delete()

    try:
        await nekos.send_nekos(message, link)
    except (MediaEmpty, WebpageCurlFailed):
        link = download(link)
        await nekos.send_nekos(message, link)
        os.remove(link)


        