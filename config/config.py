import os

from dotenv import load_dotenv

class Bot_config:
    def __init__(self):
        load_dotenv()
        self.getBotEnv()
        self.getClickToken()
        self.getDataBase()


    def getBotEnv(self):
        self.token = os.getenv("BOT_TOKEN", "")

    def getClickToken(self):
        self.click_token = os.getenv("CLICK_TOKEN", "")

    def getDataBase(self):
        self.host = os.getenv("HOST", "")
        self.user = os.getenv("USER", "")
        self.database = os.getenv("DATABASE", "")
        self.password = os.getenv("PASSWORD", "")