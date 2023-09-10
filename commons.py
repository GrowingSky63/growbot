from openpyxl import load_workbook
from datetime import datetime
from time import sleep
import sqlite3
import pygame
import sys
import os


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


class Workbook:

    def __init__(self, wb_path:os.path, wb_template:os.path=None, sheet=None):
        if wb_template:
            self.wb_path = wb_template
            self.safe_as = wb_path
        else:
            self.wb_path = wb_path
            self.safe_as = self.wb_path
        self.sheet = sheet
    
    def __enter__(self):
        self.wb = load_workbook(self.wb_path)
        if self.sheet:
            self.sheet = self.wb[self.sheet]
        else:
            self.sheet = self.wb.active
        return self.sheet
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.wb.save(self.wb_path)


def play(path):
    pygame.init()
    pygame.mixer.music.load(path)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pass
    pygame.quit()


if getattr(sys, 'frozen', False):
    MAIN_PATH = os.path.dirname(sys.executable)
elif __file__:
    MAIN_PATH = os.path.dirname(__file__)
DB_PATH = os.path.join(MAIN_PATH, 'data.db')


def find_safe(element, by, value, multi=False, timeout=60):
    while True:
        if timeout > 0:
            try:
                response = element.find_elements(by, value)
                if multi:
                    return response
                else:
                    return response[0]
            except:
                timeout -= 1
                sleep(1)
        else:
            return


def month_mkdir(path:os.path, date:datetime = datetime.now()):
    years = os.listdir(path)
    year = str(date.year)
    path = os.path.join(path, year)
    if year not in years:
        os.mkdir(path)
    months = os.listdir(path)
    month = MONTH[date.month-1]
    path = os.path.join(path, month)
    if month not in months:
        os.mkdir(path)
    return path


MONTH = ['JAN', 'FEV', 'MAR', 'ABR', 'MAI', 'JUN', 'JUL', 'AGO', 'SET', 'OUT', 'NOV', 'DEZ']


months = [
    "Janeiro",
    "Fevereiro",
    "Março",
    "Abril",
    "Maio",
    "Junho",
    "Julho",
    "Agosto",
    "Setembro",
    "Outubro",
    "Novembro",
    "Dezembro"]