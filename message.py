from typing import Optional, Union, Tuple, List, Dict
from enum import Enum

from datetime import datetime

class PinnedChatPaidLevel(Enum):
    ONE = 'ONE'
    TWO = 'TWO'
    THREE = 'THREE'
    FOUR = 'FOUR'
    FIVE = 'FIVE'
    SIX = 'SIX'
    SEVEN = 'SEVEN'
    EIGHT = 'EIGHT'
    NINE = 'NINE'
    TEN = 'TEN'

class MsgID(Enum):
    pass

    ## msg_id do comando "NOTICE"
    #already_banned = 'already_banned'
    #already_emote_only_off = 'already_emote_only_off'
    #already_emote_only_on = 'already_emote_only_on'
    #already_followers_off = 'already_followers_off'
    #already_followers_on = 'already_followers_on'
    #already_r9k_off = 'already_r9k_off'
    #already_r9k_on = 'already_r9k_on'
    #already_slow_off = 'already_slow_off'
    #already_slow_on = 'already_slow_on'
    #already_subs_off = 'already_subs_off'
    #already_subs_on = 'already_subs_on'
    #autohost_receive = 'autohost_receive'
    #bad_ban_admin = 'bad_ban_admin'
    #bad_ban_anon = 'bad_ban_anon'
    #bad_ban_broadcaster = 'bad_ban_broadcaster'
    #bad_ban_mod = 'bad_ban_mod'
    #bad_ban_self = 'bad_ban_self'
    #bad_ban_staff = 'bad_ban_staff'
    #bad_commercial_error = 'bad_commercial_error'
    #bad_delete_message_broadcaster = 'bad_delete_message_broadcaster'
    #bad_delete_message_mod = 'bad_delete_message_mod'
    #bad_host_error = 'bad_host_error'
    #bad_host_hosting = 'bad_host_hosting'
    #bad_host_rate_exceeded = 'bad_host_rate_exceeded'
    #bad_host_rejected = 'bad_host_rejected'
    #bad_host_self = 'bad_host_self'
    #bad_mod_banned = 'bad_mod_banned'
    #bad_mod_mod = 'bad_mod_mod'
    #bad_slow_duration = 'bad_slow_duration'
    #bad_timeout_admin = 'bad_timeout_admin'
    #bad_timeout_anon = 'bad_timeout_anon'
    #bad_timeout_broadcaster = 'bad_timeout_broadcaster'
    #bad_timeout_duration = 'bad_timeout_duration'
    #bad_timeout_mod = 'bad_timeout_mod'
    #bad_timeout_self = 'bad_timeout_self'
    #bad_timeout_staff = 'bad_timeout_staff'
    #bad_unban_no_ban = 'bad_unban_no_ban'
    #bad_unhost_error = 'bad_unhost_error'
    #bad_unmod_mod = 'bad_unmod_mod'
    #bad_vip_grantee_banned = 'bad_vip_grantee_banned'
    #bad_vip_grantee_already_vip = 'bad_vip_grantee_already_vip'
    #bad_vip_max_vips_reached = 'bad_vip_max_vips_reached'
    #bad_vip_achievement_incomplete = 'bad_vip_achievement_incomplete'
    #bad_unvip_grantee_not_vip = 'bad_unvip_grantee_not_vip'
    #ban_success = 'ban_success'
    #cmds_available = 'cmds_available'
    #color_changed = 'color_changed'
    #commercial_success = 'commercial_success'
    #delete_message_success = 'delete_message_success'
    #delete_staff_message_success = 'delete_staff_message_success'
    #emote_only_off = 'emote_only_off'
    #emote_only_on = 'emote_only_on'
    #followers_off = 'followers_off'
    #followers_on = 'followers_on'
    #followers_on_zero = 'followers_on_zero'
    #host_off = 'host_off'
    #host_on = 'host_on'
    #host_receive = 'host_receive'
    #host_receive_no_count = 'host_receive_no_count'
    #host_target_went_offline = 'host_target_went_offline'
    #hosts_remaining = 'hosts_remaining'
    #invalid_user = 'invalid_user'
    #mod_success = 'mod_success'
    #msg_banned = 'msg_banned'
    #msg_bad_characters = 'msg_bad_characters'
    #msg_channel_blocked = 'msg_channel_blocked'
    #msg_channel_suspended = 'msg_channel_suspended'
    #msg_duplicate = 'msg_duplicate'
    #msg_emoteonly = 'msg_emoteonly'
    #msg_followersonly = 'msg_followersonly'
    #msg_followersonly_followed = 'msg_followersonly_followed'
    #msg_followersonly_zero = 'msg_followersonly_zero'
    #msg_r9k = 'msg_r9k'
    #msg_ratelimit = 'msg_ratelimit'
    #msg_rejected = 'msg_rejected'
    #msg_rejected_mandatory = 'msg_rejected_mandatory'
    #msg_requires_verified_phone_number = 'msg_requires_verified_phone_number'
    #msg_slowmode = 'msg_slowmode'
    #msg_subsonly = 'msg_subsonly'
    #msg_suspended = 'msg_suspended'
    #msg_timedout = 'msg_timedout'
    #msg_verified_email = 'msg_verified_email'
    #no_help = 'no_help'
    #no_mods = 'no_mods'
    #no_vips = 'no_vips'
    #not_hosting = 'not_hosting'
    #no_permission = 'no_permission'
    #r9k_off = 'r9k_off'
    #r9k_on = 'r9k_on'
    #raid_error_already_raiding = 'raid_error_already_raiding'
    #raid_error_forbidden = 'raid_error_forbidden'
    #raid_error_self = 'raid_error_self'
    #raid_error_too_many_viewers = 'raid_error_too_many_viewers'
    #raid_error_unexpected = 'raid_error_unexpected'
    #raid_notice_mature = 'raid_notice_mature'
    #raid_notice_restricted_chat = 'raid_notice_restricted_chat'
    #room_mods = 'room_mods'
    #slow_off = 'slow_off'
    #slow_on = 'slow_on'
    #subs_off = 'subs_off'
    #subs_on = 'subs_on'
    #timeout_no_timeout = 'timeout_no_timeout'
    #timeout_success = 'timeout_success'
    #tos_ban = 'tos_ban'
    #turbo_only_color = 'turbo_only_color'
    #unavailable_command = 'unavailable_command'
    #unban_success = 'unban_success'
    #unmod_success = 'unmod_success'
    #unraid_error_no_active_raid = 'unraid_error_no_active_raid'
    #unraid_error_unexpected = 'unraid_error_unexpected'
    #unraid_success = 'unraid_success'
    #unrecognized_cmd = 'unrecognized_cmd'
    #untimeout_banned = 'untimeout_banned'
    #untimeout_success = 'untimeout_success'
    #unvip_success = 'unvip_success'
    #usage_ban = 'usage_ban'
    #usage_clear = 'usage_clear'
    #Clear = 'Clear'
    #usage_color = 'usage_color'
    #Change = 'Change'
    #usage_commercial = 'usage_commercial'
    #Triggers = 'Triggers'
    #usage_disconnect = 'usage_disconnect'
    #Reconnects = 'Reconnects'
    #usage_delete = 'usage_delete'
    #usage_emote_only_off = 'usage_emote_only_off'
    #Disables = 'Disables'
    #usage_emote_only_on = 'usage_emote_only_on'
    #Enables = 'Enables'
    #usage_followers_off = 'usage_followers_off'
    #Disables = 'Disables'
    #usage_followers_on = 'usage_followers_on'
    #Enables = 'Enables'
    #usage_help = 'usage_help'
    #Lists = 'Lists'
    #usage_host = 'usage_host'
    #Host = 'Host'
    #usage_marker = 'usage_marker'
    #Adds = 'Adds'
    #usage_me = 'usage_me'
    #usage_mod = 'usage_mod'
    #usage_mods = 'usage_mods'
    #Lists = 'Lists'
    #usage_r9k_off = 'usage_r9k_off'
    #usage_r9k_on = 'usage_r9k_on'
    #usage_raid = 'usage_raid'
    #Raid = 'Raid'
    #Use = 'Use'
    #usage_slow_off = 'usage_slow_off'
    #Disables = 'Disables'
    #usage_slow_on = 'usage_slow_on'
    #Enables = 'Enables'
    #Use = 'Use'
    #usage_subs_off = 'usage_subs_off'
    #Disables = 'Disables'
    #usage_subs_on = 'usage_subs_on'
    #Enables = 'Enables'
    #Use = 'Use'
    #usage_timeout = 'usage_timeout'
    #Temporarily = 'Temporarily'
    #Use = 'Use'
    #usage_unban = 'usage_unban'
    #Removes = 'Removes'
    #usage_unhost = 'usage_unhost'
    #Stop = 'Stop'
    #usage_unmod = 'usage_unmod'
    #usage_unraid = 'usage_unraid'
    #Cancel = 'Cancel'
    #usage_untimeout = 'usage_untimeout'
    #Removes = 'Removes'
    #usage_unvip = 'usage_unvip'
    #usage_user = 'usage_user'
    #usage_vip = 'usage_vip'
    #usage_vips = 'usage_vips'
    #usage_whisper = 'usage_whisper'
    #vip_success = 'vip_success'
    #vips_success = 'vips_success'
    #whisper_banned = 'whisper_banned'
    #whisper_banned_recipient = 'whisper_banned_recipient'
    #whisper_invalid_login = 'whisper_invalid_login'
    #whisper_invalid_self = 'whisper_invalid_self'
    #whisper_limit_per_min = 'whisper_limit_per_min'
    #whisper_limit_per_sec = 'whisper_limit_per_sec'
    #whisper_restricted = 'whisper_restricted'
    #whisper_restricted_recipient = 'whisper_restricted_recipient'

    ## msg_id do comando "USERNOTICE"
    #sub = 'sub'
    #resub = 'resub'
    #subgift = 'subgift'
    #submysterygift = 'submysterygift'
    #giftpaidupgrade = 'giftpaidupgrade'
    #rewardgift = 'rewardgift'
    #anongiftpaidupgrade = 'anongiftpaidupgrade'
    #raid = 'raid'
    #unraid = 'unraid'
    #ritual = 'ritual'
    #bitsbadgetier = 'bitsbadgetier'

