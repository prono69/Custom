# By @kirito6969 for Userge

import requests
from userge import userge, Message
from userge.utils import rand_array
from userge.plugins.custom.nekos import send_nekos

NSFW = [
    'ass',
    'bdsm',
    'blowjob',
    'cum',
    'cumslut',
    'doujin',
    'feet',
    'femdom',
    'foxgirl',
    'gangbang',
    'gif',
    'glasses',
    'hentai',
    'lewdneko',
    'maid',
    'maids',
    'masturbation',
    'netorare',
    'nsfwmobilewallpapers',
    'nsfwwallpapers',
    'orgy',
    'panties',
    'pussy',
    'random',
    'school',
    'succubus',
    'tentacles',
    'thighs',
    'uglybastard',
    'uniform',
    'yuri',
    'zettai-ryouiki']

SFW = ['mobilewallpapers', 'neko', 'sfwfoxes', 'wallpapers']

neko_help = "<b>🔞NSFW</b> :  "
for i in NSFW:
    neko_help += f"<code>{i.lower()}</code>   "
neko_help += "\n\n<b>😇SFW</b> :  "
for m in SFW:
    neko_help += f"<code>{m.lower()}</code>   "


@userge.on_cmd(
    "ak",
    about={
        "header": "Get NSFW / SFW stuff from akaneko ^_^",
        "flags": {"nsfw": "For random NSFW"},
        "usage": "{tr}ak\n{tr}ak -nsfw\n{tr}ak [Choice]",
        "Choice": neko_help,
    },
)
async def akaneko(message: Message):
    choice = message.input_str
    if "-nsfw" in message.flags:
        choosen_ = rand_array(NSFW)
    elif choice:
        neko_all = SFW + NSFW
        choosen_ = (choice.split())[0]
        if choosen_ not in neko_all:
            await message.err('Choose a valid Input !, See Help for more info.', del_in=5)
            return
    else:
        choosen_ = rand_array(SFW)

    await message.delete()
    k = requests.get(
        f"http://cuteasfubuki.cf/api/{choosen_}").json()
    link = k.get("url")
    try:
        await send_nekos(message, link)
    except Exception:
        await message.err("Nothing to send :(", del_in=4)
