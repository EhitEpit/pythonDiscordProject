import asyncio
import re
import Util
from Log import Log
from discord.ext import commands
import discord
from discord.ext.commands import Context
from youtube_dl import YoutubeDL


class Music:
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    YDL_OPTIONS = {'format': 'bestaudio/best', 'noplaylist': 'True'}

    def __init__(self, bot: commands.Bot):
        self.logger = Log(self.__class__.__name__)
        self.bot = bot
        self.play_source_list = []
        self.play_title_list = []
        self.playing_music = ""

    async def add_music(self, ctx: Context, url: str):
        self.logger.info('add_music')
        try:
            is_url_right = re.match(
                '(https?://)?(www\.)?(((music\.)?youtube\.(com))/watch\?v=([-\w]+)|youtu\.be/([-\w]+))', url)
            if is_url_right is None:
                await Util.send_error_msg(ctx, "url이 잘못된 것 같은데?")
                return False
            with YoutubeDL(Music.YDL_OPTIONS) as ydl:
                info = ydl.extract_info(url, download=False)
                I_URL = info['formats'][0]['url']
                source = await discord.FFmpegOpusAudio.from_probe(I_URL, **Music.FFMPEG_OPTIONS)
                self.play_source_list.append(source)
                self.play_title_list.append((str(info['title']), url))

                embed = discord.Embed(title="추가된 음악",
                                      description=str(info['title']),
                                      color=0xFFCCE6)
                embed.set_thumbnail(url=str(info['thumbnail']))
                await ctx.send(embed=embed)
        except Exception as e:
            self.logger.error('add_music: ' + str(e))
            return False
        return True

    def get_music_source(self):
        self.logger.info('get_music_source')
        self.logger.info("전 노래 개수: " + str(len(self.play_source_list)))
        if self.play_source_list:
            source = self.play_source_list.pop(0)
            self.playing_music = self.play_title_list.pop(0)[0]
            self.logger.info('빠져나온 음악: ' + self.playing_music)
            self.logger.info("후 노래 개수: " + str(len(self.play_source_list)))
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

    def get_playing_music(self):
        return discord.Embed(title="현재 재생 중인 음악",
                             description=self.playing_music,
                             color=0xFFCCE6)

    async def send_play_list(self, ctx: Context):
        embed = self.get_playing_music()
        embed.add_field(name="====음악 목록====", value=f"대기 중인 음악: {str(len(self.play_title_list))}개", inline=False)
        for index, item in enumerate(self.play_title_list):
            embed.add_field(name=str(index + 1) + ". " + item[0], value=item[1], inline=False)
            if index == 4:
                break
        await ctx.send(embed=embed)

    def clear_list(self):
        self.play_source_list.clear()
        self.play_title_list.clear()