class UserType(Enum):
    NORMAL: str = ''
    ADMIN: str = 'admin'
    GLOBAL_MOD: str = 'global_mod'
    STAFF: str = 'staff'

class TagDoesntExixts(Exception):
    def __init__(self, msg):
        super().__init__(msg)

class Tags:
    def __init__(self, *args):
        self.badge_info: Dict[str:str] = None # Cada chave do dicionário é um badge, seu valor correspondente é o METADATA. Pode vir vazio
        self.badges: Dict[str:int] = None # Cada chave é um badge, e seu valor correspondente é sua versão. Pode vir vazio
        self.bits: int = None
        self.color: str = None # Hexadecimal do RGB correspondente. Pode vir vazio
        self.display_name: str = None # Pode vir vazio
        self.emotes: Dict[str:Tuple[int, int]] = None
        self.id: str = None
        self.mod: bool = None
        self.pinned_chat_paid_amount: int = None
        self.pinned_chat_paid_currency: str = None
        self.pinned_chat_paid_exponent: float = None
        self.pinned_chat_paid_level: str = None # Estudar possibilidade de enum
        self.pinned_chat_paid_is_system_message: bool = None
        self.reply_parent_msg_id: str = None
        self.reply_parent_user_id: str = None
        self.reply_parent_user_login: str = None
        self.reply_parent_display_name: str = None
        self.reply_parent_msg_body: str = None
        self.reply_thread_parent_msg_id: str = None
        self.reply_thread_parent_user_login: str = None
        self.room_id: str = None
        self.subscriber: bool = None
        self.tmi_sent_ts: int = None # Tempo em milisegundos
        self.turbo: bool = None
        self.user_id: str = None
        self.user_type: UserType = None
        self.vip: bool = None
        self.ban_duration: int = None
        self.target_user_id: str = None
        self.login: str = None
        self.target_msg_id: str = None # UUID
        self.emote_sets: List[str] = None # Pode vir com um '0'
        self.msg_id: MsgID = None # Estudar possibilidade de enum. Verificar se o msgID de cada tipo de NOTICE, deve ser diferente, ou pode ser o mesmo
        self.emote_only: bool = None
        self.followers_only: bool = None
        self.r9k: bool = None
        self.slow: int = None
        self.subs_only: bool = None
        self.system_msg: str = None
        self.message_id: str = None
        self.thread_id: str = None

        self.attributes = dir(self)
        for attribute in args:
            if attribute in self.attributes:
                setattr(self, attribute, args[attribute])
            else:
                raise TagDoesntExixts(f"Tag {attribute} doesn't exists!")

        # Não fiz essa parte ainda https://dev.twitch.tv/docs/irc/tags/#usernotice-tags:~:text=Only%20subscription%2D%20and%20raid%2Drelated%20notices%20include%20the%20following%20tags%3A

