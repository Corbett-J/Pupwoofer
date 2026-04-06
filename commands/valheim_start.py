import os


def valheim_start():
    os.chdir("C:\\steamcmd\\steamapps\\common\\Valheim dedicated server")
    os.startfile("start_headless_server.bat")

