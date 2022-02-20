# By @kirito6969 for Userge :)
# @PhycoNinja13b is OP AF

from userge import userge, Message
BOT = "myriasbot"

@userge.on_cmd(
    "iph",
    about={
        "header": "Inline Pornhub Search",
        "description": "U know already",
        "usage": "{tr}iph\n{tr}iph <reply or input>",
    },
)
async def phub(message: Message):
    "Inline phub search"
    input = message.input_or_reply_str
    r =  await userge.get_inline_bot_results(BOT, f"ph {input}")
    try:
    	await userge.send_inline_bot_result(message.chat.id, query_id=r.query_id, result_id=r.results[0].id)
    except Exception:
    	await message.err("**No results found**")
        