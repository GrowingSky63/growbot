from datetime import datetime, timedelta
from collections import namedtuple
from random import randint
from typing import List
import requests
import asyncio
import sqlite3
import socket
import pytz
import json
import ssl
import re


# https://www.twitch.tv/popout/xgrowingsky/chat?popout=
DB_PATH = "./data.db"
MY_CREDENTIALS_DB_PATH = "./my_credentials.db"


Command = namedtuple(
    "Command", "aliases function role universal_delay individual_delay desc usage"
)


class Object:
    def __init__(self, dictionary: dict = {}):
        for key, value in dictionary.items():
            setattr(self, key, value)

    def add_attribute(self, key, value):
        setattr(self, key, value)


class Database:
    def __init__(self, db_path):
        self.db_path = db_path

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.commit()
        self.conn.close()


class GrowBot:
    # Definições e autenticação
    def __init__(
        self,
        client_bot,
        channels,
        irc_server="irc.chat.twitch.tv",
        irc_port=6697,
        redirect_uri="https://localhost:3000",
    ):
        # Recuperando as informações de autenticação do bot, no banco de dados
        with Database(MY_CREDENTIALS_DB_PATH) as cursor:
            cursor.execute(f"SELECT * FROM client_bots WHERE username = '{client_bot}'")
            (
                self.client_username,
                self.client_id,
                self.client_secret,
            ) = cursor.fetchall()[0]

        # Instanciando variaveis para conexão do irc e montagem do link para obtenção do código de autenticação
        self.chat_url = "irc.chat.twitch.tv"
        self.chat_port = 6667
        self.irc_server = irc_server
        self.irc_port = irc_port
        self.channels = channels
        self.redirect_uri = redirect_uri
        self.capabilities = [
            'twitch.tv/commands',
            'twitch.tv/tags',
            'twitch.tv/membership'
        ]
        self.scopes = "+".join(
            [
                "chat:read",
                "chat:edit",
                "channel:manage:raids",
                "channel:read:redemptions",
                "channel:manage:redemptions",
                "channel:read:stream_key",
                "channel:read:subscriptions",
                "channel:read:vips",
                "channel:manage:vips",
                "clips:edit",
                "moderation:read",
                "moderator:manage:announcements",
                "moderator:manage:banned_users",
                "moderator:manage:chat_messages",
                "moderator:read:chatters",
                "moderator:read:followers",
                "user:manage:chat_color",
                "user:manage:whispers",
            ]
        )
        self.auth_code_url = f"\033[32mhttps://id.twitch.tv/oauth2/authorize?response_type=code&client_id={self.client_id}&redirect_uri={self.redirect_uri}&scope={self.scopes}\033[m\n\033[34mCole o código aqui: \033[m"

        # Checando validade do token
        with Database(MY_CREDENTIALS_DB_PATH) as cursor:
            cursor.execute(
                f"SELECT tokens.access_token, tokens.refresh_token, tokens.expires_in FROM tokens WHERE tokens.client_id = '{self.client_id}'"
            )
            data = cursor.fetchall()
        if data:
            self.access_token, self.refresh_token, self.expires_in = data[0]
            self.expires_in = datetime.strptime(self.expires_in, "%Y-%m-%d %H:%M:%S")
        else:
            self.access_token, self.refresh_token, self.expires_in = self.get_auth_code(
                "authorization_code"
            )
        teste = (self.expires_in - datetime.now())
        if teste < timedelta(0):
            self.access_token, self.refresh_token, self.expires_in = self.get_auth_code(
                "refresh_token", self.refresh_token
            )

        # Instanciando comandos predefinidos para todos os canais
        self.cmd_prefix = "!"
        self.roles = ["vwr", "vip", "mod", "own"]
        self.predef_commands = {
            "help": Command(
                aliases=["h", "ajuda"],
                function=self.cmd_help,
                role="vwr",
                universal_delay=0,
                individual_delay=10,
                desc="Envia esta mensagem",
                usage=f"{self.cmd_prefix}help [comando]",
            ),
            "cmd": Command(
                aliases=[],
                function=self.cmd_cmd,
                role="vwr",
                universal_delay=0,
                individual_delay=3,
                desc="Permite criar, editar ou remover um comando de resposta personalizada.",
                usage=f"{self.cmd_prefix}cmd <add/remove/edit> <nome do comando> <resposta(add/edit)> [aliase1;aliase2;...] [delay universal] [delay por usuário]",
            ),
        }

        # instanciando variáveis universais que podem ser usadas na criação de template_commands
        self.vars = {
            "count": self.var_count,
            "user": self.var_user,
            "channel": self.var_channel,
            "now.date": self.var_now_date,
            "now.clock": self.var_now_clock,
            "now.day": self.var_now_day,
            "now.month": self.var_now_month,
            "now.year": self.var_now_year,
            "now.hour": self.var_now_hour,
            "now.minute": self.var_now_minute,
            "now.second": self.var_now_second,
            "rand.chatter": self.var_rand_chatter,
            "rand.number": self.var_rand_number,
            "arg": self.var_arg,
        }

    def var_count(self, msg):
        return msg.count

    def var_user(self, msg):
        return msg.user

    def var_channel(self, msg):
        return msg.channel

    def var_now_date(self, msg, *args):
        tz_info = args[0]
        if tz_info:
            return msg.time.replace(tzinfo=pytz.timezone(tz_info)).strftime("%d/%m/%Y")
        else:
            return msg.time.strftime("%d/%m/%Y")

    def var_now_clock(self, msg, tz_info=None):
        if tz_info:
            return msg.time.replace(tzinfo=pytz.timezone(tz_info)).strftime("%H:%M:%S")
        else:
            return msg.time.strftime("%H:%M:%S")

    def var_now_day(self, msg, tz_info=None):
        if tz_info:
            return msg.time.replace(tzinfo=pytz.timezone(tz_info)).strftime("%d")
        else:
            return msg.time.strftime("%d")

    def var_now_month(self, msg, tz_info=None):
        if tz_info:
            return msg.time.replace(tzinfo=pytz.timezone(tz_info)).strftime("%m")
        else:
            return msg.time.strftime("%m")

    def var_now_year(self, msg, tz_info=None):
        if tz_info:
            return msg.time.replace(tzinfo=pytz.timezone(tz_info)).strftime("%Y")
        else:
            return msg.time.strftime("%Y")

    def var_now_hour(self, msg, tz_info=None):
        if tz_info:
            return msg.time.replace(tzinfo=pytz.timezone(tz_info)).strftime("%H")
        else:
            return msg.time.strftime("%H")

    def var_now_minute(self, msg, tz_info=None):
        if tz_info:
            return msg.time.replace(tzinfo=pytz.timezone(tz_info)).strftime("%M")
        else:
            return msg.time.strftime("%M")

    def var_now_second(self, msg, tz_info=None):
        if tz_info:
            return msg.time.replace(tzinfo=pytz.timezone(tz_info)).strftime("%S")
        else:
            return msg.time.strftime("%S")

    def var_rand_chatter(self, msg):
        chatters = self.get_chatters(msg.channel)
        if chatters:
            with Database(DB_PATH) as cursor:
                cursor.execute("SELECT * FROM bot_chatters")
                data = [row[0] for row in cursor.fetchall()]
            users_login = [
                chatter for chatter in chatters.keys() if chatter not in data
            ]
            return chatters[users_login[randint(0, len(users_login) - 1)]]
        else:
            return "Erro interno"

    def var_rand_number(self, msg, *args):
        i, f = (1, 100)
        if len(args) >= 2:
            i, f = (int(args[0]), int(args[1]))
        return str(randint(i, f))

    def var_arg(self, msg, *args):
        if len(args) == 0:
            arg_index = 0
        elif len(args) == 1:
            arg_index = int(args[0])
        elif len(args) > 1:
            arg_index = int(args[0])
        if len(msg.text_args) > arg_index:
            for arg in args[1:]:
                if arg.startswith("-r-d"):
                    arg = arg.replace("-r-d", "")
                    return re.sub(arg, "", msg.text_args[arg_index - 1])
        else:
            return ""
        return msg.text_args[arg_index]

    # Funções auxiliares // Buscas em APIs // Buscas no banco de dados
    def find_variable(self, text):
        return re.findall(r"\${([^{}]*(?:{[^{}]*}[^{}]*)*)}", text)

    def get_users_info(self, *users) -> List[Object]:
        users_url_parameters = "&".join([f"login={user}" for user in users])
        users_dict = json.loads(
            requests.get(
                url=f"https://api.twitch.tv/helix/users?{users_url_parameters}",
                headers={
                    "Authorization": f"Bearer {self.access_token}",
                    "Client-Id": self.client_id,
                },
            ).content
        )
        if "data" in users_dict.keys():
            users_dict = users_dict["data"]
        else:
            print(users_dict)
        if len(users) == 1:
            return Object(users_dict[0])
        else:
            return [Object(user) for user in users_dict]

    def get_auth_code(self, grant_type, code=None):
        if code is None:
            code = input(self.auth_code_url)
        if grant_type == "refresh_token":
            url_form = f"client_id={self.client_id}&client_secret={self.client_secret}&refresh_token={code}&grant_type={grant_type}&redirect_uri={self.redirect_uri}"
        elif grant_type == "authorization_code":
            url_form = f"client_id={self.client_id}&client_secret={self.client_secret}&code={code}&grant_type={grant_type}&redirect_uri={self.redirect_uri}"
        elif grant_type == "client_credentials":
            url_form = f"client_id={self.client_id}&client_secret={self.client_secret}"

        response = requests.post(
            url="https://id.twitch.tv/oauth2/token",
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data=url_form,
        )
        response = json.loads(response.content)

        with Database(MY_CREDENTIALS_DB_PATH) as cursor:
            cursor.execute(
                f'SELECT * FROM tokens WHERE username = "{self.client_username}";'
            )
            expires_in = (timedelta(seconds=response["expires_in"]) + datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
            if cursor.fetchall():
                cursor.execute(
                    f"UPDATE tokens SET access_token = ?, expires_in = ?, refresh_token = ?, scope = ? WHERE username = ?",
                    (
                        response["access_token"],
                        expires_in,
                        response["refresh_token"],
                        "+".join(response["scope"]),
                        self.client_username,
                    ),
                )
            else:
                cursor.execute(
                    f"INSERT INTO tokens (client_id, access_token, expires_in, refresh_token, scope, username) VALUES (?, ?, ?, ?, ?, ?)",
                    (
                        self.client_id,
                        response["access_token"],
                        expires_in,
                        response["refresh_token"],
                        "+".join(response["scope"]),
                        self.client_username,
                    ),
                )
        return (
            response["access_token"],
            response["refresh_token"],
            timedelta(seconds=response["expires_in"]) + datetime.now(),
        )

    def send_command(self, command):
        self.chat.send(f"{command}\r\n".encode())
        print(f"< {command}")

    def send_privmsg(self, msg: Object, response, reply_msg=False):
        if reply_msg:
            command = (
                f"@reply-parent-msg-id={msg.id} PRIVMSG #{msg.channel} :{response}"
            )
        else:
            command = f"PRIVMSG #{msg.channel} :{response}"
        self.send_command(command)

    def send_whisper(self, target, response):
        sender_id, target_id = (
            user.id for user in self.get_users_info(self.client_username, target)
        )
        requests.post(
            url=f"https://api.twitch.tv/helix/whispers?from_user_id={sender_id}&to_user_id={target_id}",
            headers={
                "Authorization": f"Bearer {self.access_token}",
                "Client-Id": self.client_id,
                "Content-Type": "application/json",
            },
            json={"message": f"{response}"},
        )
        print(f"< WHISPER {target} :{response}")

    def login(self, nickname, password):
        self.chat = ssl.wrap_socket(socket.socket())
        self.chat.connect((self.irc_server, self.irc_port))
        self.send_command(f"PASS oauth:{password}")
        self.send_command(f"NICK {nickname}")
        self.send_command(
            "CAP REQ :"+' '.join(self.capabilities)
        )

    def connect(self):
        loop = asyncio.get_event_loop()
        self.login(self.client_username, self.access_token)
        for channel in self.channels:
            self.send_command(f"JOIN #{channel}")
        loop.run_until_complete(self.messages_listener())

    def get_chatters(self, channel) -> Object:
        ids = self.get_users_info(channel, self.client_username)
        data = json.loads(
            requests.get(
                url=f"https://api.twitch.tv/helix/chat/chatters?broadcaster_id={ids[0].id}&moderator_id={ids[1].id}",
                headers={
                    "Authorization": f"Bearer {self.access_token}",
                    "Client-Id": self.client_id,
                },
            ).content
        )
        if "data" in data.keys():
            return {user["user_login"]: user["user_name"] for user in data["data"]}
        else:
            print(data)
            return False

    # Tratamento de mensagens e eventos
    def get_user_from_prefix(self, prefix):
        domain = prefix.split("!")[0]
        if domain.endswith(".tmi.twitch.tv"):
            return domain.replace(".tmi.twitch.tv", "")
        if "tmi.twitch.tv" not in domain:
            return domain
        return None

    def parse_message(self, received_msg) -> Object:
        parts: list = received_msg.split(" ")

        prefix = None
        user = None
        channel = None
        text = None
        text_command = None
        text_args = None
        irc_command = None
        irc_args = None
        user_role = "vwr"
        is_sub = False
        tags = {}

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

        if parts[0].startswith(":"):
            prefix = parts[0][1:]
            user = self.get_user_from_prefix(prefix)
            parts = parts[1:]

        text_start = next(
            (idx for idx, msg in enumerate(parts) if msg.startswith(":")), None
        )
        if text_start:
            text_parts = parts[text_start:]
            text_parts[0] = text_parts[0][1:]
            text = " ".join(text_parts)
            text_command = text_parts[0].lower()
            text_args = text_parts[1:]
            parts = parts[:text_start]

        irc_command = parts[0]
        irc_args = parts[1:]

        hash_start = next(
            (idx for idx, part in enumerate(irc_args) if part.startswith("#")), None
        )
        if hash_start != None:
            channel = irc_args[hash_start][1:]

        msg = {
            "prefix": prefix,
            "user": user,
            "channel": channel,
            "text": text,
            "text_command": text_command,
            "text_args": text_args,
            "irc_command": irc_command,
            "irc_args": irc_args,
            "user_role": user_role,
            "is_sub": is_sub,
            "time": datetime.now(),
        }

        if "mod" in tags.keys() and tags["mod"] == "1":
            tags["user_role"] = "mod"
        elif "vip" in tags.keys() and tags["vip"] == "1":
            tags["user_role"] = "vip"
        elif "badges" in tags.keys() and "broadcaster" in [
            badge[0] for badge in tags["badges"]
        ]:
            tags["user_role"] = "own"
        if "subscriber" in tags.keys() and tags["subscriber"] == "1":
            tags["is_sub"] = True

        msg.update(tags)

        return Object(msg)

    def check_command_availability(
        self, msg: Object, cmd, just_template_commands=False
    ):
        if just_template_commands:
            command_list = msg.template_command_list
        else:
            command_list = msg.command_list
        for aliase in command_list:
            if cmd == aliase:
                return False
        return True

    def get_template_commands(self, msg: Object) -> dict:
        with Database(DB_PATH) as cursor:
            cursor.execute(
                f"SELECT cmd_name, cmd_msg, count FROM template_commands WHERE channel='{msg.channel}'"
            )
            data = cursor.fetchall()
        template_commands = {
            row[0]: Command(
                aliases=[],
                function=(self.cmd_any_template, (row[1], int(row[2]))),
                role="vwr",
                universal_delay=10,
                individual_delay=0,
                desc=f'Envia "{row[1]}", no chat',
                usage=f"{self.cmd_prefix}{row[0]}",
            )
            for row in data
        }
        return template_commands

    def handle_msg(self, msg: Object):
        if msg:
            message = self.parse_message(msg)
            print(f"> [{message.irc_command}] {message.user}: {message.text}")
            if message.irc_command == "PING":
                self.send_command("PONG :tmi.twitch.tv")
            elif message.irc_command == "PRIVMSG" and message.text_command.startswith(
                self.cmd_prefix
            ):
                self.handle_command(message)

    def handle_command(self, msg: Object):
        msg.add_attribute("text_command_wop", msg.text_command.lstrip(self.cmd_prefix))

        command_dict = self.get_template_commands(msg)
        command_list = {
            alias: cmd for cmd, value in command_dict.items() for alias in value.aliases
        }
        command_list.update({cmd: cmd for cmd in command_dict.keys()})
        msg.add_attribute("template_command_list", command_list)

        command_dict.update(self.predef_commands)
        command_list = {
            alias: cmd for cmd, value in command_dict.items() for alias in value.aliases
        }
        command_list.update({cmd: cmd for cmd in command_dict.keys()})
        msg.add_attribute("command_list", command_list)

        if not self.check_command_availability(msg, msg.text_command_wop):
            command = command_dict[msg.command_list[msg.text_command_wop]]
            with Database(DB_PATH) as cursor:
                cursor.execute(
                    f"SELECT * FROM command_history WHERE channel='{msg.channel}' AND cmd_name='{msg.text_command_wop}' ORDER BY time DESC LIMIT 1"
                )
                universal_data = cursor.fetchone()
            with Database(DB_PATH) as cursor:
                cursor.execute(
                    f"SELECT * FROM command_history WHERE channel='{msg.channel}' AND cmd_name='{msg.text_command_wop}' AND user='{msg.user}' ORDER BY time DESC LIMIT 1"
                )
                individual_data = cursor.fetchone()

            if universal_data and not individual_data:
                universal_time = datetime.strptime(
                    universal_data[4], "%Y-%m-%d %H:%M:%S"
                )
                universal_delta = (msg.time - universal_time).total_seconds()
                if (
                    msg.user_role in ["own", "mod"]
                    or (not (universal_data or individual_data))
                    or ((universal_delta > command.universal_delay))
                ):
                    if self.roles.index(msg.user_role) >= self.roles.index(
                        command.role
                    ):
                        if type(command.function) is type(tuple()):
                            command.function[0](msg, *command.function[1])
                        else:
                            command.function(msg)
                        with Database(DB_PATH) as cursor:
                            cursor.execute(
                                'INSERT INTO "command_history" ("cmd_name", "channel", "user", "time") VALUES (?, ?, ?, ?)',
                                (
                                    msg.text_command_wop,
                                    msg.channel,
                                    msg.user,
                                    msg.time.strftime("%Y-%m-%d %H:%M:%S"),
                                ),
                            )

            elif individual_data and universal_data:
                individual_time = datetime.strptime(
                    individual_data[4], "%Y-%m-%d %H:%M:%S"
                )
                individual_delta = (msg.time - individual_time).total_seconds()

                universal_time = datetime.strptime(
                    universal_data[4], "%Y-%m-%d %H:%M:%S"
                )
                universal_delta = (msg.time - universal_time).total_seconds()

                if (
                    msg.user_role in ["own", "mod"]
                    or (not (universal_data or individual_data))
                    or (
                        (universal_delta > command.universal_delay)
                        and (individual_delta > command.individual_delay)
                    )
                ):
                    if self.roles.index(msg.user_role) >= self.roles.index(
                        command.role
                    ):
                        if type(command.function) is type(tuple()):
                            command.function[0](msg, *command.function[1])
                        else:
                            command.function(msg)
                        with Database(DB_PATH) as cursor:
                            cursor.execute(
                                'INSERT INTO "command_history" ("cmd_name", "channel", "user", "time") VALUES (?, ?, ?, ?)',
                                (
                                    msg.text_command_wop,
                                    msg.channel,
                                    msg.user,
                                    msg.time.strftime("%Y-%m-%d %H:%M:%S"),
                                ),
                            )
            elif not individual_data and not universal_data:
                if (
                    msg.user_role in ["own", "mod"]
                    or (not (universal_data or individual_data))
                    or (
                        (universal_delta > command.universal_delay)
                        and (individual_delta > command.individual_delay)
                    )
                ):
                    if self.roles.index(msg.user_role) >= self.roles.index(
                        command.role
                    ):
                        if type(command.function) is type(tuple()):
                            command.function[0](msg, *command.function[1])
                        else:
                            command.function(msg)
                        with Database(DB_PATH) as cursor:
                            cursor.execute(
                                'INSERT INTO "command_history" ("cmd_name", "channel", "user", "time") VALUES (?, ?, ?, ?)',
                                (
                                    msg.text_command_wop,
                                    msg.channel,
                                    msg.user,
                                    msg.time.strftime("%Y-%m-%d %H:%M:%S"),
                                ),
                            )


    def handle_variables(self, msg, text):
        final_text = text
        for var in self.find_variable(text):
            if len(self.find_variable(var)) == 0:
                var = var.split(";")
                if var[0] in self.vars:
                    if len(var) > 1:
                        var_content = self.vars[var[0]](msg, *var[1:])
                    else:
                        var_content = self.vars[var[0]](msg)
                    var = "${" + ";".join(var) + "}"
                    final_text = final_text.replace(var, var_content)
            else:
                new_var = self.handle_variables(msg, var)
                final_text = final_text.replace(var, new_var)
                new_var = new_var.split(";")
                if new_var[0] in self.vars:
                    if len(new_var) > 1:
                        var_content = self.vars[new_var[0]](msg, *new_var[1:])
                    else:
                        var_content = self.vars[new_var[0]](msg)
                if new_var[0] in self.vars:
                    new_var = "${" + ";".join(new_var) + "}"
                    final_text = final_text.replace(new_var, var_content)

        return final_text

    # Funções dos comandos
    def cmd_help(self, msg: Object):
        len_args = len(msg.text_args)
        commands_dict = self.get_template_commands(msg)
        commands_dict.update(self.predef_commands)
        response = ""
        if len_args == 0 or self.check_command_availability(
            msg, msg.text_args[0].lstrip(self.cmd_prefix)
        ):
            commands_str = ", ".join(
                [
                    f"{self.cmd_prefix}{cmd_name}: {cmd.desc}"
                    for cmd_name, cmd in commands_dict.items()
                ]
            )
            response = f"Esta é a lista de comandos do canal @{self.get_users_info(msg.channel).display_name}, dos quais você tem permissão: {commands_str}"
        elif len_args >= 1:
            for arg in msg.text_args:
                response += f"{arg}: {commands_dict[arg].desc} || Como usar: {commands_dict[arg].usage}"
                if commands_dict[arg].aliases:
                    response += (
                        f" || Outros nomes:{', '.join(commands_dict[arg].aliases)}"
                    )
        self.send_whisper(msg.user, response)

    def cmd_cmd(self, msg: Object):
        len_args = len(msg.text_args)
        text_arg_cmd_wop = msg.text_args[1].lstrip(self.cmd_prefix)
        query = None
        response = None
        if len_args == 0:
            self.send_whisper(
                msg.user,
                f"Uso correto do comando: {msg.text_command_wop} {self.predef_commands[msg.text_command_wop].usage}",
            )
        elif len_args == 1:
            self.send_whisper(
                msg.user,
                f"Uso correto do comando: {msg.text_command_wop} {self.predef_commands[msg.text_command_wop].usage}",
            )
        elif len_args >= 2:
            if msg.text_args[0] == "add":
                if len_args >= 3:
                    if self.check_command_availability(msg, text_arg_cmd_wop):
                        query = "INSERT INTO template_commands (channel, cmd_name, cmd_msg, count) VALUES (?, ?, ?, ?)"
                        values_tuple = (
                            msg.channel,
                            text_arg_cmd_wop,
                            " ".join(msg.text_args[2:]),
                            0,
                        )
                        response = f"Comando {msg.text_args[1].lstrip(self.cmd_prefix)}, criado com sucesso."
                    else:
                        response = f"Comando {msg.text_args[1].lstrip(self.cmd_prefix)}, já existe."
                else:
                    self.send_whisper(
                        msg.user,
                        f"Uso correto do comando: {msg.text_command_wop} {self.predef_commands[msg.text_command_wop].usage}",
                    )

            elif msg.text_args[0] == "remove":
                if not self.check_command_availability(msg, text_arg_cmd_wop, True):
                    query = "DELETE FROM template_commands WHERE channel = ? AND cmd_name = ?"
                    values_tuple = (msg.channel, msg.text_args[1])
                    response = f"Comando {msg.text_args[1].lstrip(self.cmd_prefix)}, removido com sucesso."
                else:
                    response = f"Comando {msg.text_args[1].lstrip(self.cmd_prefix)}, não existe, ou não pode ser removido."

            elif msg.text_args[0] == "edit":
                if not self.check_command_availability(msg, text_arg_cmd_wop, True):
                    query = "UPDATE template_commands SET cmd_msg = ? WHERE channel = ? AND cmd_name = ?"
                    values_tuple = (
                        " ".join(msg.text_args[2:]),
                        msg.channel,
                        msg.text_args[1],
                    )
                    response = f"Comando {msg.text_args[1].lstrip(self.cmd_prefix)}, editado com sucesso."
                else:
                    response = f"Comando {msg.text_args[1].lstrip(self.cmd_prefix)}, não existe, ou não pode ser removido."

            if query:
                with Database(DB_PATH) as cursor:
                    cursor.execute(query, values_tuple)
                self.send_privmsg(msg, response, True)
            elif response:
                self.send_privmsg(msg, response, True)
            else:
                self.send_privmsg(
                    msg,
                    f'Erro ao executar o comando "{msg.text_command_wop}", verifique sua DM para mais informações',
                    True,
                )

    def cmd_any_template(self, msg, response, count):
        msg.add_attribute("count", count + 1)
        self.send_privmsg(msg, self.handle_variables(msg, response))

    # Loop principal
    async def messages_listener(self):
        while True:
            received_msgs = self.chat.recv(2048).decode()
            for received_msg in received_msgs.split("\r\n"):
                self.handle_msg(received_msg)
            await asyncio.sleep(1)


if __name__ == "__main__":
    bot = GrowBot("growb0t", ["xgrowingsky", "j4panet"])
    bot.connect()
