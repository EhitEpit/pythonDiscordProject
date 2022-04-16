import asyncio
import time

from discord.ext import commands
from Command import Command
from Status import Status
from Log import Log
import datetime




class Program:
    def __init__(self):
        self.last_time = datetime.datetime.now()
        self.idle_status = True
        self.logger = Log(self.__class__.__name__)
        self.bot = commands.Bot(command_prefix='!')
        self.bot.add_cog(Status(self.bot))
        self.bot.add_cog(Command(self.bot))

    def start(self, token=""):
        self.bot.run(token)
