import asyncio
from doctest import debug

async def ryo_stop(ryokonomas_kingdom_server_process: asyncio.subprocess.Process | None) -> None:
    if ryokonomas_kingdom_server_process is None:
        return None

    ryokonomas_kingdom_server_process.stdin.write(b"stop\n")
    await ryokonomas_kingdom_server_process.stdin.drain()

    server_stopped = False
    while not server_stopped:
        stdout_current_line = await ryokonomas_kingdom_server_process.stdout.readline()
        if not stdout_current_line:
                break
        decoded_current_line = stdout_current_line.decode(errors="ignore").strip()

        if "Quit correctly" in decoded_current_line:
            server_stopped = True
    
    ryokonomas_kingdom_server_process.kill()
    await ryokonomas_kingdom_server_process.wait()
    print("Ryo kingdom offline")
    return None
