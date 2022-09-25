import datetime
import discord
from discord.ext import commands, tasks
from discord.ext.commands import Context

import Music
import Util
import time
from Log import Log


class Command(commands.Cog):
    _R6S_MEMBER = 957613056391794708

    def __init__(self, bot: commands.Bot):
        self.logger = Log(self.__class__.__name__)
        self.bot = bot
        self.last_msg = []
        self.music = Music.Music(self.bot)
        self.last_time = datetime.datetime.now()

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.get_channel(500644812358156310).send(Util.Message.HELLO, delete_after=5.0)

    # 핑 테스트
    @commands.command(name="핑")
    async def ping(self, ctx: Context):
        import socket
        start_time = time.time()
        await ctx.send(Util.Message.ANSWER_PING)
        end_time = time.time()
        await ctx.send(f'Latency: {round(self.bot.latency * 1000)}ms\n{socket.gethostname()}: {round((end_time - start_time) * 1000)}ms')

    # 인사
    @commands.command(name="안녕")
    async def hello(self, ctx: Context):
        await ctx.send(Util.Message.ANSWER_HELLO + ' ' + Util.get_user_name(ctx) + '!')

    @commands.command(name="음악")
    async def music(self, ctx: Context, url: str):
        channel = ctx.author.voice.channel

        if not channel:  # 명령어를 친 유저가 음성채널에 없는 경우.
            await Util.send_error_msg(ctx, Util.Message.DONT_JOIN_VOICE_CHANNEL)
            return
        elif channel and not self.bot.voice_clients:  # 명령어를 친 유저가 음성채널에 있고, 다른 음성 채널에 봇이 없는 경우
            status = self.bot.get_cog('Status')
            status.idle_check_on()
            await status.singing()
            await channel.connect()
            await self.music.add_music(ctx, url)
            ctx.voice_client.play(self.music.get_music_source(), after=self.music.get_next_music)
        elif channel is self.bot.voice_clients[0].channel:  # 명령어를 친 유저가 음성채널에 있고, 그 음성태널에 이미 봇이 있는 경우
            await self.music.add_music(ctx, url)
            if not self.bot.voice_clients[0].is_playing():
                ctx.voice_client.play(self.music.get_music_source(), after=self.music.get_next_music)
        else:
            await Util.send_error_msg(ctx, Util.Message.ALREADY_JOIN_VOICE_CHANNEL)
            return

    @commands.command(name="일시정지")
    async def pause(self, ctx: Context):
        voice = self.bot.voice_clients[0]
        if voice.is_playing():
            voice.pause()
        else:
            await Util.send_error_msg(ctx, Util.Message.WRONG_SITUATION_COMMAND)

    @commands.command(name="재개")
    async def resume(self, ctx: Context):
        voice = self.bot.voice_clients[0]
        if voice.is_paused():
            voice.resume()
        else:
            await Util.send_error_msg(ctx, Util.Message.WRONG_SITUATION_COMMAND)

    @commands.command(name="정지")
    async def stop(self, ctx: Context):
        self.music.clear_list()
        voice = self.bot.voice_clients[0]
        if voice.is_playing():
            voice.stop()
        else:
            await Util.send_error_msg(ctx, Util.Message.WRONG_SITUATION_COMMAND)

    @commands.command(name="스킵")
    async def skip(self, ctx: Context):
        voice = self.bot.voice_clients[0]
        if voice.is_playing():
            voice.stop()
        else:
            await Util.send_error_msg(ctx, Util.Message.WRONG_SITUATION_COMMAND)

    @commands.command(name="목록")
    async def music_list(self, ctx: Context):
        await self.music.send_play_list(ctx)

    @commands.command(name="들어와")
    async def join(self, ctx: Context):
        channel = ctx.author.voice.channel

        if not channel:  # 명령어를 친 유저가 음성채널에 없는 경우.
            await Util.send_error_msg(ctx, Util.Message.DONT_JOIN_VOICE_CHANNEL)
        elif channel and not self.bot.voice_clients:  # 명령어를 친 유저가 음성채널에 있고, 다른 음성 채널에 봇이 없는 경우
            self.bot.get_cog('Status').idle_check_on()
            await channel.connect()
            self.bot.voice_clients[0].stop()
        elif channel is self.bot.voice_clients[0].channel:  # 명령어를 친 유저가 음성채널에 있고, 그 음성채널에 이미 봇이 있는 경우
            await Util.send_error_msg(ctx, Util.Message.ALREADY_JOIN_VOICE_CHANNEL)
        else:
            await Util.send_error_msg(ctx, Util.Message.ALREADY_JOIN_OTHER_VOICE_CHANNEL)

    @commands.command(name="나가")
    async def leave(self, ctx: Context):
        if not self.bot.voice_clients:
            await Util.send_error_msg(ctx, Util.Message.ALREADY_NOT_JOIN_VOICE_CHANNEL)
        elif self.bot.voice_clients[0].channel is ctx.author.voice.channel:
            status = self.bot.get_cog('Status')
            status.idle_check_off()
            await status.waiting()
            self.music.clear_list()
            await self.bot.voice_clients[0].disconnect()
        else:
            await Util.send_error_msg(ctx, Util.Message.WRONG_SITUATION_COMMAND)

    # 메시지 삭제 리스너
    @commands.Cog.listener()
    async def on_message_delete(self, message: discord.Message):
        self.last_msg.append(message)

    # 메시지 삭제 기록 보기
    @commands.command(name="삭제기록")
    async def delete_log(self, ctx: Context):
        if not self.last_msg:
            await Util.send_error_msg(ctx, Util.Message.NOT_EXIST_DELETE_MESSAGE)
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
    @commands.command(name="어셈블")
    async def call_everyone(self, ctx: Context):
        await ctx.send(Util.Message.ASSEMBLE + ' ' + ctx.guild.get_role(Command._R6S_MEMBER).mention)

    # 커맨드 에러
    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error: commands.CommandError):
        if isinstance(error, commands.CommandNotFound):
            message = Util.get_error_message()
        elif isinstance(error, commands.CommandOnCooldown):
            message = f"쿨타임 중... {round(error.retry_after, 1)}초 정도 있다가 다시 해"
        elif isinstance(error, commands.MissingPermissions):
            message = Util.Message.NOT_PERMISSION
        elif isinstance(error, commands.UserInputError):
            message = Util.get_error_message()
        else:
            self.logger.error(error)
            message = Util.Message.BUSY

        await Util.send_error_msg(ctx, message)

    @commands.command(name="척추요정")
    async def spine_fairy_on(self, ctx: Context, *args):
        if args:
            if args[0] == "시작":
                if self.spine_fairy.is_running():
                    await Util.send_error_msg(ctx, Util.Message.ALREADY_EXCUTE)
                    return
                elif ctx.author.voice is None:
                    await Util.send_error_msg(ctx, Util.Message.DONT_JOIN_VOICE_CHANNEL)
                    return

                await ctx.send(Util.Message.START_FAIRY)
                self.spine_fairy.start(ctx)
            elif args[0] == "끝":
                if self.spine_fairy.is_running():
                    await ctx.send(Util.Message.END_FAIRY)
                    self.spine_fairy.stop()
                else:
                    await Util.send_error_msg(ctx, Util.Message.DONT_END)
            else:
                raise commands.CommandNotFound
        else:
            raise commands.CommandNotFound

    @tasks.loop(minutes=10.0)
    async def spine_fairy(self, ctx: Context):
        str = ""
        for member_id in ctx.author.voice.channel.voice_states.keys():
            str += f"<@{member_id}>"
        await Util.send_error_msg(ctx, f"{str} {Util.get_fairy_message()}", 10)
