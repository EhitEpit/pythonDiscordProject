from typing import Any

from discord.ext.commands import Context
from discord import Message
from multipledispatch import dispatch
from datetime import datetime
import random
from enum import Enum, auto

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


async def send_error_msg(ctx: Context, msg: str, sec=5):
    await ctx.send(msg, delete_after=sec)


def get_fairy_message():
    return fairy_msg_list[random.randint(0, len(fairy_msg_list) - 1)]


def get_loop_message(loop_type):
    if loop_type == 'none':
        return '없음'
    elif loop_type == 'once':
        return '한곡반복'
    elif loop_type == 'all':
        return '전체반복'

class StrEnum(str, Enum):
    def _generate_next_value_(value, start, count, last_values):
        return value

    def __str__(self):
        return self.value


class Message(StrEnum):
    HELLO = '무~ 야~ 호~!'
    ASSEMBLE = '레식하러 다들모여!!!'
    BUSY = '바빠서 못해주는데?'

    ANSWER_PING = '퐁!'
    ANSWER_HELLO = '하위~'

    WRONG_MUSIC_URL = 'URL이 잘못된 것 같은데?'
    WRONG_SITUATION_COMMAND = '응~ 그럴 상황은 아냐~'

    DONT_JOIN_VOICE_CHANNEL = '음성 채널에 들어가고 나서 말해'
    DONT_END = '시작시키고나 말하시지'

    ALREADY_EXCUTE = '이미 실행 중이야'
    ALREADY_JOIN_VOICE_CHANNEL = '이미 들어와 있는데?'
    ALREADY_JOIN_OTHER_VOICE_CHANNEL = '다른 채널에 있는데?'
    ALREADY_NOT_JOIN_VOICE_CHANNEL = '원래 없었는데 뭔소리야'

    NOT_EXIST_DELETE_MESSAGE = '기록된 삭제 메시지가 없어!'
    NOT_PERMISSION = '자격 미달!'

    START_FAIRY = '척추의 요정 시작!'
    END_FAIRY = '척추의 요정 끝!'

    LOOP_MODE = '반복 모드'

    NOW_PLAYING_MUSIC = '현재 재생 중인 음악'

