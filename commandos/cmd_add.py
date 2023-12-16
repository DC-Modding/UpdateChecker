async def ex(args, bot, message):
    result = int(args[0]) + int(args[1])
    msg = f'the result is {result}'
    await message.channel.send(msg)
