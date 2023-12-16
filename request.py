import requests
import json
import discord
import asyncio
from datetime import datetime


async def make_initial_request_and_fill_file(mod_ids, mod_info_url, headers, debug, filepath):
    try:
        with open(filepath, 'r') as file:
            initial_data = json.load(file)
    except FileNotFoundError:
        initial_data = {}
    for mod_id in mod_ids:
        mod_id = str(mod_id)
        if mod_id in initial_data:
            print(f'Skipped Mod ID {mod_id}: Entry already exists in the file')
            continue
        mod_url = mod_info_url.format(mod_id)
        response = requests.get(mod_url, headers=headers)
        if response.status_code == 200:
            print(f'Initial Request for Mod ID {mod_id} successful!')
            response_data = response.json()
            mod_name = response_data['data']['name']
            latest_files = response_data['data']['latestFiles']
            latest_file_info = latest_files[0]
            initial_data[mod_id] = {
                "mod-name": mod_name,
                "latest-file": latest_file_info['displayName'],
                "latest-date": latest_file_info['fileDate']
            }
        else:
            print(f'Mod Request failed for Mod ID {mod_id}:', response.status_code)
            await debug.send(f"Mod Request failed for Mod ID {mod_id}: {response.status_code}")
    with open(filepath, 'w') as file:
        json.dump(initial_data, file, indent=4)


async def check_for_updates(channel, debug, mod_ids, mod_info_url, headers, filepath, changelog_base_url, sleeptime):
    while True:
        update_data = {}
        for mod_id in mod_ids:
            mod_id = str(mod_id)
            mod_url = mod_info_url.format(mod_id)
            response = requests.get(mod_url, headers=headers)
            if response.status_code == 200:
                print(f'Request for Mod ID {mod_id} successful!')
                response_data = response.json()
                mod_name = response_data['data']['name']
                latest_files = response_data['data']['latestFiles']
                mod_cf_url = response_data['data']['links']['websiteUrl']
                icon = response_data['data']['logo']['url']
                with open(filepath, 'r') as file:
                    try:
                        file_data = json.load(file)
                    except json.JSONDecodeError:
                        file_data = {}
                file_date_old = None
                if str(mod_id) in file_data:
                    file_date_old = datetime.strptime(file_data[str(mod_id)]['latest-date'], '%Y-%m-%dT%H:%M:%S.%fZ')
                update_found = False
                for file_info in latest_files:
                    file_date = file_info['fileDate']
                    current_date = datetime.strptime(file_date, '%Y-%m-%dT%H:%M:%S.%fZ')
                    if file_date_old is None or current_date > file_date_old:
                        update_found = True
                        file_id = file_info['id']
                        break
                if update_found:
                    update_data[mod_id] = {
                        "mod-name": mod_name,
                        "latest-file": latest_files[0]['displayName'],
                        "latest-date": latest_files[0]['fileDate']
                    }
                    changelog_url = changelog_base_url.format(mod_id, file_id)
                    changelog_response = requests.get(changelog_url, headers=headers)
                    if changelog_response.status_code == 200:
                        changelog_weburl = f"**For the full changelog visit:**\n{mod_cf_url}/files/{file_id}"
                        max_chars = 1024
                        changelog_data = changelog_response.json()
                        changes = changelog_data['data']
                        changes = changes.replace('<p>', '').replace('</p>', '\n').replace('<br>', '\n')
                        version, *changes_lines = changes.split('\n', 1)
                        changes = '\n'.join(changes_lines)
                        embed = discord.Embed(title='Update has been published!', color=discord.Color.green())
                        if len(changes) > max_chars:
                            last_newline_index = changes.rfind('\n', 0, max_chars)
                            if last_newline_index != -1:
                                changes = f'{changes[:last_newline_index]}'
                            else:
                                changes = f'{changes[:max_chars - len(changelog_weburl)]}'
                            embed.add_field(name=version, value=changes, inline=False)
                            embed.add_field(name="...", value=changelog_weburl, inline=False)
                        else:
                            embed.add_field(name=version, value=changes, inline=False)
                        embed.add_field(name="Mod-URL", value=mod_cf_url, inline=False)
                        embed.set_author(name=mod_name)
                        embed.set_thumbnail(url=icon)
                        await channel.send(embed=embed)
                    else:
                        print(f'Changelog Request failed for Mod ID {mod_id}:', changelog_response.status_code)
                        await debug.send(
                            f"Changelog Request failed for Mod ID {mod_id}: {changelog_response.status_code}")
            else:
                print(f'Mod Request failed for Mod ID {mod_id}:', response.status_code)
                await debug.send(f"Mod Request failed for Mod ID {mod_id}: {response.status_code}")
        if update_data:
            with open(filepath, 'r+') as file:
                try:
                    file_data = json.load(file)
                except json.JSONDecodeError:
                    file_data = {}
                file_data.update(update_data)
                file.seek(0)
                json.dump(file_data, file, indent=4)
                file.truncate()
        await asyncio.sleep(sleeptime)
