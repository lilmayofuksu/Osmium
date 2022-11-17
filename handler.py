import asyncio
import json
import inspect
import enum
import base64

import betterproto
from websockets.server import WebSocketServerProtocol

from out import proto

class PacketDirection(enum.Enum):
    Send = 0
    Receive = 1

cmdid_map: dict[int, betterproto.Message] = {}

def _is_cmdid_enum(object):
    return inspect.isclass(object) and object.__name__.endswith("CmdId")

def initCmdIdMap():
    for _, type in inspect.getmembers(proto, _is_cmdid_enum):
        cmdid_map[type.CMD_ID] = getattr(proto, type.__name__.replace("CmdId", ""))

async def handleJsonPacket(data: str, ws: WebSocketServerProtocol):
    json_data = json.loads(base64.b64decode(data).decode("utf-8"))
    parsed_packets = []

    for packet in json_data["packets"]:
        cmd_id = packet["cmd_id"]
        ts = packet["timestamp"]
        proto_data = base64.b64decode(packet["raw_content"])
        direction = PacketDirection(packet["direction"]["value"])

        message: betterproto.Message = cmdid_map[cmd_id]()
        message.parse(proto_data)

        packet_obj = {
            "packetID": cmd_id,
            "protoName": cmdid_map[cmd_id].__name__,
            "object": message.to_dict(),
            "packet": packet["raw_content"],
            "source": not direction.value,
            "time": ts
        }

        await ws.send(json.dumps({"cmd":"PacketNotify", "data": [packet_obj] }))
