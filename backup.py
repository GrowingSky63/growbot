from datetime import datetime, timedelta
from collections import namedtuple
import requests
import asyncio
import sqlite3
import socket
import json
import ssl

# https://www.twitch.tv/popout/xgrowingsky/chat?popout=
DB_PATH = './data.db'

Message = namedtuple(
    'Message',
    'prefix user channel irc_command irc_args text text_command text_args user_badges user_color_name user_display_name first_message message_id user_is_mod user_is_sub returning_chatter room_id user_id user_type',
)


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


    def __init__(self, client_bot, channels, irc_server='irc.chat.twitch.tv', irc_port=6697, redirect_uri='https://localhost:3000'):
        # Recuperando as informações de autenticação do bot, no banco de dados
        with Database(DB_PATH) as cursor:
            cursor.execute(f"SELECT * FROM client_bot WHERE username = '{client_bot}'")
            self.client_username, self.client_id, self.client_secret = cursor.fetchall()[0]
        
        # Instanciando variaveis para conexão do irc e montagem do link para obtenção do código de autenticação
        self.chat_url = "irc.chat.twitch.tv"
        self.chat_port = 6667
        self.irc_server = irc_server
        self.irc_port = irc_port
        self.channels = channels
        self.redirect_uri = redirect_uri
        self.scopes = '+'.join(
            [
                'chat:read',
                'chat:edit',
                'channel:manage:raids',
                'channel:read:redemptions',
                'channel:manage:redemptions',
                'channel:read:stream_key',
                'channel:read:subscriptions',
                'channel:read:vips',
                'channel:manage:vips',
                'clips:edit',
                'moderation:read',
                'moderator:manage:announcements',
                'moderator:manage:banned_users',
                'moderator:manage:chat_messages',
                'moderator:read:chatters',
                'moderator:read:followers',
                'user:manage:chat_color',
                'user:manage:whispers'
            ])
        self.auth_code_url = f'\033[32mhttps://id.twitch.tv/oauth2/authorize?response_type=code&client_id={self.client_id}&redirect_uri={self.redirect_uri}&scope={self.scopes}\033[m\n\033[34mCole o código aqui: \033[m'

        # Checando validade do token
        with Database(DB_PATH) as cursor:
            cursor.execute(f"SELECT tokens.access_token, tokens.refresh_token, tokens.expires_in FROM tokens WHERE tokens.client_id = '{self.client_id}'")
            data = cursor.fetchall()
        if data:
            self.access_token, self.refresh_token, self.expires_in = data[0]
            self.expires_in = datetime.strptime(self.expires_in, "%Y-%m-%d %H:%M:%S")
        else:
            self.access_token, self.refresh_token, self.expires_in = self.get_auth_code('authorization_code')
        if (self.expires_in - datetime.now()) < timedelta(0):
            self.access_token, self.refresh_token, self.expires_in = self.get_auth_code('refresh_token', self.refresh_token)


    def get_auth_code(self, grant_type, code=None):
        if code is None:
            code = input(self.auth_code_url)
        if grant_type == 'refresh_token':
            url_form = f'client_id={self.client_id}&client_secret={self.client_secret}&refresh_token={code}&grant_type={grant_type}&redirect_uri={self.redirect_uri}'
        elif grant_type == 'authorization_code':
            url_form = f'client_id={self.client_id}&client_secret={self.client_secret}&code={code}&grant_type={grant_type}&redirect_uri={self.redirect_uri}'
        elif grant_type == 'client_credentials':
            url_form = f'client_id={self.client_id}&client_secret={self.client_secret}'

        response = requests.post(
            url='https://id.twitch.tv/oauth2/token',
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
            data=url_form
        )
        response = json.loads(response.content)

        with Database(DB_PATH) as cursor:
            cursor.execute(f'SELECT tokens.* FROM tokens WHERE username = "{self.client_username}";')
            if cursor.fetchall():
                cursor.execute(f"UPDATE tokens SET access_token = ?, expires_in = ?, refresh_token = ?, scope = ? WHERE username = ?",
                    (
                        response['access_token'],
                        (timedelta(seconds=response['expires_in']) + datetime.now()).strftime('%Y-%m-%d %H:%M:%S'),
                        response['refresh_token'],
                        '+'.join(response['scope']),
                        self.client_username
                    )
                )
            else:
                cursor.execute(
                    f"INSERT INTO tokens (client_id, access_token, expires_in, refresh_token, scope, username) VALUES (?, ?, ?, ?, ?, ?)",
                    (
                        self.client_id,
                        response['access_token'],
                        (timedelta(seconds=response['expires_in']) + datetime.now()).strftime('%Y-%m-%d %H:%M:%S'),
                        response['refresh_token'],
                        '+'.join(response['scope']),
                        self.client_username
                    )
                )
        return (response['access_token'], response['refresh_token'], timedelta(seconds=response['expires_in']) + datetime.now())


    def send_command(self, command):
        self.chat.send(f'{command}\r\n'.encode())
        print(f'< {command}')
    

    def login(self, nickname, password):
        self.chat = ssl.wrap_socket(socket.socket())
        self.chat.connect((self.irc_server, self.irc_port))
        self.send_command(f'PASS oauth:{password}')
        self.send_command(f'NICK {nickname}')
        self.send_command('CAP REQ :twitch.tv/commands twitch.tv/tags twitch.tv/membership')


    def connect(self):
        loop = asyncio.get_event_loop()
        self.login(self.client_username, self.access_token)
        for channel in self.channels:
            self.send_command(f'JOIN #{channel}')
        loop.run_until_complete(self.messages_listener())
    

    def enter_channel(self, channel):
        self.send_command(f'JOIN #{channel}')


    def get_user_from_prefix(self, prefix):
        domain = prefix.split('!')[0]
        if domain.endswith('.tmi.twitch.tv'):
            return domain.replace('.tmi.twitch.tv', '')
        if 'tmi.twitch.tv' not in domain:
            return domain
        return None


    def parse_message(self, received_msg):
        parts = received_msg.split(' ')
        
        user_badges = None
        user_color_name = None
        user_display_name = None
        first_message = None
        message_id = None
        user_is_mod = None
        user_is_sub = None
        returning_chatter = None
        room_id = None
        user_id = None
        user_type = None
        prefix = None
        user = None
        channel = None
        text = None
        text_command = None
        text_args = None
        irc_command = None
        irc_args = None

        if parts[0].startswith('@'):
            tags = parts[0].split(';')
            tags = {key:value for key,value in [tag.split('=') for tag in tags]}
            tags_keys = tags.keys()
            if 'badges' in tags_keys:
                user_badges = [badge.split('/')[0] for badge in tags['badges'].split(',')]
            if 'color' in tags_keys:
                user_color_name = tags['color']
            if 'display-name' in tags_keys:
                user_display_name = tags['display-name']
            if 'first-msg' in tags_keys:
                first_message = tags['first-msg']
            if 'id' in tags_keys:
                message_id = tags['id']
            if 'mod' in tags_keys:
                user_is_mod = tags['mod']
            if 'subscriber' in tags_keys:
                user_is_sub = tags['subscriber']
            if 'returning-chatter' in tags_keys:
                returning_chatter = tags['returning-chatter']
            if 'room-id' in tags_keys:
                room_id = tags['room-id']
            if 'user-id' in tags_keys:
                user_id = tags['user-id']
            if 'user-type' in tags_keys:
                user_type = tags['user-type']

            parts = parts[1:]
        
        if parts[0].startswith(':'):
            prefix = parts[0][1:]
            user = self.get_user_from_prefix(prefix)
            parts = parts[1:]

        text_start = next((idx for idx, msg in enumerate(parts) if msg.startswith(':')), None)
        if text_start:
            text_parts = parts[text_start:]
            text_parts[0] = text_parts[0][1:]
            text = ' '.join(text_parts)
            text_command = text_parts[0].lower()
            text_args = text_parts[1:]
            parts = parts[:text_start]
        
        irc_command = parts[0]
        irc_args = parts[1:]

        hash_start = next((idx for idx, part in enumerate(irc_args) if part.startswith('#')), None)
        if hash_start != None:
            channel = irc_args[hash_start][1:]
        
        msg = Message(
            prefix=prefix,
            user=user,
            channel=channel,
            text=text,
            text_command=text_command,
            text_args=text_args,
            irc_command=irc_command,
            irc_args=irc_args,
            user_badges=user_badges,
            user_color_name=user_color_name,
            user_display_name=user_display_name,
            first_message=first_message,
            message_id=message_id,
            user_is_mod=user_is_mod,
            user_is_sub=user_is_sub,
            returning_chatter=returning_chatter,
            room_id=room_id,
            user_id=user_id,
            user_type=user_type
        )

        return msg


    def handle_msg(self, msg):
        if msg:
            message = self.parse_message(msg)
            print(f'> [{message.irc_command}] {message.user}: {message.text}')
            if message.irc_command == 'PING':
                self.send_command('PONG :tmi.twitch.tv')
            elif message.text and 'salve' in message.text:
                self.send_command(f'PRIVMSG #{message.channel} :Salve dog')
            elif message.text_command == '!prime':
                if 'premium' in message.user_badges and message.user_is_sub == '0':
                    self.send_command(f'PRIVMSG #{message.channel} :E esse prime @{message.user}, tá pra jogo?')
                elif 'premium' in message.user_badges and message.user_is_sub == '1':
                    self.send_command(f'PRIVMSG #{message.channel} :Silvio agradece a humildade. @{message.user} é prime e SUB.')
                elif 'premium' not in message.user_badges and message.user_is_sub == '1':
                    self.send_command(f'PRIVMSG #{message.channel} :@{message.user} é SUB sem prime, que cara foda.')
                elif 'premium' not in message.user_badges and message.user_is_sub == '0':
                    self.send_command(f'PRIVMSG #{message.channel} :@{message.user} Compra um pirmezinho aí boy, vale a pena!')
                
            #elif True:
            #    with Database(DB_PATH) as cursor:
            #        cursor.execute(f"SELECT * FROM template_commands WHERE cmd_name = '{message.text_command}'")
            #        data = cursor.fetchall()
            #        if data:
            #            cmd_id, channel, cmd_name, cmd_aliases, cmd_msg, cmd_desc, cmd_universal_delay, cmd_individual_delay = data[0]
                    



    async def messages_listener(self):
        while True:
            received_msgs =  self.chat.recv(2048).decode()
            for received_msg in received_msgs.split('\r\n'):
                self.handle_msg(received_msg)
            await asyncio.sleep(1)

                
if __name__ == '__main__':
    bot = GrowBot('growb0t', ['xgrowingsky', 'silviuss9'])
    bot.connect()
