little discord bot which periodically checks if there was an update released for your mods.  
  
If there is an update it posts an embed message into a specified channel together with the changelogs.  
check https://discordpy.readthedocs.io/en/stable/intro.html and https://discordpy.readthedocs.io/en/stable/discord.html for the general discord.py setup guide  
  
The "old" bot can be found in... "oldbot > bot.py"  

You need to edit the `secrets.py` where you enter the CF API token and the bot token  
Settings can be found in the `statics.py`  
If you want to add additional commands check the `main.py`  
  
to start the bot install the dependencies listed down below and run `python3 main.py`  

### Dependencies:  
  
discord.py   
aiosqlite  
requests  

