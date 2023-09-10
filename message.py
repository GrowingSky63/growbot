from typing import Optional, Union, Tuple, List, Dict
from enum import Enum


class PinnedChatPaidLevel(Enum):
    ONE = "ONE"
    TWO = "TWO"
    THREE = "THREE"
    FOUR = "FOUR"
    FIVE = "FIVE"
    SIX = "SIX"
    SEVEN = "SEVEN"
    EIGHT = "EIGHT"
    NINE = "NINE"
    TEN = "TEN"


class MsgID(Enum):
    pass

    ## msg_id do comando "NOTICE"
    # already_banned = 'already_banned'
    # already_emote_only_off = 'already_emote_only_off'
    # already_emote_only_on = 'already_emote_only_on'
    # already_followers_off = 'already_followers_off'
    # already_followers_on = 'already_followers_on'
    # already_r9k_off = 'already_r9k_off'
    # already_r9k_on = 'already_r9k_on'
    # already_slow_off = 'already_slow_off'
    # already_slow_on = 'already_slow_on'
    # already_subs_off = 'already_subs_off'
    # already_subs_on = 'already_subs_on'
    # autohost_receive = 'autohost_receive'
    # bad_ban_admin = 'bad_ban_admin'
    # bad_ban_anon = 'bad_ban_anon'
    # bad_ban_broadcaster = 'bad_ban_broadcaster'
    # bad_ban_mod = 'bad_ban_mod'
    # bad_ban_self = 'bad_ban_self'
    # bad_ban_staff = 'bad_ban_staff'
    # bad_commercial_error = 'bad_commercial_error'
    # bad_delete_message_broadcaster = 'bad_delete_message_broadcaster'
    # bad_delete_message_mod = 'bad_delete_message_mod'
    # bad_host_error = 'bad_host_error'
    # bad_host_hosting = 'bad_host_hosting'
    # bad_host_rate_exceeded = 'bad_host_rate_exceeded'
    # bad_host_rejected = 'bad_host_rejected'
    # bad_host_self = 'bad_host_self'
    # bad_mod_banned = 'bad_mod_banned'
    # bad_mod_mod = 'bad_mod_mod'
    # bad_slow_duration = 'bad_slow_duration'
    # bad_timeout_admin = 'bad_timeout_admin'
    # bad_timeout_anon = 'bad_timeout_anon'
    # bad_timeout_broadcaster = 'bad_timeout_broadcaster'
    # bad_timeout_duration = 'bad_timeout_duration'
    # bad_timeout_mod = 'bad_timeout_mod'
    # bad_timeout_self = 'bad_timeout_self'
    # bad_timeout_staff = 'bad_timeout_staff'
    # bad_unban_no_ban = 'bad_unban_no_ban'
    # bad_unhost_error = 'bad_unhost_error'
    # bad_unmod_mod = 'bad_unmod_mod'
    # bad_vip_grantee_banned = 'bad_vip_grantee_banned'
    # bad_vip_grantee_already_vip = 'bad_vip_grantee_already_vip'
    # bad_vip_max_vips_reached = 'bad_vip_max_vips_reached'
    # bad_vip_achievement_incomplete = 'bad_vip_achievement_incomplete'
    # bad_unvip_grantee_not_vip = 'bad_unvip_grantee_not_vip'
    # ban_success = 'ban_success'
    # cmds_available = 'cmds_available'
    # color_changed = 'color_changed'
    # commercial_success = 'commercial_success'
    # delete_message_success = 'delete_message_success'
    # delete_staff_message_success = 'delete_staff_message_success'
    # emote_only_off = 'emote_only_off'
    # emote_only_on = 'emote_only_on'
    # followers_off = 'followers_off'
    # followers_on = 'followers_on'
    # followers_on_zero = 'followers_on_zero'
    # host_off = 'host_off'
    # host_on = 'host_on'
    # host_receive = 'host_receive'
    # host_receive_no_count = 'host_receive_no_count'
    # host_target_went_offline = 'host_target_went_offline'
    # hosts_remaining = 'hosts_remaining'
    # invalid_user = 'invalid_user'
    # mod_success = 'mod_success'
    # msg_banned = 'msg_banned'
    # msg_bad_characters = 'msg_bad_characters'
    # msg_channel_blocked = 'msg_channel_blocked'
    # msg_channel_suspended = 'msg_channel_suspended'
    # msg_duplicate = 'msg_duplicate'
    # msg_emoteonly = 'msg_emoteonly'
    # msg_followersonly = 'msg_followersonly'
    # msg_followersonly_followed = 'msg_followersonly_followed'
    # msg_followersonly_zero = 'msg_followersonly_zero'
    # msg_r9k = 'msg_r9k'
    # msg_ratelimit = 'msg_ratelimit'
    # msg_rejected = 'msg_rejected'
    # msg_rejected_mandatory = 'msg_rejected_mandatory'
    # msg_requires_verified_phone_number = 'msg_requires_verified_phone_number'
    # msg_slowmode = 'msg_slowmode'
    # msg_subsonly = 'msg_subsonly'
    # msg_suspended = 'msg_suspended'
    # msg_timedout = 'msg_timedout'
    # msg_verified_email = 'msg_verified_email'
    # no_help = 'no_help'
    # no_mods = 'no_mods'
    # no_vips = 'no_vips'
    # not_hosting = 'not_hosting'
    # no_permission = 'no_permission'
    # r9k_off = 'r9k_off'
    # r9k_on = 'r9k_on'
    # raid_error_already_raiding = 'raid_error_already_raiding'
    # raid_error_forbidden = 'raid_error_forbidden'
    # raid_error_self = 'raid_error_self'
    # raid_error_too_many_viewers = 'raid_error_too_many_viewers'
    # raid_error_unexpected = 'raid_error_unexpected'
    # raid_notice_mature = 'raid_notice_mature'
    # raid_notice_restricted_chat = 'raid_notice_restricted_chat'
    # room_mods = 'room_mods'
    # slow_off = 'slow_off'
    # slow_on = 'slow_on'
    # subs_off = 'subs_off'
    # subs_on = 'subs_on'
    # timeout_no_timeout = 'timeout_no_timeout'
    # timeout_success = 'timeout_success'
    # tos_ban = 'tos_ban'
    # turbo_only_color = 'turbo_only_color'
    # unavailable_command = 'unavailable_command'
    # unban_success = 'unban_success'
    # unmod_success = 'unmod_success'
    # unraid_error_no_active_raid = 'unraid_error_no_active_raid'
    # unraid_error_unexpected = 'unraid_error_unexpected'
    # unraid_success = 'unraid_success'
    # unrecognized_cmd = 'unrecognized_cmd'
    # untimeout_banned = 'untimeout_banned'
    # untimeout_success = 'untimeout_success'
    # unvip_success = 'unvip_success'
    # usage_ban = 'usage_ban'
    # usage_clear = 'usage_clear'
    # Clear = 'Clear'
    # usage_color = 'usage_color'
    # Change = 'Change'
    # usage_commercial = 'usage_commercial'
    # Triggers = 'Triggers'
    # usage_disconnect = 'usage_disconnect'
    # Reconnects = 'Reconnects'
    # usage_delete = 'usage_delete'
    # usage_emote_only_off = 'usage_emote_only_off'
    # Disables = 'Disables'
    # usage_emote_only_on = 'usage_emote_only_on'
    # Enables = 'Enables'
    # usage_followers_off = 'usage_followers_off'
    # Disables = 'Disables'
    # usage_followers_on = 'usage_followers_on'
    # Enables = 'Enables'
    # usage_help = 'usage_help'
    # Lists = 'Lists'
    # usage_host = 'usage_host'
    # Host = 'Host'
    # usage_marker = 'usage_marker'
    # Adds = 'Adds'
    # usage_me = 'usage_me'
    # usage_mod = 'usage_mod'
    # usage_mods = 'usage_mods'
    # Lists = 'Lists'
    # usage_r9k_off = 'usage_r9k_off'
    # usage_r9k_on = 'usage_r9k_on'
    # usage_raid = 'usage_raid'
    # Raid = 'Raid'
    # Use = 'Use'
    # usage_slow_off = 'usage_slow_off'
    # Disables = 'Disables'
    # usage_slow_on = 'usage_slow_on'
    # Enables = 'Enables'
    # Use = 'Use'
    # usage_subs_off = 'usage_subs_off'
    # Disables = 'Disables'
    # usage_subs_on = 'usage_subs_on'
    # Enables = 'Enables'
    # Use = 'Use'
    # usage_timeout = 'usage_timeout'
    # Temporarily = 'Temporarily'
    # Use = 'Use'
    # usage_unban = 'usage_unban'
    # Removes = 'Removes'
    # usage_unhost = 'usage_unhost'
    # Stop = 'Stop'
    # usage_unmod = 'usage_unmod'
    # usage_unraid = 'usage_unraid'
    # Cancel = 'Cancel'
    # usage_untimeout = 'usage_untimeout'
    # Removes = 'Removes'
    # usage_unvip = 'usage_unvip'
    # usage_user = 'usage_user'
    # usage_vip = 'usage_vip'
    # usage_vips = 'usage_vips'
    # usage_whisper = 'usage_whisper'
    # vip_success = 'vip_success'
    # vips_success = 'vips_success'
    # whisper_banned = 'whisper_banned'
    # whisper_banned_recipient = 'whisper_banned_recipient'
    # whisper_invalid_login = 'whisper_invalid_login'
    # whisper_invalid_self = 'whisper_invalid_self'
    # whisper_limit_per_min = 'whisper_limit_per_min'
    # whisper_limit_per_sec = 'whisper_limit_per_sec'
    # whisper_restricted = 'whisper_restricted'
    # whisper_restricted_recipient = 'whisper_restricted_recipient'

    ## msg_id do comando "USERNOTICE"
    # sub = 'sub'
    # resub = 'resub'
    # subgift = 'subgift'
    # submysterygift = 'submysterygift'
    # giftpaidupgrade = 'giftpaidupgrade'
    # rewardgift = 'rewardgift'
    # anongiftpaidupgrade = 'anongiftpaidupgrade'
    # raid = 'raid'
    # unraid = 'unraid'
    # ritual = 'ritual'
    # bitsbadgetier = 'bitsbadgetier'


