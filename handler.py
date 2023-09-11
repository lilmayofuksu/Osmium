import asyncio
import json
import inspect
import enum
import base64
from typing import Union

import betterproto
from loguru import logger
from websockets.server import WebSocketServerProtocol

from out import proto

class PacketDirection(enum.Enum):
    Send = 0
    Receive = 1

cmdid_map: dict[int, betterproto.Message] = {}

def _is_cmdid_enum(object) -> bool:
    return inspect.isclass(object) and object.__name__.endswith("CmdId")

def initCmdIdMap() -> None:
    for _, type in inspect.getmembers(proto, _is_cmdid_enum):
        cmdid_map[type.CMD_ID] = getattr(
            proto, type.__name__.replace("CmdId", ""))

def getAbilityInvokeProto(argument_type: proto.AbilityInvokeArgument) -> betterproto.Message:
    match argument_type:
        case proto.AbilityInvokeArgument.ABILITY_META_MODIFIER_CHANGE:
            return proto.AbilityMetaModifierChange
        case proto.AbilityInvokeArgument.ABILITY_META_COMMAND_MODIFIER_CHANGE_REQUEST:
            return None
        case proto.AbilityInvokeArgument.ABILITY_META_SPECIAL_FLOAT_ARGUMENT:
            return proto.AbilityMetaSpecialFloatArgument
        case proto.AbilityInvokeArgument.ABILITY_META_OVERRIDE_PARAM:
            return proto.AbilityScalarValueEntry
        case proto.AbilityInvokeArgument.ABILITY_META_CLEAR_OVERRIDE_PARAM:
            return proto.AbilityScalarValueEntry
        case proto.AbilityInvokeArgument.ABILITY_META_MODIFIER_DURABILITY_CHANGE:
            return proto.AbilityMetaModifierDurabilityChange
        case proto.AbilityInvokeArgument.ABILITY_META_UPDATE_BASE_REACTION_DAMAGE:
            return proto.AbilityMetaUpdateBaseReactionDamage
        case proto.AbilityInvokeArgument.ABILITY_META_SET_POSE_PARAMETER:
            return proto.AbilityMetaSetPoseParameter
        case proto.AbilityInvokeArgument.ABILITY_META_REINIT_OVERRIDEMAP:
            return proto.AbilityMetaReInitOverrideMap
        case proto.AbilityInvokeArgument.ABILITY_META_GLOBAL_FLOAT_VALUE:
            return proto.AbilityScalarValueEntry
        case proto.AbilityInvokeArgument.ABILITY_META_CLEAR_GLOBAL_FLOAT_VALUE:
            return proto.AbilityScalarValueEntry
        case proto.AbilityInvokeArgument.ABILITY_META_ABILITY_ELEMENT_STRENGTH:
            return None
        case proto.AbilityInvokeArgument.ABILITY_META_ADD_OR_GET_ABILITY_AND_TRIGGER:
            return proto.AbilityMetaAddOrGetAbilityAndTrigger
        case proto.AbilityInvokeArgument.ABILITY_META_SET_KILLED_SETATE:
            return proto.AbilityMetaSetKilledState
        case proto.AbilityInvokeArgument.ABILITY_META_SET_ABILITY_TRIGGER:
            return proto.AbilityMetaSetAbilityTrigger
        case proto.AbilityInvokeArgument.ABILITY_META_ADD_NEW_ABILITY:
            return proto.AbilityMetaAddAbility
        case proto.AbilityInvokeArgument.ABILITY_META_REMOVE_ABILITY:
            return None
        case proto.AbilityInvokeArgument.ABILITY_META_SET_MODIFIER_APPLY_ENTITY:
            return proto.AbilityMetaSetModifierApplyEntityId
        case proto.AbilityInvokeArgument.ABILITY_META_MODIFIER_DURABILITY_CHANGE:
            return proto.AbilityMetaModifierDurabilityChange
        case proto.AbilityInvokeArgument.ABILITY_META_ELEMENT_REACTION_VISUAL:
            return proto.AbilityMetaElementReactionVisual
        case proto.AbilityInvokeArgument.ABILITY_META_SET_POSE_PARAMETER:
            return proto.AbilityMetaSetPoseParameter
        case proto.AbilityInvokeArgument.ABILITY_META_UPDATE_BASE_REACTION_DAMAGE:
            return proto.AbilityMetaUpdateBaseReactionDamage
        case proto.AbilityInvokeArgument.ABILITY_META_TRIGGER_ELEMENT_REACTION:
            return proto.AbilityMetaTriggerElementReaction
        case proto.AbilityInvokeArgument.ABILITY_META_LOSE_HP:
            return proto.AbilityMetaLoseHp
        case proto.AbilityInvokeArgument.ABILITY_META_DURABILITY_IS_ZERO:
            return proto.AbilityMetaDurabilityIsZero

        case proto.AbilityInvokeArgument.ABILITY_ACTION_TRIGGER_ABILITY:
            return proto.AbilityActionTriggerAbility
        case proto.AbilityInvokeArgument.ABILITY_ACTION_SET_CRASH_DAMAGE:
            return proto.AbilityActionSetCrashDamage
        case proto.AbilityInvokeArgument.ABILITY_ACTION_EFFECT:
            return None
        case proto.AbilityInvokeArgument.ABILITY_ACTION_SUMMON:
            return proto.AbilityActionSummon
        case proto.AbilityInvokeArgument.ABILITY_ACTION_BLINK:
            return proto.AbilityActionBlink
        case proto.AbilityInvokeArgument.ABILITY_ACTION_CREATE_GADGET:
            return proto.AbilityActionCreateGadget
        case proto.AbilityInvokeArgument.ABILITY_ACTION_APPLY_LEVEL_MODIFIER:
            return proto.AbilityApplyLevelModifier
        case proto.AbilityInvokeArgument.ABILITY_ACTION_GENERATE_ELEM_BALL:
            return proto.AbilityActionGenerateElemBall
        case proto.AbilityInvokeArgument.ABILITY_ACTION_SET_RANDOM_OVERRIDE_MAP_VALUE:
            return proto.AbilityActionSetRandomOverrideMapValue
        case proto.AbilityInvokeArgument.ABILITY_ACTION_SERVER_MONSTER_LOG:
            return proto.AbilityActionServerMonsterLog
        case proto.AbilityInvokeArgument.ABILITY_ACTION_CREATE_TILE:
            return proto.AbilityActionCreateTile
        case proto.AbilityInvokeArgument.ABILITY_ACTION_DESTROY_TILE:
            return proto.AbilityActionDestroyTile
        case proto.AbilityInvokeArgument.ABILITY_ACTION_FIRE_AFTER_IMAGE:
            return proto.AbilityActionFireAfterImgae
        case proto.AbilityInvokeArgument.ABILITY_ACTION_DEDUCT_STAMINA:
            return proto.AbilityActionDeductStamina
        case proto.AbilityInvokeArgument.ABILITY_ACTION_HIT_EFFECT:
            return proto.AbilityActionHitEffect
        case proto.AbilityInvokeArgument.ABILITY_ACTION_SET_BULLET_TRACK_TARGET:
            return proto.AbilityActionSetBulletTrackTarget

        case proto.AbilityInvokeArgument.ABILITY_MIXIN_AVATAR_STEER_BY_CAMERA:
            return proto.AbilityMixinAvatarSteerByCamera
        case proto.AbilityInvokeArgument.ABILITY_MIXIN_MONSTER_DEFEND:
            return None
        case proto.AbilityInvokeArgument.ABILITY_MIXIN_WIND_ZONE:
            return proto.AbilityMixinWindZone
        case proto.AbilityInvokeArgument.ABILITY_MIXIN_COST_STAMINA:
            return proto.AbilityMixinCostStamina
        case proto.AbilityInvokeArgument.ABILITY_MIXIN_ELITE_SHIELD:
            return proto.AbilityMixinEliteShield
        case proto.AbilityInvokeArgument.ABILITY_MIXIN_ELEMENT_SHIELD:
            return proto.AbilityMixinElementShield
        case proto.AbilityInvokeArgument.ABILITY_MIXIN_GLOBAL_SHIELD:
            return proto.AbilityMixinGlobalShield
        case proto.AbilityInvokeArgument.ABILITY_MIXIN_SHIELD_BAR:
            return proto.AbilityMixinShieldBar
        case proto.AbilityInvokeArgument.ABILITY_MIXIN_WIND_SEED_SPAWNER:
            return proto.AbilityMixinWindSeedSpawner
        case proto.AbilityInvokeArgument.ABILITY_MIXIN_DO_ACTION_BY_ELEMENT_REACTION:
            return proto.AbilityMixinDoActionByElementReaction
        case proto.AbilityInvokeArgument.ABILITY_MIXIN_FIELD_ENTITY_COUNT_CHANGE:
            return proto.AbilityMixinFieldEntityCountChange
        case proto.AbilityInvokeArgument.ABILITY_MIXIN_SCENE_PROP_SYNC:
            return proto.AbilityMixinScenePropSync
        case proto.AbilityInvokeArgument.ABILITY_MIXIN_WIDGET_MP_SUPPORT:
            return proto.AbilityMixinWidgetMpSupport
        case proto.AbilityInvokeArgument.ABILITY_MIXIN_DO_ACTION_BY_SELF_MODIFIER_ELEMENT_DURABILITY_RATIO:
            return proto.AbilityMixinDoActionBySelfModifierElementDurabilityRatio
        case proto.AbilityInvokeArgument.ABILITY_MIXIN_FIREWORKS_LAUNCHER:
            return proto.AbilityMixinFireworksLauncher
        case proto.AbilityInvokeArgument.ABILITY_MIXIN_ATTACK_RESULT_CREATE_COUNT:
            return proto.AttackResultCreateCount
        case proto.AbilityInvokeArgument.ABILITY_MIXIN_UGC_TIME_CONTROL:
            return proto.AbilityMixinUgcTimeControl
        case proto.AbilityInvokeArgument.ABILITY_MIXIN_AVATAR_COMBAT:
            return proto.AbilityMixinAvatarCombat
        case proto.AbilityInvokeArgument.ABILITY_MIXIN_DEATH_ZONE_REGIONAL_PLAY_MIXIN:
            return None
        case proto.AbilityInvokeArgument.ABILITY_MIXIN_UI_INTERACT:
            return proto.AbilityMixinUiInteract
        case proto.AbilityInvokeArgument.ABILITY_MIXIN_SHOOT_FROM_CAMERA:
            return proto.AbilityMixinShootFromCamera
        case proto.AbilityInvokeArgument.ABILITY_MIXIN_ERASE_BRICK_ACTIVITY:
            return proto.AbilityMixinEraseBrickActivity

        case _:
            return None

