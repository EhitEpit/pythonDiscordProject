import datetime
import discord
from discord.ext import commands
from discord.ext.commands import Context

import Music
import Util
import time
from Log import Log


class Command(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.logger = Log(self.__class__.__name__)
        self.bot = bot
        self.last_msg = []
        self.spine_fairy_flag = False
        self.music = Music.Music(self.bot)
        self.last_time = datetime.datetime.now()
        self.bot_status = self.bot.get_cog('Status')

    # 핑 테스트
    @commands.command(name="핑")
    async def ping(self, ctx: Context):
        import socket
        start_time = time.time()
        await ctx.send("퐁! ")
        end_time = time.time()
        await ctx.send(f'Latency: {round(self.bot.latency * 1000)}ms\n{socket.gethostname()}: {round((end_time - start_time) * 1000)}ms')

    # 인사
    @commands.command(name="안녕")
    async def hello(self, ctx: Context):
        await ctx.send(f'안녕! {Util.get_user_name(ctx)}!')

    @commands.command(name="음악")
    async def music(self, ctx: Context, url: str):
        channel = ctx.author.voice.channel

        if not channel:  # 명령어를 친 유저가 음성채널에 없는 경우.
            await Util.send_error_msg(ctx, "음성 채널에 들어가고 나서 말해")
            return
        elif channel and not self.bot.voice_clients:  # 명령어를 친 유저가 음성채널에 있고, 다른 음성 채널에 봇이 없는 경우
            self.bot_status.idle_check_on()
            await self.bot_status.singing()
            await channel.connect()
            await self.music.add_music(ctx, url)
            ctx.voice_client.play(self.music.get_music_source(), after=self.music.get_next_music)
        elif channel is self.bot.voice_clients[0].channel:  # 명령어를 친 유저가 음성채널에 있고, 그 음성태널에 이미 봇이 있는 경우
            await self.music.add_music(ctx, url)
            if not self.bot.voice_clients[0].is_playing():
                ctx.voice_client.play(self.music.get_music_source(), after=self.music.get_next_music)
        else:
            await Util.send_error_msg(ctx, "안들려~")
            return

    @commands.command(name="일시정지")
    async def pause(self, ctx: Context):
        voice = self.bot.voice_clients[0]
        if voice.is_playing():
            voice.pause()
        else:
            await Util.send_error_msg(ctx, "응~ 아냐~")

    @commands.command(name="재개")
    async def resume(self, ctx: Context):
        voice = self.bot.voice_clients[0]
        if voice.is_paused():
            voice.resume()
        else:
            await Util.send_error_msg(ctx, "응~ 아냐~")

    @commands.command(name="정지")
    async def stop(self, ctx: Context):
        self.music.clear_list()
        voice = self.bot.voice_clients[0]
        if voice.is_playing():
            voice.stop()
        else:
            await Util.send_error_msg(ctx, "응~ 아냐~")

    @commands.command(name="스킵")
    async def skip(self, ctx: Context):
        voice = self.bot.voice_clients[0]
        if voice.is_playing():
            voice.stop()
        else:
            await Util.send_error_msg(ctx, "응~ 아냐~")

    @commands.command(name="목록")
    async def music_list(self, ctx: Context):
        await self.music.send_play_list(ctx)

    @commands.command(name="들어와")
    async def join(self, ctx: Context):
        print("join")
        channel = ctx.author.voice.channel

        if not channel:  # 명령어를 친 유저가 음성채널에 없는 경우.
            await Util.send_error_msg(ctx, "음성 채널에 들어가고 나서 말해")
        elif channel and not self.bot.voice_clients:  # 명령어를 친 유저가 음성채널에 있고, 다른 음성 채널에 봇이 없는 경우
            self.bot_status.idle_check_on()
            await channel.connect()
            self.bot.voice_clients[0].stop()
        elif channel is self.bot.voice_clients[0].channel:  # 명령어를 친 유저가 음성채널에 있고, 그 음성채널에 이미 봇이 있는 경우
            await Util.send_error_msg(ctx, "응~ 이미 들어와 있어~")
        else:
            await Util.send_error_msg(ctx, "안들려~")

        print(channel)
        print(self.bot.voice_clients[0])

    @commands.command(name="나가")
    async def leave(self, ctx: Context):
        if not self.bot.voice_clients:
            await Util.send_error_msg(ctx, "원래 없었는데 뭔소리야")
        elif self.bot.voice_clients[0].channel is ctx.author.voice.channel:
            self.bot_status.idle_check_off()
            await self.bot_status.waiting()
            self.music.clear_list()
            await self.bot.voice_clients[0].disconnect()
        else:
            await Util.send_error_msg(ctx, "안들려~")

    # 메시지 삭제 리스너
    @commands.Cog.listener()
    async def on_message_delete(self, message: discord.Message):
        self.last_msg.append(message)

    # 메시지 삭제 기록 보기
    @commands.command(name="삭제기록")
    async def delete_log(self, ctx: Context):
        if not self.last_msg:
            await ctx.send("기록된 삭제 메시지가 없어!")
            return

        message = ""
        for item in self.last_msg:
            if item.attachments:
                await ctx.send(
                    f'{Util.get_user_name(item)}이/가 {Util.format_datetime(item.created_at)}에 {item.attachments[0].url} 를 삭제했어.\n')
            else:
                message += f'{Util.get_user_name(item)}이/가 {Util.format_datetime(item.created_at)}에 \"{item.content}\"를 삭제했어.\n'

        self.last_msg.clear()
        await ctx.send(message)

    # 다들 모여!!!(레식채널)
    @commands.command(name="다들모여")
    async def call_everyone(self, ctx: Context):
        await ctx.send(f"레식하러 다들모여!!! {ctx.guild.get_role(957613056391794708).mention}")

    # 커맨드 에러
    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error: commands.CommandError):
        if isinstance(error, commands.CommandNotFound):
            message = Util.get_error_message()
        elif isinstance(error, commands.CommandOnCooldown):
            message = f"쿨타임 중... {round(error.retry_after, 1)}초 정도 있다가 다시 해"
        elif isinstance(error, commands.MissingPermissions):
            message = "자격 미달!"
        elif isinstance(error, commands.UserInputError):
            message = Util.get_error_message()
        else:
            self.logger.error(error)
            message = "바빠서 못해주는데?"

        await ctx.send(message, delete_after=5)

    # @commands.command(name="척추의요정시작")
    # async def start_spine_fairy(self, ctx: Context, *args):
    #     if self.spine_fairy_flag:
    #         await Util.send_error_msg(ctx, "이미 실행 중이니 껐다가 다시 켜")
    #
    #     fairy_time = 300
    #     if args and len(args) == 0:
    #         try:
    #             fairy_time = int(args[0]) * 60
    #         except Exception as e:
    #             self.logger.error(e)
    #
    #     await ctx.send("척추의 요정 시작!")
    #     self.spine_fairy_flag = True
    #     self.work = threading.Thread(target=self.spine_fairy, args=(ctx, fairy_time))
    #     self.work.start()
    #
    # @commands.command(name="척추의요정끝")
    # async def end_spine_fairy(self, ctx: Context):
    #     if self.work is not None:
    #         self.spine_fairy_flag = False
    #         await ctx.send("척추의 요정 끝!")
    #     else:
    #         await ctx.send("시작시키고나 말하시지")
    #
    # def spine_fairy_wrap(self, ctx: Context, fairy_time: int):
    #     asyncio.run(self.spine_fairy(ctx, fairy_time))
    #
    # async def spine_fairy(self, ctx: Context, fairy_time: int):
    #     while self.spine_fairy_flag:
    #         await ctx.send(Util.get_fairy_message())
    #         time.sleep(fairy_time)
