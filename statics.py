import discord
import secrets
import os

use_db = True  # If true the bot uses a DB instead of a textfile to check for the updates
prefix = '-'  # The prefix used for the bot to react to commands
channel_id = 123456789987654321  # Enter the channel ID the bot should post the updates
debug_id = 987654321123456789  # Enter the channel ID the bit should post Request error messages in
announce_messages = False  # If true the bot would automatically publish the messages. The channel needs to be an "announcement" channel
sleeptime = 300  # Time in seconds between the requests
mod_ids = [931119, 942024]  # Enter the projectIDs/modIDs of the mods you want to track here


######################################################################################

# DO NOT CHANGE ANY CODE BELOW, UNLESS YOU KNOW WHAT YOU'RE DOING

######################################################################################


filepath = os.path.abspath(__file__)
filepath = os.path.join(os.path.dirname(filepath), 'latest.txt')
mod_info_url = 'https://api.curseforge.com/v1/mods/{}'
changelog_base_url = 'https://api.curseforge.com/v1/mods/{}/files/{}/changelog'
headers = {
    'x-api-key': secrets.api_key
}

intents = discord.Intents.default()
