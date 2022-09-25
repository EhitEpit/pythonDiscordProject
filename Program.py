import asyncio
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
            self.bot = commands.Bot(command_prefix='$', activity=discord.Game(name=Status.WAITING[1]), intents=discord.Intents.all())
        else:
            self.bot = commands.Bot(command_prefix='!', activity=discord.Game(name=Status.WAITING[1]), intents=discord.Intents.all())
        self.status = Status(self.bot)
        self.command = Command(self.bot)

    async def setup(self):
        await self.bot.add_cog(self.status)
        await self.bot.add_cog(self.command)

    def start(self, token=""):
        asyncio.run(self.setup())
        self.bot.run(token)
