from Log import Log
from discord.ext import commands, tasks
import discord
import datetime


class Status(commands.Cog):
    IDLE_TIME = 1

    status = {
        "waiting": "대기중"
    }

    def __init__(self, bot: commands.Bot):
        self.logger = Log(self.__class__.__name__)
        self.bot = bot
        self.last_time = datetime.datetime.now()

    # 대기 상태
    async def waiting(self):
        await self.bot.change_presence(activity=discord.Game(name="심심해"))
        
    # 노래 중 상태
    async def singing(self):
        await self.bot.change_presence(activity=discord.Game(name="노래"))

    # 휴면 상태 체크 시작
    def idle_check_on(self):
        self.idle_check.start()

    # 휴면 상태 체크 끝
    def idle_check_off(self):
        self.idle_check.cancel()

    # 휴면 상태 체크
    @tasks.loop(seconds=5.0)
    async def idle_check(self):
        self.logger.info("휴면 상태 체크")
        if self.bot.voice_clients:
            if self.bot.voice_clients[0].is_playing():
                self.logger.info("휴면 상태 갱신")
                self.last_time = datetime.datetime.now()
            elif self.last_time + datetime.timedelta(minutes=Status.IDLE_TIME) <= datetime.datetime.now():
                self.logger.info("나가기")
                await self.bot.voice_clients[0].disconnect()
        else:
            self.idle_check_off()
