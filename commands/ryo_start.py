import asyncio
import json

from config import SECRETS_FILE_PATH

async def ryo_start(ryokonomas_kingdom_server_process: asyncio.subprocess.Process | None, version_name: str) -> asyncio.subprocess.Process | None:
    if ryokonomas_kingdom_server_process is not None:
        return ryokonomas_kingdom_server_process
    
    with open(SECRETS_FILE_PATH, "r") as secrets_file:
            secrets = json.load(secrets_file)
    beckrock_server_root_path: str = secrets["beckrock_server_root_path"]

    beckrock_server_exe_path = f"{beckrock_server_root_path}\\{version_name}\\bedrock_server.exe"
    ryokonomas_kingdom_server_process = await asyncio.create_subprocess_exec(
        beckrock_server_exe_path,
        stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.STDOUT,
    )

    server_started = False
    while not server_started:
        stdout_current_line = await ryokonomas_kingdom_server_process.stdout.readline()
        if not stdout_current_line:
                break
        decoded_current_line = stdout_current_line.decode(errors="ignore").strip()

        if "Server started." in decoded_current_line:
            server_started = True
        elif "Exiting program" in decoded_current_line:
            ryokonomas_kingdom_server_process.kill()
            await ryokonomas_kingdom_server_process.wait()
            return None
    print("Ryo kingdom online")
    return ryokonomas_kingdom_server_process

