import asyncio
import os
import platform
import time

from discord.ext import commands
from Command import Command
from Status import Status
from Log import Log
import datetime
import threading


def get_token():
    if platform.system() == 'Windows':
        token_path = os.getcwd() + '\\token'
    else:
        token_path = os.getcwd() + '/token'
    t = open(token_path, 'r', encoding='utf-8')
    return t.read()


class Program:
    IDLE_TIME = 1

    def __init__(self):
        self.last_time = datetime.datetime.now()
        self.idle_status = True
        self.logger = Log(self.__class__.__name__)
        self.bot = commands.Bot(command_prefix='!')
        self.bot.add_cog(Command(self.bot))
        self.bot.add_cog(Status(self.bot))
        # self.bot.get_cog("Status").waiting()

        # Todo 휴면 상태로 나가기 할 때 에러남.
        # self.idle = threading.Thread(target=self.idle_thread)
        # self.idle.start()

    # 쓰레드 사용을 위한 렙핑 메소드
    def idle_thread(self):
        asyncio.run(self.idle_check())

    # 휴면 상태 체크
    async def idle_check(self):
        while True:
            self.logger.info("휴면 상태 체크")
            if self.bot.voice_clients and not self.bot.voice_clients[0].is_playing() and self.idle_status and\
                    self.last_time + datetime.timedelta(minutes=Program.IDLE_TIME) <= datetime.datetime.now():
                self.logger.info("나가기")
                self.idle_status = False
                await self.bot.voice_clients[0].disconnect()
            elif self.bot.voice_clients and self.bot.voice_clients[0].is_playing():
                self.logger.info("휴면 상태 갱신")
                self.idle_status = True
                self.last_time = datetime.datetime.now()

            time.sleep(5)

    def start(self):
        token = get_token()
        self.logger.info(token)
        self.bot.run(token)
