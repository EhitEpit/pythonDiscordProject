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
            file_data = await YTDLSource.from_url(url, loop=bot.loop)
            self.play_list.append(file_data)
            self.logger.info("노래 추가: " + str(file_data))
        except Exception as e:
            self.logger.error('add_music: ' + str(e))
            return False
        return True

    def get_music_source(self):
        self.logger.info('get_music_source')
        self.logger.info("전 노래 개수: " + str(len(self.play_list)))
        if len(self.play_list) > 0:
            source = discord.PCMVolumeTransformer(
                discord.FFmpegPCMAudio(executable="C:\\ffmpeg-master-latest-win64-gpl\\bin\\ffmpeg.exe",
                                       source=self.play_list.pop(0)['file_name']))
            self.logger.info('music source: ' + str(source))
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


class YTDLSource(discord.PCMVolumeTransformer):
    ytdl_format_options = {
        'format': 'bestaudio/best',
        'restrictfilenames': True,
        'noplaylist': True,
        'nocheckcertificate': True,
        'ignoreerrors': False,
        'logtostderr': False,
        'quiet': True,
        'no_warnings': True,
        'default_search': 'auto',
        'source_address': '0.0.0.0'  # bind to ipv4 since ipv6 addresses cause issues sometimes
    }
    ytdl = YoutubeDL(ytdl_format_options)

    def __init__(self, source, *, data, volume=0.2):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = ""

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: cls.ytdl.extract_info(url, download=not stream))
        file_data = {}
        if 'entries' in data:
            print(data)
            data = data['entries'][0]
            print(data)
        file_data['id'] = data['id']
        file_data['file_name'] = data['title'] if stream else cls.ytdl.prepare_filename(data)
        file_data['file_title'] = data['title']
        return file_data
