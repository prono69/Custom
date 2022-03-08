from userge import Message

async def send_nekos(message: Message, link: str):
    reply = message.reply_to_message
    reply_id = reply.message_id if reply else None
    if link.endswith(".gif"):
        #  Bots can't use "unsave=True"
        bool_unsave = not message.client.is_bot
        await message.client.send_animation(
            chat_id=message.chat.id,
            animation=link,
            unsave=bool_unsave,
            reply_to_message_id=reply_id,
        )
    else:
        await message.client.send_photo(
            chat_id=message.chat.id, photo=link, reply_to_message_id=reply_id
        )
