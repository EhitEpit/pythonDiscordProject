import os
import platform
from discord.ext import commands
from Command import Command
from Status import Status
from Log import Log


class Program:
    def __init__(self):
        self.logger = Log(self.__class__.__name__)
        self.bot = commands.Bot(command_prefix='!')
        if platform.system() == 'Windows':
            token_path = os.getcwd() + '\\token'
        else:
            token_path = os.getcwd() + '/token'
        t = open(token_path, 'r', encoding='utf-8')
        self.token = t.read()
        self.bot.add_cog(Command(self.bot))
        self.bot.add_cog(Status(self.bot))
        # self.bot.get_cog("Status").waiting()

    def start(self):
        self.bot.run(self.token)
