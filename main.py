# # -*- coding: utf-8 -*-
#
# import discord, asyncio, os, youtube_dl
# from discord.ext import commands
# import random
# from Log import Log
#
# logger = Log('discord-bot')
#
# client = commands.Bot(command_prefix='!')
# error_msg_list = ["뭐라고?", "명령어 좀 똑바로 쓰자", "제발 명령어 알고 써라", "뭔솔?"]
# que = {}
# player_list = {}  # 플레이어 리스트
# play_list = list()  # 재생목록 리스트
#
#
# # 에러 메시지를 랜덤으로 골라줌
# def get_error_message():
#     return error_msg_list[random.randint(0, len(error_msg_list) - 1)]
#
#
# def queue(id):  # 음악 재생용 큐
#     if que[id]:
#         player = que[id].pop(0)
#         player_list[id] = player
#         del player_list[0]
#         player.start()
#
#
#
#
# @client.command()
# async def 안녕(ctx):
#     await ctx.send(f'안녕! {get_user_name(ctx)}!')
#
#
# @client.on_error
# async def error(ctx):
#     await ctx.send(f'{get_user_name(ctx)}야... {get_error_message()}')
#
# client.run(get_token())

from Program import Program

program = Program()
program.start()