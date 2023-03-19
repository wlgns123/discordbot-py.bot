from cmath import log
from distutils.sysconfig import PREFIX
import discord
from dotenv import load_dotenv
import os
import re
load_dotenv()

TOKEN = os.environ['TOKEN']

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print('작동')
    await bot.change_presence(activity=discord.Game("!도움"))

@bot.command()
async def 도움말(ctx):
    embed=discord.Embed(title="· 지원 명령어", color=0x4ff380)
    embed.add_field(name='· 명령어', value="!유저조회 <광장링크> or <멤버번호> [<> 는 제외 하고 검색하셔야 작동합니다.]\n!도움 [봇 사용법에 대해 안내 하는 명령어 입니다.]", inline=False)
    embed.add_field(name='· 신고하기', value="각종 버그 & 요청사항은 https://discord.gg/H3qe6yNtuA -> 문의하기", inline=False)
    embed.add_field(name='· 이 외 기능', value="해당 봇은 외부정보만 볼 수 있는 봇입니다\nTR 및 호감지수 등을 조회하기 위해선 다른 버전의 조회봇을 사용 하셔야 하며 사용 가능 시간은 18시~23시59분 입니다.", inline=False)
    embed.set_footer(text="· DM 문의 받습니다 20시~23시50분 30분 내외 답장 지훈#3674")
    await ctx.send(embed=embed)

@bot.command()
async def 도움(ctx):
    embed=discord.Embed(title="· 지원 명령어", color=0x4ff380)
    embed.add_field(name='· 명령어', value="!유저조회 <광장링크> or <멤버번호> [<> 는 제외 하고 검색하셔야 작동합니다.]\n!도움 [봇 사용법에 대해 안내 하는 명령어 입니다.]", inline=False)
    embed.add_field(name='· 신고하기', value="각종 버그 & 요청사항은 https://discord.gg/H3qe6yNtuA -> 문의하기", inline=False)
    embed.add_field(name='· 이 외 기능', value="해당 봇은 외부정보만 볼 수 있는 봇입니다\nTR 및 호감지수 등을 조회하기 위해선 다른 버전의 조회봇을 사용 하셔야 하며 사용 가능 시간은 18시~23시59분 입니다.", inline=False)
    embed.set_footer(text="· DM 문의 받습니다 20시~23시50분 30분 내외 답장 지훈#3674")
    await ctx.send(embed=embed)

@bot.command()
async def 유저조회(ctx, member_no):
    pattern = r'\d+'
    result = re.findall(pattern, member_no)
    if result:
        member_no = result[0]
    else:
        await ctx.send('잘못된 형식입니다.')
        return

    url = f"https://api.onstove.com/community/v1.0/user/profile/{member_no}?game_no=2&nocache=$%7BF()%7D"
    response = requests.get(url)
    data = response.json()

    if "result" in data and data["result"] == "404":
        await ctx.send('member를 찾지 못했습니다.')
    else:
        user_info = data["value"]
        username = user_info['cp_home_game_nickname']
        character_uid = user_info['cp_home_game_character_uid']
        email_verify_yn = user_info['email_verify_yn']
        url = f"https://api.onstove.com/community/v1.0/user/{member_no}?member_no={member_no}&character_uid={character_uid}&game_no=2&nocache=${{F()}}"
        response = requests.get(url)
        data = response.json()

    if "result" in data and data["result"] == "404":
        await ctx.send('member를 찾지 못했습니다.')
    else:
        user_info = data["value"]
        channel = user_info['login_provider_cd']
        nickname = user_info['nickname']
        rank = user_info['character_ranking']
        profile = user_info['cp_home_game_profile_img']
        exp = user_info['cp_home_game_exp']
        level = user_info['cp_home_game_level']
        embed=discord.Embed(title="· "f"{username}" " 님의 정보", color=0x4ff380)
        embed.add_field(name='· 캐릭터 UID', value=f"{character_uid}" " / 해당 유저의 Character UID를 조회합니다.", inline=False)
        embed.add_field(name='· 이메일 인증 여부', value=f"{email_verify_yn}" " / 해당 유저의 계정 이메일 인증 유/무를 조회합니다.", inline=False)
        embed.add_field(name='· 채널링', value=f"{channel}" " / 해당 유저의 채널링을 조회합니다.", inline=False)
        embed.add_field(name='· 스토브', value=f"{nickname}" " / 해당 유저의 첫닉네임 또는 스토브 닉네임을 조회합니다.", inline=True)
        embed.add_field(name='· 랭킹', value=f"{rank}" "등 / 해당 유저의 랭킹순위를 조회합니다.", inline=False)
        embed.add_field(name='· 광장프로필', value=f"{profile}" " / 해당 유저의 광장사진을 조회합니다.", inline=True)
        embed.add_field(name='· 경험치', value=f"{exp}" " / 해당 유저의 EXP를 조회합니다.", inline=False)
        embed.add_field(name='· 레벨', value=f"{level}" " / 해당 유저의 레벨을 조회합니다.", inline=False)
        embed.set_footer(text="유저정보 봇 사용으로 더욱 편리하게 게임을 이용하세요.")
        await ctx.send(embed=embed)

try:
    client.run(TOKEN)
except discord.errors.LoginFailure as e:
    print("Improper token has been passed.")
