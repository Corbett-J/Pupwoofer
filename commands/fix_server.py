import os


def fix_server():
    os.system('taskkill /F /IM playit.exe')
    os.system('start "playit-opener" "C:\\Program Files\\playit_gg\\bin\\playit.exe"')

