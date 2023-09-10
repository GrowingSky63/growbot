from collections import namedtuple
import sqlite3
import sys
import os


Command = namedtuple(
    "Command", "aliases function role universal_delay individual_delay desc usage"
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

def get_template_commands(msg, template_cmd_function) -> dict:
    with Database(DB_PATH) as cursor:
        cursor.execute(
            f"SELECT cmd_name, cmd_msg, count FROM template_commands WHERE channel='{msg.channel}'"
        )
        data = cursor.fetchall()
    template_commands = {
        row[0]: Command(
            aliases=[],
            function=(template_cmd_function, (row[1], int(row[2]))),
            role="vwr",
            universal_delay=10,
            individual_delay=0,
            desc=f'Envia "{row[1]}", no chat',
            usage=f"{msg.commmand_prefix}{row[0]}",
        )
        for row in data
    }
    return template_commands

if getattr(sys, 'frozen', False):
    MAIN_PATH = os.path.dirname(sys.executable)
elif __file__:
    MAIN_PATH = os.path.dirname(__file__)
DB_PATH = os.path.join(MAIN_PATH, 'data.db')
