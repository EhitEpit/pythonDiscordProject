import asyncio
import re
import Util
from Log import Log
from discord.ext import commands
import discord
from discord.ext.commands import Context
from youtube_dl import YoutubeDL
import copy


class MusicSource:
    def __init__(self, source, url, title, title_url):
        self.source = source
        self.url = url
        self.title = title
        self.title_url = title_url

    def set_source(self, source):
        self.source = source

    def get_source(self):
        return self.source

    def set_url(self, url):
        self.url = url

    def get_url(self):
        return self.url

    def set_title(self, title):
        self.title = title

    def get_title(self):
        return self.title

    def set_title_url(self, title_url):
        self.title_url = title_url

    def get_title_url(self):
        return self.title_url


class Music:
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    YDL_OPTIONS = {'format': 'bestaudio/best', 'noplaylist': 'False'}
    MAX_PLAYLIST = 30

    def __init__(self, bot: commands.Bot):
        self.logger = Log(self.__class__.__name__)
        self.bot = bot
        self.play_music_list = []
        self.temp = {}
        self.playing_music = None
        self.loop_type = "none"  # none, once, all

    async def add_music(self, ctx: Context, url: str):
        self.logger.info('add_music')
        try:
            is_url_right = re.match(
                '(https?://)?(www\.)?(((music\.)?youtube\.(com))/watch\?v=([-\w]+)|youtu\.be/([-\w]+))', url)
            is_list_url_right = re.match(
                '(https?://)?(www\.)?(((music\.)?youtube\.(com))/playlist\?list=([-\w]+))', url)
            if (is_url_right or is_list_url_right) is None:
                await Util.send_error_msg(ctx, Util.Message.WRONG_MUSIC_URL)
                return False
            with YoutubeDL(Music.YDL_OPTIONS) as ydl:
                info = ydl.extract_info(url, download=False)
                i_urls = []
                if "entries" in info:
                    i_urls = info.get("entries")
                else:
                    i_urls.append(info)

                for index, i_url in enumerate(i_urls):
                    source = await self.download_music_source(i_url['formats'][0]['url'])
                    self.play_music_list.append(MusicSource(source=source, url=i_url['formats'][0]['url'],
                                                            title=str(i_url['title']), title_url=url))

                    if index == 0:
                        if len(i_urls):
                            pass
                        else:
                            pass
                        embed = discord.Embed(title="추가된 음악",
                                              description=str(i_url['title']),
                                              color=0xFFCCE6)
                        embed.set_thumbnail(url=str(i_url['thumbnail']))
                        await ctx.send(embed=embed)

        except Exception as e:
            self.logger.error('add_music: ' + str(e))
            return False
        return True

    async def download_music_source(self, url):
        return await discord.FFmpegOpusAudio.from_probe(url, **Music.FFMPEG_OPTIONS)

    async def wait_add_music_loop(self, music_source):
        source = await self.download_music_source(music_source.get_url())
        temp_music_source = MusicSource(source=source, url=music_source.get_url(), title=music_source.get_title(),
                                        title_url=music_source.get_title_url())
        if self.loop_type == 'all':
            self.play_music_list.append(temp_music_source)
        elif self.loop_type == 'once':
            self.play_music_list.insert(0, temp_music_source)

    def get_music_source(self):
        self.logger.info('get_music_source')
        self.logger.info("전 노래 개수: " + str(len(self.play_music_list)))
        if self.play_music_list:
            music_source = self.play_music_list.pop(0)
            self.playing_music = music_source

            self.bot.loop.create_task(self.wait_add_music_loop(music_source))

            self.logger.info('빠져나온 음악: ' + self.playing_music.get_title())
            self.logger.info("후 노래 개수: " + str(len(self.play_music_list)))
            return music_source.get_source()

    def play_music(self):
        self.logger.info('play_music')
        try:
            source = self.get_music_source()
            if source is None:
                return False
            self.bot.voice_clients[0].play(source, after=self.get_next_music)
        except Exception as e:
            self.logger.error('play_music: ' + str(e))
        return True

    def get_next_music(self, error):
        self.logger.info('get_next_music')
        try:
            if not self.play_music():
                return
        except Exception as e:
            self.logger.error('get_next_music: ' + str(e))

    def get_playing_music(self):
        return discord.Embed(title=Util.Message.NOW_PLAYING_MUSIC + f" ({Util.get_loop_message(self.loop_type)})",
                             description=self.playing_music.get_title(),
                             color=0xFFCCE6)

    async def send_play_list(self, ctx: Context):
        embed = self.get_playing_music()
        embed.add_field(name="====음악 목록====",
                        value=f"대기 중인 음악: {str(len(self.play_music_list))}개",
                        inline=False)
        for index, item in enumerate(self.play_music_list):
            embed.add_field(name=str(index + 1) + ". " + item.get_title(), value=item.get_title_url(), inline=False)
            if index == 4:
                break
        await ctx.send(embed=embed)

    def clear_list(self):
        self.play_music_list.clear()

    def loop(self):
        self.logger.info('loop: ' + self.loop_type)
        if self.loop_type == 'none':
            self.loop_type = 'once'
        elif self.loop_type == 'once':
            self.play_music_list.pop(0)
            self.loop_type = 'all'
        elif self.loop_type == 'all':
            self.loop_type = 'none'

        self.bot.loop.create_task(self.wait_add_music_loop(self.playing_music))

        return self.loop_type
