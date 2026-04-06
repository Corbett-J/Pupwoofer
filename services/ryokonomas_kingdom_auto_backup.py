import asyncio
import json
from datetime import datetime, timedelta, time
from discord.ext import commands

from config import SECRETS_FILE_PATH, SAVE_FILE_PATH

from commands.ryo_start import ryo_start
from commands.ryo_stop import ryo_stop
from commands.ryo_backup import ryo_backup

async def ryokonomas_kingdom_auto_backup(bot: commands.Bot):
    with open(SECRETS_FILE_PATH, "r") as secrets_file:
            secrets = json.load(secrets_file)
    beckrock_server_root_path: str = secrets["beckrock_server_root_path"]

    backup_schedule_path = f"{beckrock_server_root_path}\\backup-schedule.json"

    
    with open(backup_schedule_path, 'r') as save_file:
        backup_schedule = json.load(save_file)
    backup_times = []
    for backup_time in sorted(backup_schedule["backup_times"]):
        backup_times.append(time(backup_time))
    warning_intervals = sorted(backup_schedule["warning_intervals"], reverse=True)
    print("backup_times: ", backup_times)
    print("warning_intervals: ", warning_intervals)

    next_backup_time = None
    while True:
        time_now = datetime.now().time()
        date_time_now = datetime.combine(datetime.today().date(), time_now)

        is_next_backup_tomorrow = backup_times[-1] < time_now
        
        if  (next_backup_time is None) or (next_backup_time < time_now):
            if is_next_backup_tomorrow:
                next_backup_time = backup_times[0]
            else:
                for backup_time in backup_times:
                    if time_now < backup_time:
                        next_backup_time = backup_time
                        break
        print("next_backup_time: ", next_backup_time)
        
        if is_next_backup_tomorrow:
            date_time_next_backup = datetime.combine(datetime.today().date(), next_backup_time) + timedelta(days=1)
        else:
            date_time_next_backup = datetime.combine(datetime.today().date(), next_backup_time)
        print("date_time_next_backup: ", date_time_next_backup)
        
        time_until_next_backup = round((date_time_next_backup -  date_time_now).total_seconds())
        print("time_until_next_backup: ", time_until_next_backup)
        
        if time_until_next_backup <= 1:
            bot.ryokonomas_kingdom_server_process = ryo_stop(bot.ryokonomas_kingdom_server_process)
            with open(SAVE_FILE_PATH, 'r') as save_file:
                save_data = json.load(save_file)
            current_version_name = save_data["minecraft_bedrock"]["current_version_name"]
            ryo_backup(current_version_name)
            bot.ryokonomas_kingdom_server_process = ryo_start(bot.ryokonomas_kingdom_server_process, current_version_name)
            return
        
        for index, warning_interval in enumerate(warning_intervals):
            print("warning_interval: ", warning_interval)
            if time_until_next_backup > warning_interval:
                sleep_time = time_until_next_backup - warning_interval
                print("IN time_until_next_backup > warning_interval")
                print("sleeping for ", sleep_time)
                await asyncio.sleep(sleep_time)
                break
            elif time_until_next_backup == warning_interval:
                if bot.ryokonomas_kingdom_server_process is not None:
                    if time_until_next_backup > 60:
                        warning_time = time_until_next_backup / 60
                        warning_time_units = "minutes"
                    if time_until_next_backup == 60:
                        warning_time = time_until_next_backup / 60
                        warning_time_units = "minute"
                    if time_until_next_backup < 60:
                        warning_time = time_until_next_backup
                        warning_time_units = "seconds"
                    minecraft_warning_message = f"say Backup will occur in {warning_time} {warning_time_units}. This will restart the server, and you will have to reconnect.\n"
                    bot.ryokonomas_kingdom_server_process.stdin.write(minecraft_warning_message.encode())
                sleep_time = time_until_next_backup - (warning_intervals[index + 1] or warning_intervals[index])
                print("IN time_until_next_backup == warning_interval")
                print("sleeping for ", sleep_time)
                await asyncio.sleep(sleep_time)
                break


async def setup(bot: commands.Bot):
    await teardown(bot)
    bot.ryokonomas_kingdom_auto_backup_loop = bot.loop.create_task(ryokonomas_kingdom_auto_backup(bot))
    


async def teardown(bot: commands.Bot):
    if bot.ryokonomas_kingdom_auto_backup_loop is type(asyncio.Task) :
        bot.ryokonomas_kingdom_auto_backup_loop.cancel()
        try:
            await bot.ryokonomas_kingdom_auto_backup_loop
        except asyncio.CancelledError:
            pass
        bot.ryokonomas_kingdom_auto_backup_loop = None
