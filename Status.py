import time

from Log import Log
from discord.ext import commands, tasks
import discord
import datetime


class Status(commands.Cog):
    IDLE_TIME = 1
    WAITING = ("waiting", "심심해")
    SINGING = ("singing", "노래")
    WORKING = ("working", "일")

    def __init__(self, bot: commands.Bot):
        self.logger = Log(self.__class__.__name__)
        self.bot = bot
        self.last_time = datetime.datetime.now()
        self.present_status = "waiting"

    # 대기 상태
    async def waiting(self):
        self.present_status = Status.WAITING[0]
        await self.bot.change_presence(activity=discord.Game(name=Status.WAITING[1]))
        
    # 노래 중 상태
    async def singing(self):
        self.present_status = Status.SINGING[0]
        await self.bot.change_presence(activity=discord.Game(name=Status.SINGING[1]))
        
    # 일하는 중 상태
    async def working(self):
        self.present_status = Status.WORKING[0]
        await self.bot.change_presence(activity=discord.Game(name=Status.WORKING[1]))

    # 휴면 상태 체크 시작
    def idle_check_on(self):
        if not self.idle_check.is_running():
            self.logger.info("휴면 상태 체크 시작")
            self.last_time = datetime.datetime.now()
            self.idle_check.start()

    # 휴면 상태 체크 끝
    def idle_check_off(self):
        if self.idle_check.is_running():
            self.logger.info("휴면 상태 체크 끝")
            self.idle_check.stop()

    # 휴면 상태 체크
    @tasks.loop(seconds=5.0)
    async def idle_check(self):
        if self.bot.voice_clients:
            if self.bot.voice_clients[0].is_playing():
                self.logger.info("휴면 상태 갱신")
                self.last_time = datetime.datetime.now()
            elif self.last_time + datetime.timedelta(minutes=Status.IDLE_TIME) <= datetime.datetime.now():
                self.logger.info("나가기")
                await self.waiting()
                await self.bot.voice_clients[0].disconnect()
        else:
            self.idle_check_off()
