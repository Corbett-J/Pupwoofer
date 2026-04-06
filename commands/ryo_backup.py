import datetime
import shutil


def ryo_backup(current_version_name):
    print("Ryo kingdom backing up")
    backup_date_time = str(datetime.datetime.now()).replace(':', '.')
    
    path_to_mcb = "C:\\Users\\Server\\Desktop\\minecraft_bedrock"
    path_to_mcb_current_version = path_to_mcb + "\\" + current_version_name
    path_to_new_backup = path_to_mcb + "\\_backups" + "\\" + backup_date_time
    
    shutil.copytree(path_to_mcb_current_version + "\\worlds", path_to_new_backup + "\\worlds")
    shutil.copy(path_to_mcb_current_version + "\\allowlist.json", path_to_new_backup)
    shutil.copy(path_to_mcb_current_version + "\\packetlimitconfig.json", path_to_new_backup)
    shutil.copy(path_to_mcb_current_version + "\\permissions.json", path_to_new_backup)
    shutil.copy(path_to_mcb_current_version + "\\profanity_filter.wlist", path_to_new_backup)
    shutil.copy(path_to_mcb_current_version + "\\server.properties", path_to_new_backup)
    print("Ryo kingdom backed up")
    
    return backup_date_time

