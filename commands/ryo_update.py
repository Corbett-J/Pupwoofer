import requests
import zipfile
import io
import shutil


def ryo_update(backup_date_time, old_version_name):
    
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0'}
    
    dl_links_response = requests.get("https://net-secondary.web.minecraft-services.net/api/v1.0/download/links", headers=headers)
    dl_links_data = dl_links_response.json()
    links = dl_links_data["result"]["links"]
    
    download_url = ""
    
    for link in links:
        if link["downloadType"] == "serverBedrockWindows":
            download_url = link["downloadUrl"]
            
    if not download_url:
        return "error: no download url found. Tell Fox 3,:"
        
    new_version_name = download_url.split("/")[-1].replace(".zip", "")
    
    if old_version_name == new_version_name:
        return "error: The server appears to be up-to-date. Old version name matches new version name, '" + old_version_name + "' == '" + new_version_name + "'"
        
    dowload_response = requests.get(download_url, headers=headers)
    dowload_zip = zipfile.ZipFile(io.BytesIO(dowload_response.content))
    path_to_mcb = "C:\\Users\\Server\\Desktop\\minecraft_bedrock"
    dowload_zip.extractall(path_to_mcb + "\\" + new_version_name)
    
    path_to_backup = path_to_mcb + "\\_backups" + "\\" + backup_date_time
    path_to_mcb_new_version = path_to_mcb + "\\" + new_version_name
    
    shutil.copytree( path_to_backup + "\\worlds", path_to_mcb_new_version + "\\worlds")
    shutil.copy(path_to_backup + "\\allowlist.json", path_to_mcb_new_version)
    shutil.copy(path_to_backup + "\\packetlimitconfig.json", path_to_mcb_new_version)
    shutil.copy(path_to_backup + "\\permissions.json", path_to_mcb_new_version)
    shutil.copy(path_to_backup + "\\profanity_filter.wlist", path_to_mcb_new_version)
    shutil.copy(path_to_backup + "\\server.properties", path_to_mcb_new_version)
    
    
    
    return new_version_name
