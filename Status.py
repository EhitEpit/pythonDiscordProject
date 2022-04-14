from Log import Log
from discord.ext import commands
import discord


class Status(commands.Cog):
    status = {
        "waiting": "대기중"
    }

    def __init__(self, bot: commands.Bot):
        self.logger = Log(self.__class__.__name__)
        self.bot = bot

    async def waiting(self):
        await self.bot.change_presence(activity=discord.Game(name=Status.status.get("waiting")))

