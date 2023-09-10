from datetime import datetime, timedelta
from collections import namedtuple
import requests
import sqlite3
import socket
import json
import ssl


DB_PATH = './data.db'

Message = namedtuple(
    'Message',
    'prefix user channel irc_command irc_args text text_command text_args',
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
        with Database(DB_PATH) as cursor:
            cursor.execute(f"SELECT * FROM client_bot WHERE username = '{client_bot}'")
            self.client_username, self.client_id, self.client_secret, self.access_token = cursor.fetchall()[0]
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
        if not self.access_token or len(self.access_token) <= 0:
            self.get_auth_code()
        self.chat_url = "irc.chat.twitch.tv"
        self.chat_port = 6667
        self.irc_server = irc_server
        self.irc_port = irc_port
        self.channels = channels


    def get_oauth_token(self):
        get_oauth_token_url = 'https://id.twitch.tv/oauth2/token'
        get_oauth_token_response =  requests.post(get_oauth_token_url,
                                                  headers={'Content-Type': 'application/x-www-form-urlencoded'},
                                                  data=f'client_id={self.client_id}&client_secret={self.client_secret}&grant_type=client_credentials')
        return get_oauth_token_response.content


    def get_auth_code(self):
        auth_code = input()
        response = requests.post(url='https://id.twitch.tv/oauth2/token',
                                 headers={'Content-Type': 'application/x-www-form-urlencoded'},
                                 data=f'client_id={self.client_id}&client_secret={self.client_secret}&code={auth_code}&grant_type=authorization_code&redirect_uri={self.redirect_uri}')
        response = json.loads(response.content)
        with Database(DB_PATH) as cursor:
            cursor.execute(query = f"""
                           UPDATE client_bot
                           SET 
                               access_token = '{response['access_token']}',
                               expires_in = '{timedelta(seconds=response['expires_in']) + datetime.now()}'
                               refresh_token = '{response['refresh_token']}',
                               scope = '{response['scope']}',
                               username = '{self.username}'
                           WHERE username = '{self.client_username}'""")


    def send_command(self, command):
        print(f'< {command}')
        self.chat.send(f'{command}\r\n'.encode())
    

    def login(self, nickname, password):
        self.chat = ssl.wrap_socket(socket.socket())
        self.chat.connect((self.irc_server, self.irc_port))
        self.send_command(f'PASS oauth:{password}')
        self.send_command(f'NICK {nickname}')


    def connect(self):
        self.login(self.client_username, self.access_token)
        for channel in self.channels:
            self.send_command(f'JOIN #{channel}')
        self.messages_listener()


    def get_user_from_prefix(self, prefix):
        domain = prefix.split('!')[0]
        if domain.endswith('.tmi.twitch.tv'):
            return domain.replace('.tmi.twitch.tv', '')
        if 'tmi.twitch.tv' not in domain:
            return domain
        return None


    def parse_message(self, received_msg):
        parts = received_msg.split(' ')
        
        prefix = None
        user = None
        channel = None
        text = None
        text_command = None
        text_args = None
        irc_command = None
        irc_args = None

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
        if hash_start:
            channel = irc_args[hash_start:][1:]
        
        msg = Message(
            prefix=prefix,
            user=user,
            channel=channel,
            text=text,
            text_command=text_command,
            text_args=text_args,
            irc_command=irc_command,
            irc_args=irc_args
        )
        
        return msg


    def handle_msg(self, msg):
        if msg:
            message = self.parse_message(msg)
            print(f'> [{message.irc_command}] {message.user}: {message.text}')
            if message.irc_command == 'PING':
                self.send_command('PONG :tmi.twitch.tv')
            elif message.irc_command == 'Login unsuccessful':
                return True
            return False
            

    def messages_listener(self):
        while True:
            received_msgs =  self.chat.recv(2048).decode()
            for received_msg in received_msgs.split('\r\n'):
                if self.handle_msg(received_msg):
                    return True

                
if __name__ == '__main__':
    bot = GrowBot('xgrowingsky', ['xgrowingsky'])
    bot.connect()