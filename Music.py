import asyncio

from Log import Log
from discord.ext import commands
import discord
from discord.ext.commands import Context
from youtube_dl import YoutubeDL
import youtube_dl
import Util
from discord.utils import get
from discord import FFmpegPCMAudio
import re


class Music:
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    YDL_OPTIONS = {'format': 'bestaudio/best', 'noplaylist': 'True'}

    def __init__(self, bot: commands.Bot):
        self.logger = Log(self.__class__.__name__)
        self.bot = bot
        self.play_list = []

    async def add_music(self, bot: commands.Bot, ctx: Context, url: str):
        self.logger.info('add_music')
        try:
            is_url_right = re.match('(https?://)?(www\.)?((youtube\.(com))/watch\?v=([-\w]+)|youtu\.be/([-\w]+))', url)
            if is_url_right is None:
                await Util.send_error_msg(ctx, "url이 잘못된 것 같은데?")
                return False
            with YoutubeDL(Music.YDL_OPTIONS) as ydl:
                info = ydl.extract_info(url, download=False)
                I_URL = info['formats'][0]['url']
                source = await discord.FFmpegOpusAudio.from_probe(I_URL, **Music.FFMPEG_OPTIONS)
                self.play_list.append(source)
                self.logger.info("노래 추가: " + str(source))
        except Exception as e:
            self.logger.error('add_music: ' + str(e))
            return False
        return True

    def get_music_source(self):
        self.logger.info('get_music_source')
        self.logger.info("전 노래 개수: " + str(len(self.play_list)))
        if self.play_list:
            source = self.play_list.pop(0)
            self.logger.info('빠져나온 음악: ' + str(source))
            self.logger.info("후 노래 개수: " + str(len(self.play_list)))
            return source

    def play_music(self):
        self.logger.info('play_music')
        try:
            source = self.get_music_source()
            self.bot.voice_clients[0].play(source, after=self.get_next_music)
        except Exception as e:
            self.logger.error('play_music: ' + str(e))

    def get_next_music(self, error):
        self.logger.info('get_next_music')
        try:
            fut = asyncio.run_coroutine_threadsafe(self.play_music(), self.bot.loop)
            fut.result()
        except Exception as e:
            self.logger.error('get_next_music: ' + str(e))
            self.logger.error(str(error))

    def clear_list(self):
        self.play_list.clear()
