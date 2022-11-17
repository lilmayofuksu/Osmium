import websockets
from websockets.server import WebSocketServerProtocol
from loguru import logger

import asyncio
import json

from handler import handleJsonPacket, initCmdIdMap

background_tasks = set()

async def onPacket(ws: WebSocketServerProtocol):
    async for data in ws:
        message = json.loads(data)
        ip_addr, port = (None, None)
        if len(ws.remote_address) == 2:
            ip_addr, port = ws.remote_address

        match message["cmd"]:
            case "ConnectReq":
                logger.info(f"[{message['cmd']}] New connection from {ip_addr if ip_addr else ''}:{port if port else ''}")
                msg = json.dumps({"cmd": "ConnectRsp", "data": {"sessionStarted": False}})
                await ws.send(msg)

            case "ProcessFileReq":
                file_name = message["data"]["name"]
                file_data = message["data"]["data"]
                file_ext = message["data"]["ext"]
                logger.info(f"[{message['cmd']}] {file_name}")

                match file_ext:
                    case "json":
                        task = asyncio.create_task(handleJsonPacket(data=file_data, ws=ws))
                        background_tasks.add(task)
                        task.add_done_callback(background_tasks.discard)
                    case _:
                        ...

            case _:
                ...


async def main():
    logger.info(f"Starting websocket server")
    initCmdIdMap()
    async with websockets.serve(onPacket, "localhost", 40510, max_size = 204800 * 1024):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())