def getCombatInvokeProto(argument_type: proto.CombatTypeArgument) -> betterproto.Message:
    match argument_type:
        case proto.CombatTypeArgument.COMBAT_EVT_BEING_HIT:
            return proto.EvtBeingHitInfo
        case proto.CombatTypeArgument.COMBAT_ANIMATOR_STATE_CHANGED:
            return proto.EvtAnimatorStateChangedInfo
        case proto.CombatTypeArgument.COMBAT_FACE_TO_DIR:
            return proto.EvtFaceToDirInfo
        case proto.CombatTypeArgument.COMBAT_SET_ATTACK_TARGET:
            return proto.EvtSetAttackTargetInfo
        case proto.CombatTypeArgument.COMBAT_RUSH_MOVE:
            return proto.EvtRushMoveInfo
        case proto.CombatTypeArgument.COMBAT_ANIMATOR_PARAMETER_CHANGED:
            return proto.EvtAnimatorParameterInfo
        case proto.CombatTypeArgument.ENTITY_MOVE:
            return proto.EntityMoveInfo
        case proto.CombatTypeArgument.SYNC_ENTITY_POSITION:
            return proto.EvtSyncEntityPositionInfo
        case proto.CombatTypeArgument.COMBAT_STEER_MOTION_INFO:
            return proto.EvtCombatSteerMotionInfo
        case proto.CombatTypeArgument.COMBAT_FORCE_SET_POS_INFO:
            return proto.EvtCombatForceSetPosInfo
        case proto.CombatTypeArgument.COMBAT_COMPENSATE_POS_DIFF:
            return proto.EvtCompensatePosDiffInfo
        case proto.CombatTypeArgument.COMBAT_MONSTER_DO_BLINK:
            return proto.EvtMonsterDoBlink
        case proto.CombatTypeArgument.COMBAT_FIXED_RUSH_MOVE:
            return proto.EvtFixedRushMove
        case proto.CombatTypeArgument.COMBAT_SYNC_TRANSFORM:
            return proto.EvtSyncTransform
        case proto.CombatTypeArgument.COMBAT_LIGHT_CORE_MOVE:
            return proto.EvtLightCoreMove            
        case proto.CombatTypeArgument.COMBAT_BEING_HEALED_NTF:
            return proto.EvtBeingHealedNotify
        case proto.CombatTypeArgument.COMBAT_SKILL_ANCHOR_POSITION_NTF:
            return proto.EvtSyncSkillAnchorPosition
        case proto.CombatTypeArgument.COMBAT_GRAPPLING_HOOK_MOVE:
            return proto.EvtGrapplingHookMove

