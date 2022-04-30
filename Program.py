from discord.ext import commands
from Command import Command
from Status import Status
from Log import Log
import discord
import platform

class Program:
    def __init__(self):
        self.logger = Log(self.__class__.__name__)
        if platform.system() == 'Windows':
            self.bot = commands.Bot(command_prefix='$', activity=discord.Game(name=Status.WAITING[1]))
        else:
            self.bot = commands.Bot(command_prefix='!', activity=discord.Game(name=Status.WAITING[1]))
        self.bot.add_cog(Status(self.bot))
        self.bot.add_cog(Command(self.bot))

    def start(self, token=""):
        self.bot.run(token)
