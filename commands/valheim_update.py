import os


def valheim_update():
    os.system('C:\steamcmd\steamcmd.exe +login anonymous +app_update 896660 -beta public-test -betapassword yesimadebackups validate +exit')

