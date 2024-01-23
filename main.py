import discord
from discord.ext import commands
import asyncio
import statics
import secrets
from request import make_initial_request_and_fill_file, check_for_updates
from request_DB import create_initial_db, fill_initial_data_db, check_for_updates_db


######################################################################################
# if you want to add new commands, create a cmd_*command* file in the commandos folder
# and add cmd_*command* to the line below
from commandos import cmd_hello, cmd_help, cmd_add
######################################################################################

######################################################################################
# You also need to add the new command here. the string in between the " " is the
# string the bot is going to react to
commandos = {
    "hello": cmd_hello,
    "help": cmd_help,
    "add": cmd_add  # example of a command which takes arguments: type '-add 1 2'
}
######################################################################################

# DO NOT CHANGE ANY CODE BELOW, UNLESS YOU KNOW WHAT YOU'RE DOING

######################################################################################

statics.intents.message_content = True
bot = commands.Bot(command_prefix=statics.prefix, intents=statics.intents)


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.content.startswith(statics.prefix):
        invoke = message.content[len(statics.prefix):].split(" ")[0]
        args = message.content.split(" ")[1:]
        if commandos.__contains__(invoke):
            cmd = commandos[invoke]
            await cmd.ex(args, bot, message)


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    await bot.change_presence(activity=discord.Game(name='-help'))
    channel = bot.get_channel(statics.channel_id)
    debug = bot.get_channel(statics.debug_id)
    await debug.send("I'm Online")
    if statics.use_db:
        await create_initial_db()
        await fill_initial_data_db(statics.mod_ids, statics.mod_info_url, statics.headers, debug)
        await asyncio.sleep(10)
        await check_for_updates_db(channel, debug, statics.mod_ids, statics.mod_info_url, statics.headers,
                                   statics.changelog_base_url, statics.sleeptime)
    else:
        await make_initial_request_and_fill_file(statics.mod_ids, statics.mod_info_url, statics.headers, debug,
                                                 statics.filepath)
        await asyncio.sleep(10)
        await check_for_updates(channel, debug, statics.mod_ids, statics.mod_info_url,
                                statics.headers, statics.filepath, statics.changelog_base_url, statics.sleeptime)


bot.run(secrets.bot_token)
