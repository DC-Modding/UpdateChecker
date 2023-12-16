import discord


async def ex(args, bot, message):
    embed = discord.Embed(title='All available commands',
                          description='hello\nadd - usage: needs 2 numbers, eg.: -add 1 2\nhelp',
                          color=discord.Color.yellow())
    await message.channel.send(embed=embed)
