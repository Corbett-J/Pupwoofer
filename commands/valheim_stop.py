import os


def valheim_stop():
    os.system('taskkill /F /IM valheim_server.exe')

