# Generated by the protocol buffer compiler.  DO NOT EDIT!
# sources: server_only/SVOProto.proto
# plugin: python-betterproto
from dataclasses import dataclass
from typing import List

import betterproto

from .. import (
    ToTheMoonProtoPos as _ToTheMoonProtoPos__,
    ToTheMoonProtoSvoBlockProto as _ToTheMoonProtoSvoBlockProto__,
    ToTheMoonProtoSvoLayerProto as _ToTheMoonProtoSvoLayerProto__,
    ToTheMoonProtoSvoNodeProto as _ToTheMoonProtoSvoNodeProto__,
    ToTheMoonProtoSvoNodeWrapperProto as _ToTheMoonProtoSvoNodeWrapperProto__,
    ToTheMoonProtoSvoStructureProto as _ToTheMoonProtoSvoStructureProto__,
)


@dataclass(eq=False, repr=False)
class Pos(betterproto.Message):
    x: float = betterproto.float_field(1)
    y: float = betterproto.float_field(2)
    z: float = betterproto.float_field(3)


@dataclass(eq=False, repr=False)
class SvoNodeProto(betterproto.Message):
    area: int = betterproto.int32_field(1)
    morton_index: int = betterproto.int64_field(2)
    parent: int = betterproto.int64_field(3)
    children: int = betterproto.int64_field(4)
    child_num: int = betterproto.int32_field(5)
    neighbors: List[int] = betterproto.int64_field(6)
    neighbors_level: List[int] = betterproto.int32_field(7)
    planar_neighbors: List[int] = betterproto.int64_field(8)
    planar_neighbors_level: List[int] = betterproto.int32_field(9)
    diagonal_neighbors: List[int] = betterproto.int64_field(10)
    diagonal_neighbors_level: List[int] = betterproto.int32_field(11)


@dataclass(eq=False, repr=False)
class SvoLayerProto(betterproto.Message):
    level: int = betterproto.int32_field(1)
    node_data: List["_ToTheMoonProtoSvoNodeProto__"] = betterproto.message_field(2)


@dataclass(eq=False, repr=False)
class SvoStructureProto(betterproto.Message):
    base_pos: "_ToTheMoonProtoPos__" = betterproto.message_field(1)
    layer_data: List["_ToTheMoonProtoSvoLayerProto__"] = betterproto.message_field(2)
    total_index: List[int] = betterproto.int32_field(3)


@dataclass(eq=False, repr=False)
class SvoBlockProto(betterproto.Message):
    svo: "_ToTheMoonProtoSvoStructureProto__" = betterproto.message_field(1)
    scene_id: int = betterproto.int32_field(2)
    block_index: List[int] = betterproto.int32_field(3)


@dataclass(eq=False, repr=False)
class SvoWorldProto(betterproto.Message):
    blocks: List["_ToTheMoonProtoSvoBlockProto__"] = betterproto.message_field(1)
    side_length: float = betterproto.float_field(2)
    scene_id: int = betterproto.int32_field(3)


@dataclass(eq=False, repr=False)
class SvoNodeWrapperProto(betterproto.Message):
    svo_node: "_ToTheMoonProtoSvoNodeProto__" = betterproto.message_field(1)
    level: int = betterproto.int32_field(2)


@dataclass(eq=False, repr=False)
class SvoNodePathProto(betterproto.Message):
    start: "_ToTheMoonProtoPos__" = betterproto.message_field(1)
    end: "_ToTheMoonProtoPos__" = betterproto.message_field(2)
    svo_nodes: List["_ToTheMoonProtoSvoNodeWrapperProto__"] = betterproto.message_field(
        3
    )