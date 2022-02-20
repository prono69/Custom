# By @kirito6969 for Userge :)

from userge import userge, Message
import aiohttp

session = aiohttp.ClientSession()

@userge.on_cmd(
    "yo",
    about={
        "header": "Yo Momma jokes",
        "description": "It will fetch random YoMomma jokes from the api :)",
        "usage": "{tr}yo\n{tr}yo -s <1-978>",
    },
)
async def yomomma(message: Message):
    "Yo Momma"
    word = message.filtered_input_str
    url = None
    if "-s" in message.flags:
    	url = f"https://yomomma-api.herokuapp.com/jokes/{word}"
    else:
    	url = "https://yomomma-api.herokuapp.com/jokes"
    async with session.get(
        url
    ) as resp:
        data = await resp.json()
    if not data["joke"]:
        return await message.err(
            "***Unknown Error occured while fetching data***", 3
        )
    momma = data["joke"]
    # await message.delete()
    await message.edit(f"<code>{momma}</code>")
        