msg = '@badge-info=;badges=vip/1,partner/1;client-nonce=cd15335a5e2059c3b087e22612de485e;color=;display-name=fun2bfun;emotes=;first-msg=0;flags=;id=1fd20412-965f-4c96-beb3-52266448f564;mod=0;returning-chatter=0;room-id=102336968;subscriber=0;tmi-sent-ts=1661372052425;turbo=0;user-id=12345678;user-type=;vip=1'
parts = msg.split()

if parts[0].startswith("@"):
    tags_str = parts.pop(0).lstrip("@")
    tags = {}
    for tag in tags_str.split(";"):  # Separando as tags
        tag = tag.split("=")  # Separando a chave do valor, para cada tag
        tag[0] = tag[0].replace(
            "-", "_"
        )  # tornando a string válida para criação de variável
        tag[1] = tag[1].split(
            ","
        )  # Tentando segmentar o valor da tag, em lista
        if len(tag[1]) <= 1:  # Caso não seja lista:
            tag[1] = tag[1][0]  # Retorne o valor como string
            tag[1] = tuple(
                tag[1].split("/")
            )  # Separando o valor em (tag, meta-tag)
            if len(tag[1]) <= 1:  # Caso não exista meta-tag
                tag[1] = tag[1][0]  # Retorene o valor como string
        else:  # Caso seja lista
            for i, j in enumerate(tag[1]):  # Itere sobre o valor
                tag[1][i] = tuple(
                    j.split("/")
                )  # Separando o valor em (tag, meta-tag)
                if len(tag[1][i]) <= 1:  # Caso não exista meta-tag
                    tag[1][i] = tag[1][i][0]  # Retorene o valor como string
        tags[tag[0]] = tag[1]