def handleAbilityInvokes(message: proto.AbilityInvocationsNotify) -> list[dict]:
    invokes = []
    for invoke in message.invokes:
        invoke_obj = invoke.to_dict()

        if invoke_message := getAbilityInvokeProto(invoke.argument_type):
            invoke_msg_obj = invoke_message()
            invoke_msg_obj.parse(invoke.ability_data)
            invoke_obj["abilityObject"] = invoke_msg_obj.to_dict()
        else:
            if invoke.argument_type != 0:
                logger.warning(f"Unknown invoke argument: {invoke.argument_type}")

        invokes.append(invoke_obj)

    return invokes

def handleCombatInvokes(message: proto.CombatInvocationsNotify):
    invokes = []
    for invoke in message.invoke_list:
        invoke_obj = invoke.to_dict()

        if invoke_message := getCombatInvokeProto(invoke.argument_type):
            invoke_msg_obj = invoke_message()
            invoke_msg_obj.parse(invoke.combat_data)
            invoke_obj["combatObject"] = invoke_msg_obj.to_dict()
        else:
            if invoke.argument_type != 0:
                logger.warning(f"Unknown invoke argument: {invoke.argument_type}")

        invokes.append(invoke_obj)

    return invokes

def handleUnionCmd(message: proto.UnionCmdNotify, packet_obj: dict[str, object]):
    for idx, cmd in enumerate(message.cmd_list):
        if cmd.message_id in cmdid_map:
            cmd_message: Union[proto.CombatInvocationsNotify,
                               proto.AbilityInvocationsNotify] = cmdid_map[cmd.message_id]()
            cmd_message.parse(cmd.body)

            packet_obj["object"]["cmdList"][idx]["protoName"] = cmd_message.__class__.__name__
            match cmd_message.__class__.__name__:
                case "CombatInvocationsNotify":
                    packet_obj["object"]["cmdList"][idx]["invokes"] = handleCombatInvokes(cmd_message)
                case "AbilityInvocationsNotify":
                    packet_obj["object"]["cmdList"][idx]["invokes"] = handleAbilityInvokes(cmd_message)
                case _:
                    ...

async def handleJsonPacket(data: str, ws: WebSocketServerProtocol) -> None:
    json_data = json.loads(base64.b64decode(data).decode("utf-8"))

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

        if message.__class__.__name__ == "UnionCmdNotify":
            handleUnionCmd(message, packet_obj)

        await ws.send(json.dumps({"cmd": "PacketNotify", "data": [packet_obj]}))
