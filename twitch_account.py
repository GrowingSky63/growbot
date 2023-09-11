from datetime import datetime, timedelta
from message import Message
import requests
import socket
import json
import ssl


class IRCServer:
    def __init__(self) -> None:
        pass
    
    def send_command(self, command):
        self.chat.send(f"{command}\r\n".encode())
        print(f"< {command}")

    def login(self, nickname, password):
        self.chat = ssl.wrap_socket(socket.socket())
        self.chat.connect((self.irc_server, self.irc_port))
        self.send_command(f"PASS oauth:{password}")
        self.send_command(f"NICK {nickname}")
        self.send_command("CAP REQ :"+' '.join(self.capabilities))
    
    def connect(self):
        self.login()
        for channel in self.channels:
            self.send_command(f"JOIN #{channel}")
        while True:
            received_msgs = self.chat.recv(2048).decode()
            if received_msgs:
                for received_msg in received_msgs.split("\r\n"):
                    Message(received_msg)

class Account:
    def __init__(self, app_nickname, app_id, app_secret, app_redirect_uri='https://localhost:3000'):
        self._app_nickname = app_nickname
        self._app_id = app_id
        self._app_secret = app_secret
        self._app_redirect_uri = app_redirect_uri
        self._capabilities = [
            'twitch.tv/commands',
            'twitch.tv/tags',
            'twitch.tv/membership'
        ]

    def get_oauth_token(self, code=None, refresh_token=None):
        if code and refresh_token:
            raise ValueError("Expected a code, a refresh_token, or none, not both.")
        elif not (code or refresh_token):
            scopes = "+".join([
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
                ])
            auth_code_url = '&'.join([
                'https://id.twitch.tv/oauth2/authorize?',
                f'response_type=code',
                f'client_id={self._app_id}',
                f'redirect_uri={self._app_redirect_uri}',
                f'scope={scopes}'
            ])
            code_input_question = f'\033[32m{auth_code_url}\n\033[34mCole o código aqui: \033[m'
            code = input(code_input_question)
        if refresh_token:
            url_form = '&'.join([
                f'client_id={self._app_id}',
                f'client_secret={self._app_secret}',
                f'refresh_token={refresh_token}',
                f'grant_type=refresh_token',
                f'redirect_uri={self._app_redirect_uri}'
            ])
        elif code:
            url_form = '&'.join([
                f'client_id={self._app_id}',
                f'client_secret={self._app_secret}',
                f'code={code}',
                f'grant_type=authorization_code',
                f'redirect_uri={self._app_redirect_uri}'
            ])
        else:
            url_form = '&'.join([
                f'client_id={self._app_id}',
                f'client_secret={self._app_secret}',
                f'grant_type=client_credentials'
            ])
        response = json.loads(requests.post(
            url="https://id.twitch.tv/oauth2/token",
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data=url_form,
        ).content)

        return (
            response["access_token"],
            response["refresh_token"],
            timedelta(seconds=response["expires_in"]) + datetime.now(),
        )
    
if __name__ == '__main__':
    growbot = Account(
        app_nickname='growb0t',
        app_id='5k0mtdnph592g1b0pmob75q4xz84v2',
        app_secret='5mvu4dtsl6tw4oomnts2teoywytztd'
    )
    credentials = growbot.get_oauth_token(refresh_token='y9jxei6yxsngp7foicjew7puu4gwmqn68hrd1kxofeyspqt1x4')
    print(credentials)