tags = Tags()

#class Message:
#    def __init__(self, received_msg, capabilities):
#        self.IRC_commands = {
#            'JOIN': {
#                'capabilitie': 'twitch.tv/membership',
#                'tags': []
#            },
#            'PART': {
#                'capabilitie': 'twitch.tv/membership',
#                'tags': []
#            },
#            'PRIVMSG': {
#                'capabilitie': '',
#                'tags': [
#                    'badge-info',
#                    'badges',
#                    'bits', # Optional
#                    'color',
#                    'display-name',
#                    'emotes',
#                    'id',
#                    'mod',
#                    'pinned-chat-paid-amount',
#                    'pinned-chat-paid-currency',
#                    'pinned-chat-paid-exponent',
#                    'pinned-chat-paid-level',
#                    'pinned-chat-paid-is-system-message',
#                    'reply-parent-msg-id', # Optional
#                    'reply-parent-user-id', # Optional
#                    'reply-parent-user-login', # Optional
#                    'reply-parent-display-name', # Optional
#                    'reply-parent-msg-body', # Optional
#                    'reply-thread-parent-msg-id', # Optional
#                    'reply-thread-parent-user-login', # Optional
#                    'room-id',
#                    'subscriber',
#                    'tmi-sent-ts',
#                    'turbo',
#                    'user-id',
#                    'user-type',
#                    'vip'
#                ]
#            },
#            'CLEARCHAT': {
#                'capabilitie': 'twitch.tv/commands',
#                'tags': [
#                    'ban-duration', # Optional
#                    'room-id',
#                    'target-user-id', # Optional
#                    'tmi-sent-ts'
#                ]
#            },
#            'CLEARMSG': {
#                'capabilitie': 'twitch.tv/commands',
#                'tags': [
#                    'login',
#                    'room-id', # Optional
#                    'target-msg-id',
#                    'tmi-sent-ts'
#                ]
#            },
#            'GLOBALUSERSTATE': {
#                'capabilitie': 'twitch.tv/commands',
#                'tags': [
#                    'badge-info',
#                    'badges',
#                    'color',
#                    'display-name',
#                    'emote-sets',
#                    'turbo',
#                    'user-id',
#                    'user-type'
#                ]
#            },
#            'HOSTTARGET': {
#                'capabilitie': 'twitch.tv/commands',
#                'tags': []
#            },
#            'NOTICE': {
#                'capabilitie': 'twitch.tv/commands',
#                'tags': [
#                    'msg-id',
#                    'target-user-id' # Optional
#                ]
#            },
#            'RECONNECT': {
#                'capabilitie': 'twitch.tv/commands',
#                'tags': []
#            },
#            'ROOMSTATE': {
#                'capabilitie': 'twitch.tv/commands',
#                'tags': [
#                    'emote-only',
#                    'followers-only',
#                    'r9k',
#                    'room-id',
#                    'slow',
#                    'subs-only'
#                ]
#            },
#            'USERNOTICE': {
#                'capabilitie': 'twitch.tv/commands',
#                'tags': [
#                    'badge-info',
#                    'badges',
#                    'display-name',
#                    'emotes',
#                    'id',
#                    'login',
#                    'mod',
#                    'msg-id',
#                    'room-id',
#                    'subscriber',
#                    'system-msg',
#                    'tmi-sent-ts',
#                    'turbo',
#                    'user-id',
#                    'user-type'
#                ]
#            },
#            'USERSTATE': {
#                'capabilitie': 'twitch.tv/commands',
#                'tags': [
#                    'badge-info',
#                    'badges',
#                    'color',
#                    'display-name',
#                    'emote-sets',
#                    'id',
#                    'mod',
#                    'subscriber',
#                    'turbo',
#                    'user-type'
#                ]
#            },
#            'WHISPER': {
#                'capabilitie': 'twitch.tv/commands',
#                'tags': [
#                    'badges',
#                    'color',
#                    'display-name',
#                    'emotes',
#                    'message-id',
#                    'thread-id',
#                    'turbo',
#                    'user-id',
#                    'user-type'
#                ]
#            }
#        }
#        self.parts: list = received_msg.split(" ")
#        self.prefix = None
#        self.user = None
#        self.channel = None
#        self.text = None
#        self.text_command = None
#        self.text_args = None
#        self.irc_command = None
#        self.irc_args = None
#        self.user_role = "vwr"
#        self.is_sub = False
#        self.tags = {}
#
#
#    def parse_message(self):
#        if parts[0].startswith("@"):
#            tags_str = parts.pop(0).lstrip("@")
#            tags = {}
#            for tag in tags_str.split(";"):  # Separando as tags
#                tag = tag.split("=")  # Separando a chave do valor, para cada tag
#                tag[0] = tag[0].replace(
#                    "-", "_"
#                )  # tornando a string válida para criação de variável
#                tag[1] = tag[1].split(
#                    ","
#                )  # Tentando segmentar o valor da tag, em lista
#                if len(tag[1]) <= 1:  # Caso não seja lista:
#                    tag[1] = tag[1][0]  # Retorne o valor como string
#                    tag[1] = tuple(
#                        tag[1].split("/")
#                    )  # Separando o valor em (tag, meta-tag)
#                    if len(tag[1]) <= 1:  # Caso não exista meta-tag
#                        tag[1] = tag[1][0]  # Retorene o valor como string
#                else:  # Caso seja lista
#                    for i, j in enumerate(tag[1]):  # Itere sobre o valor
#                        tag[1][i] = tuple(
#                            j.split("/")
#                        )  # Separando o valor em (tag, meta-tag)
#                        if len(tag[1][i]) <= 1:  # Caso não exista meta-tag
#                            tag[1][i] = tag[1][i][0]  # Retorene o valor como string
#                tags[tag[0]] = tag[1]
#        if parts[0].startswith(":"):
#            self.prefix = parts[0][1:]
#            self.user = self.get_user_from_prefix(self.prefix)
#            parts = parts[1:]
#        text_start = next(
#            (idx for idx, msg in enumerate(parts) if msg.startswith(":")), None
#        )
#        if text_start:
#            text_parts = parts[text_start:]
#            text_parts[0] = text_parts[0][1:]
#            text = " ".join(text_parts)
#            text_command = text_parts[0].lower()
#            text_args = text_parts[1:]
#            parts = parts[:text_start]
#        irc_command = parts[0]
#        irc_args = parts[1:]
#        hash_start = next(
#            (idx for idx, part in enumerate(irc_args) if part.startswith("#")), None
#        )
#        if hash_start != None:
#            channel = irc_args[hash_start][1:]
#        msg = {
#            "prefix": self.prefix,
#            "user": user,
#            "channel": channel,
#            "text": text,
#            "text_command": text_command,
#            "text_args": text_args,
#            "irc_command": irc_command,
#            "irc_args": irc_args,
#            "user_role": user_role,
#            "is_sub": is_sub,
#            "time": datetime.now(),
#        }
#        if "mod" in tags.keys() and tags["mod"] == "1":
#            tags["user_role"] = "mod"
#        elif "vip" in tags.keys() and tags["vip"] == "1":
#            tags["user_role"] = "vip"
#        elif "badges" in tags.keys() and "broadcaster" in [
#            badge[0] for badge in tags["badges"]
#        ]:
#            tags["user_role"] = "own"
#        if "subscriber" in tags.keys() and tags["subscriber"] == "1":
#            tags["is_sub"] = True
#        msg.update(tags)
#        return msg