class UserType(Enum):
    NORMAL: str = ""
    ADMIN: str = "admin"
    GLOBAL_MOD: str = "global_mod"
    STAFF: str = "staff"


class TagDoesntExixts(Exception):
    def __init__(self, msg):
        super().__init__(msg)


class Tags:
    def __init__(self, received_msg):
        self.badge_info: Dict[
            str:str
        ] = None  # Cada chave do dicionário é um badge, seu valor correspondente é o METADATA. Pode vir vazio
        self.badges: Dict[
            str:int
        ] = None  # Cada chave é um badge, e seu valor correspondente é sua versão. Pode vir vazio
        self.bits: int = None
        self.color: str = None  # Hexadecimal do RGB correspondente. Pode vir vazio
        self.display_name: str = None  # Pode vir vazio
        self.emotes: Dict[str : Tuple[int, int]] = None
        self.id: str = None
        self.mod: bool = None
        self.pinned_chat_paid_amount: int = None
        self.pinned_chat_paid_currency: str = None
        self.pinned_chat_paid_exponent: float = None
        self.pinned_chat_paid_level: str = None  # Estudar possibilidade de enum
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
        self.tmi_sent_ts: int = None  # Tempo em milisegundos
        self.turbo: bool = None
        self.user_id: str = None
        self.user_type: UserType = None
        self.vip: bool = None
        self.ban_duration: int = None
        self.target_user_id: str = None
        self.login: str = None
        self.target_msg_id: str = None  # UUID
        self.emote_sets: List[str] = None  # Pode vir com um '0'
        self.msg_id: MsgID = None  # Estudar possibilidade de enum. Verificar se o msgID de cada tipo de NOTICE, deve ser diferente, ou pode ser o mesmo
        self.emote_only: bool = None
        self.followers_only: bool = None
        self.r9k: bool = None
        self.slow: int = None
        self.subs_only: bool = None
        self.system_msg: str = None
        self.message_id: str = None
        self.thread_id: str = None
        tags_dict: dict = self.parse_tags(received_msg)
        [setattr(self, key, value) for key, value in tags_dict.items()]

    def parse_tags(self, received_msg) -> dict:
        parts = received_msg.split()
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

        return tags


received_msg = "@badge-info=;badges=broadcaster/1;client-nonce=459e3142897c7a22b7d275178f2259e0;color=#0000FF;display-name=lovingt3s;emote-only=1;emotes=62835:0-10;first-msg=0;flags=;id=885196de-cb67-427a-baa8-82f9b0fcd05f;mod=0;room-id=713936733;subscriber=0;tmi-sent-ts=1643904084794;turbo=0;user-id=713936733;user-type= :lovingt3s!lovingt3s@lovingt3s.tmi.twitch.tv PRIVMSG #lovingt3s :bleedPurple"
tags = Tags(received_msg)
print()
