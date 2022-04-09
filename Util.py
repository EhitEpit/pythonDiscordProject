from discord.ext.commands import Context
from discord import Message
from multipledispatch import dispatch
from datetime import datetime
import random

error_msg_list = ["뭐라고?", "명령어 좀 똑바로 쓰자", "제발 명령어 알고 써라", "뭔솔?", "(╯°□°）╯︵ ┻━┻"]
fairy_msg_list = ["다들 기지개 좀 펴!!", "기지개 필 시간이야~", "엉덩이에 땀띠 나겠다. 좀 일어나라", "적당히 일어나지 그래?"]

@dispatch(Context)
def get_user_name(ctx: Context):
    return str(ctx.author).split('#')[0]


@dispatch(Message)
def get_user_name(msg: Message):
    return str(msg.author).split('#')[0]


def get_content(msg: Message):
    return str(msg.content)


def format_datetime(date: datetime):
    return f'{date.year}년 {date.month}월 {date.day}일 {date.hour}시 {date.minute}분'


def get_error_message():
    return error_msg_list[random.randint(0, len(error_msg_list) - 1)]


async def send_error_msg(ctx: Context, msg: str):
    await ctx.send(msg, delete_after=5)


def get_fairy_message():
    return fairy_msg_list[random.randint(0, len(fairy_msg_list) - 1)]