#-*- coding: utf-8 -*-

import asyncio
import discord
import os
import datetime
import random
from discord.ext import commands

channel = ''
voice_channel = ''
channel_name = []
channel_id = []
channel_voice_name = []
channel_voice_id = []
bossList = []

class Boss(object):
    def __init__(self, name, name2, interval, nextTime, noCut):
        self.Name = name
        self.Name2 = name2
        self.Interval = interval
        self.NextTime = nextTime
        self.NoCut = noCut

token = os.environ["BOT_TOKEN"]

game = discord.Game("명령어를 모르실땐 /도움말을 입력하세요. 보탐 계산")
client = discord.Client()
bot = commands.Bot(command_prefix='/',status=discord.Status.online, activity=game, help_command=None)

boss_path = os.path.dirname(os.path.abspath(__file__)) + "/boss_init.txt"
b = open(boss_path, "r", encoding="utf-8")

while True:
    boss = b.readline().split()
    if not boss:
        break

    if len(boss) != 3:
        continue

    bossList.append(Boss(boss[0], boss[1], float(boss[2]), "모름", 0))

# 입력한 보스의 시간 출력
async def info_embed(boss):
    nextTime = boss.NextTime
    if(nextTime != "모름"):
        nextTime = str(datetime.date.strftime(boss.NextTime, '%H:%M:%S'))

    if boss.Interval == 0:
        embed=discord.Embed(title=boss.Name + " 리젠 주기 : 고정", description=nextTime, color=0xf3bb76)
    elif boss.Interval == int(boss.Interval):
        embed=discord.Embed(title=boss.Name + " 리젠 주기 : " + str(int(boss.Interval)) + "시간", description=nextTime, color=0xf3bb76)
    else:
        embed=discord.Embed(title=boss.Name + " 리젠 주기 : " + str(boss.Interval) + "시간", description=nextTime, color=0xf3bb76)

    return embed

# 컷한 경우 현재시간 + 리젠주기
async def cut_embed(boss):
    now = datetime.datetime.now()

    if boss.Interval == 0:
        boss.NextTime = await fixed_boss(boss)
    else:
        boss.NextTime = now + datetime.timedelta(hours=boss.Interval)
    boss.NoCut = 0
    embed=discord.Embed(title=boss.Name + " " +  str(datetime.date.strftime(now, '%H:%M:%S')) + " 컷", description=f"다음 " + boss.Name +" : " + str(datetime.date.strftime(boss.NextTime, '%H:%M:%S')), color=0xf3bb76)
    
    return embed

# 시간입력하여 컷한 경우 컷시간 + 리젠주기
async def precut_embed(boss, cutTime):
    if boss.Interval == 0:
        boss.NextTime = await fixed_boss(boss)
    else:
        boss.NextTime = cutTime + datetime.timedelta(hours=boss.Interval)
    boss.NoCut = 0
    embed=discord.Embed(title=boss.Name + " " +  str(datetime.date.strftime(cutTime, '%H:%M:%S')) + " 컷", description=f"다음 " + boss.Name +" : " + str(datetime.date.strftime(boss.NextTime, '%H:%M:%S')), color=0xf3bb76)
    
    return embed

# 안잡은 경우 전탐 + 리젠주기
async def nocut_embed(boss):
    if boss.Interval == 0:
        boss.NextTime = await fixed_boss(boss)
    else:
        boss.NextTime = boss.NextTime + datetime.timedelta(hours=boss.Interval)
    boss.NoCut = boss.NoCut + 1
    if boss.NoCut == 5:
        boss.NextTime = str("모름")

# 멍일 경우 전탐 + 리젠주기
async def skip_embed(boss):
    now = datetime.datetime.now()

    if boss.Interval == 0:
        await fixed_boss(boss)
    elif boss.NextTime == "모름":
        boss.NextTime = now + datetime.timedelta(hours=boss.Interval)
    #elif now > boss.NextTime:
    #    boss.NextTime = boss.NextTime + datetime.timedelta(hours=int(boss.Interval))
    boss.NoCut = 0
    embed=discord.Embed(title=boss.Name + " 멍", description=f"다음 " + boss.Name +" : " + str(datetime.date.strftime(boss.NextTime, '%H:%M:%S')), color=0xf3bb76)
    
    return embed

# 특정보스 시간 초기화
async def init_embed(boss):
    if boss.Interval != 0:
        boss.NextTime = str("모름")
        boss.NoCut = 0
    embed=discord.Embed(title=boss.Name + " 초기화", color=0xf3bb76)
    
    return embed

# 고정보스 리젠시간 계산
async def fixed_boss(boss):
    nextTime = boss.NextTime
    timeList = []
    
    if boss.Name == '네크':
        timeList = [ datetime.datetime.combine(datetime.date.today(), datetime.time(1)), 
        datetime.datetime.combine(datetime.date.today(), datetime.time(3)),
        datetime.datetime.combine(datetime.date.today(), datetime.time(5)),
        datetime.datetime.combine(datetime.date.today(), datetime.time(7)),
        datetime.datetime.combine(datetime.date.today(), datetime.time(9)),
        datetime.datetime.combine(datetime.date.today(), datetime.time(11)),
        datetime.datetime.combine(datetime.date.today(), datetime.time(13)),
        datetime.datetime.combine(datetime.date.today(), datetime.time(15)),
        datetime.datetime.combine(datetime.date.today(), datetime.time(17)),
        datetime.datetime.combine(datetime.date.today(), datetime.time(19)),
        datetime.datetime.combine(datetime.date.today(), datetime.time(21)),
        datetime.datetime.combine(datetime.date.today(), datetime.time(23))]
        
    elif boss.Name == '바포':
        timeList = [ datetime.datetime.combine(datetime.date.today(), datetime.time(14, 20)), 
        datetime.datetime.combine(datetime.date.today(), datetime.time(20))]

    now = datetime.datetime.now()
    for time in timeList:
        if now < time:
            nextTime = time
            break
        elif time == timeList[len(timeList) - 1]:
            nextTime = timeList[0] + datetime.timedelta(days=1)

    return nextTime

async def get_guild_channel_info():
    text_channel_name : list = []
    text_channel_id : list = []
    voice_channel_name : list = []
    voice_channel_id : list = []

    for guild in bot.guilds:
        for text_channel in guild.text_channels:
            text_channel_name.append(text_channel.name)
            text_channel_id.append(str(text_channel.id))
    for voice_channel in guild.voice_channels:
        voice_channel_name.append(voice_channel.name)
        voice_channel_id.append(str(voice_channel.id))

    return text_channel_name, text_channel_id, voice_channel_name, voice_channel_id

async def PlaySound(fileName):
    global voice_channel

    source = discord.FFmpegPCMAudio(fileName)

    try:
        if voice_channel.is_connected():
            voice_channel.play(source)

        #voice_channel.play(source)
    except discord.errors.ClientException:
        while voice_channel.is_playing():
            await asyncio.sleep(1)
    while voice_channel.is_playing():
        await asyncio.sleep(1)
    voice_channel.stop()
    source.cleanup()

# property filter 함수
def contains(list, filter):
    for x in list:
        if filter(x):
            return True
    return False

def find(list, filter):
    for x in list:
        if filter(x):
            return x
    return None

async def task():
    await bot.wait_until_ready()

    global channel

    while True:
        if (channel != ''):
            sortedList = bossList
            sortedList.sort(key = lambda x: str(x.NextTime))
            
            now = datetime.datetime.now()
            for boss in sortedList:
                    nextTime = boss.NextTime

                    if(boss.NextTime == "모름"):
                        continue

                    if (now > nextTime):
                        await nocut_embed(boss)
                        if(boss.NextTime == "모름"):
                            continue
                    
                    compTime5 = boss.NextTime - datetime.timedelta(minutes=5)
                    compTime1 = boss.NextTime - datetime.timedelta(minutes=1)
                    embed = ''

                    if now.year == nextTime.year and now.month == nextTime.month and now.day == nextTime.day and now.hour == nextTime.hour and now.minute == nextTime.minute and now.second == nextTime.second:
                        embed=discord.Embed(title=boss.Name + " 보스타임 입니다.", description='예정시간 : ' + str(datetime.date.strftime(nextTime, '%H:%M:%S')), color=0xf3bb76)
                        if voice_channel != '' and voice_channel.is_connected():
                            if boss.Interval != 0:
                                await PlaySound('./sound/' + boss.Name + '젠.mp3')
                    elif now.year == compTime5.year and now.month == compTime5.month and now.day == compTime5.day and now.hour == compTime5.hour and now.minute == compTime5.minute and now.second == compTime5.second:
                        embed=discord.Embed(title=boss.Name + " 보스타임 5분전 입니다.", description='예정시간 : ' + str(datetime.date.strftime(nextTime, '%H:%M:%S')), color=0xf3bb76)
                        if voice_channel != '' and voice_channel.is_connected():
                            if boss.Interval != 0:
                                await PlaySound('./sound/' + boss.Name + '알림1.mp3')
                    elif now.year == compTime1.year and now.month == compTime1.month and now.day == compTime1.day and now.hour == compTime1.hour and now.minute == compTime1.minute and now.second == compTime1.second:
                        embed=discord.Embed(title=boss.Name + " 보스타임 1분전 입니다.", description='예정시간 : ' + str(datetime.date.strftime(nextTime, '%H:%M:%S')), color=0xf3bb76)
                        if voice_channel != '' and voice_channel.is_connected():
                            if boss.Interval != 0:
                                await PlaySound('./sound/' + boss.Name + '알림.mp3')

                    if embed != '':
                        await channel.send(embed=embed)
        
        await asyncio.sleep(1)

# 봇 시작
@bot.event
async def on_ready():
    global channel_name
    global channel_id
    global channel_voice_name
    global channel_voice_id

    print("봇 시작")
    print(bot.user.name)
    print(bot.user.id)
    bossList[4].NextTime = await fixed_boss(bossList[4])
    bossList[20].NextTime = await fixed_boss(bossList[20])
    print("=================")
    channel_name, channel_id, channel_voice_name, channel_voice_id = await get_guild_channel_info()

@bot.command(pass_context=True)
async def 도움말(ctx):
    embed=discord.Embed(title=f"보스타임 봇 입니다.", description=f"아래 명령을 확인해 주세요!", color=0xf3bb76)
    embed.add_field(name=f"/초기화", value=f"모든 보스타임을 초기화 합니다.", inline=False)
    embed.add_field(name=f"보스 ", value=f"전체 보스타임을 출력합니다.", inline=False)
    embed.add_field(name=f"보탐", value=f"1시간 이내 보스타임을 출력합니다.", inline=False)
    embed.add_field(name=f"[보스이름]", value=f"입력한 보스의 보스타임을 출력 합니다.", inline=False)
    embed.add_field(name=f"[보스이름] 컷", value=f"현재 잡은시간에서 보스타임을 업데이트 합니다.", inline=False)
    embed.add_field(name=f"[보스자음] ㅋ", value=f"현재 잡은시간에서 보스타임을 업데이트 합니다.", inline=False)
    embed.add_field(name=f"[보스이름] [시간] [분] 컷", value=f"입력한 시간, 분에 잡은시간으로 보스타임을 업데이트 합니다.", inline=False)
    embed.add_field(name=f"[보스자음] [시간] [분] ㅋ", value=f"입력한 시간, 분에 잡은시간으로 보스타임을 업데이트 합니다.", inline=False)
    embed.add_field(name=f"[보스이름] 멍", value=f"이전에 잡은 시간에서 보스타임을 업데이트 합니다.", inline=False)
    embed.add_field(name=f"[보스자음] ㅁ", value=f"이전에 잡은 시간에서 보스타임을 업데이트 합니다.", inline=False)
    embed.add_field(name=f"[보스이름] 초기화", value=f"입력한 보스타임을 초기화 합니다.", inline=False)
    embed.add_field(name=f"분배 [가격] [인원수] ", value=f"분배 가격을 계산합니다.(가격은 판사람이 거래소에 올린 가격)", inline=False)
    embed.add_field(name=f"사다리 [이름] [이름] [당첨자수] ", value=f"입력된 이름에서 당첨자수 만큼 추첨합니다.", inline=False)
    await ctx.send(embed=embed)

    embed=discord.Embed(title=f"보스이름 목록", description=f"보스이름을 확인 후 명령을 입력해 주세요!", color=0xf3bb76)
    for boss in bossList:
        nextTime = boss.NextTime
        if(nextTime != "모름"):
            nextTime = str(datetime.date.strftime(boss.NextTime, '%H:%M:%S'))

        if boss.Interval == 0:
            embed.add_field(name=boss.Name + "(" + boss.Name2 + ")", value=" 리젠 주기 : 고정")
        elif boss.Interval == int(boss.Interval):
            embed.add_field(name=boss.Name + "(" + boss.Name2 + ")", value=" 리젠 주기 : " + str(int(boss.Interval)) + "시간")
        else:
            embed.add_field(name=boss.Name + "(" + boss.Name2 + ")", value=" 리젠 주기 : " + str(boss.Interval) + "시간")
    await ctx.send(embed=embed)

@bot.command(pass_context=True)
async def 초기화(ctx):
    embed=discord.Embed(title=f"보스타임을 초기화 합니다.", color=0xf3bb76)
    for boss in bossList:
        if boss.Interval == 0:
            boss.NextTime = await fixed_boss(boss)
            embed.add_field(name=boss.Name + " 리젠 주기 : 고정", value=boss.NextTime)
        else:
            boss.NextTime = "모름"
            if boss.Interval == int(boss.Interval):
                embed.add_field(name=boss.Name + " 리젠 주기 : " + str(int(boss.Interval)) + "시간", value=boss.NextTime)
            else:
                embed.add_field(name=boss.Name + " 리젠 주기 : " + str(boss.Interval) + "시간", value=boss.NextTime)
    await ctx.send(embed=embed)

@bot.command(pass_context=True)
async def 저장(ctx):
    boss_path = os.path.dirname(os.path.abspath(__file__)) + "/boss_save.txt"
    b = open(boss_path, "w", encoding="utf-8")
    
    for boss in bossList:
        if(boss.NextTime == "모름"):
            continue
        b.write(boss.Name + "\t" + str(datetime.date.strftime(boss.NextTime, '%Y-%m-%d %H:%M:%S')) + "\n")
    
    b.close()
        
    embed=discord.Embed(title=f"보스타임을 저장 했습니다.", description='!로드 시 저장된 보스타임을 로드할 수 있습니다.', color=0xf3bb76)
    await ctx.send(embed=embed)

@bot.command(pass_context=True)
async def 로드(ctx):
    boss_path = os.path.dirname(os.path.abspath(__file__)) + "/boss_save.txt"
    b = open(boss_path, "r", encoding="utf-8")
    
    while True:
        boss = b.readline().split()
        if not boss:
            break

        if len(boss) != 3:
            continue
        
        loadTime = datetime.datetime.strptime(boss[1] + ' ' + boss[2], '%Y-%m-%d %H:%M:%S')
        if contains(bossList, lambda x: x.Name == boss[0]):
            loadBoss = find(bossList, lambda x: x.Name == boss[0])
            loadBoss.NextTime = loadTime
    
    b.close()
        
    embed=discord.Embed(title=f"저장된 보스타임을 로드 했습니다.", color=0xf3bb76)
    await ctx.send(embed=embed)

#@bot.command()
#async def join(ctx):
#    global voice_channel
#    voice_channel = ctx.author.voice_channel
#    await Client.join_voice_channel(voice_channel)

#@bot.command()
#async def leave(ctx):
#    await ctx.voice_Client.disconnect()

@bot.event
async def on_message(message):
    await bot.wait_until_ready()

    global channel
    global voice_channel
    
    if(channel == ''):
        channel = message.channel

    if message.author.voice and voice_channel == '':
            voice_channel = await message.author.voice.channel.connect(reconnect = True)
        #voice_channel = await bot.get_channel(message.author.voice.channel).connect(reconnect = True)

    await bot.process_commands(message)
    if message.author.bot:
        return None

    param = message.content.split()
    try:
        if len(param) == 0:
            return None
            
        bossName = param[0]

        #보스이름 입력(ex. 자크)
        if contains(bossList, lambda x: x.Name == bossName):
            nextBoss = find(bossList, lambda x: x.Name == bossName)

            try:
                # 보스 정보
                if len(param) == 1:
                    embed = await info_embed(nextBoss)
                # 컷 or 멍
                elif len(param) == 2:
                    # 컷
                    if param[len(param) - 1].endswith("컷"):
                        embed = await cut_embed(nextBoss)
                    # 멍
                    elif param[len(param) - 1].endswith("멍"):
                        embed = await skip_embed(nextBoss)
                    # 초기화
                    elif param[len(param) - 1].endswith("초기화"):
                        embed = await init_embed(nextBoss)
                elif len(param) == 4:
                    try:
                        hour = int(param[1])
                        minute = int(param[2])
                        cutTime = datetime.datetime.combine(datetime.date.today(), datetime.time(hour, minute))
                        if param[len(param) - 1].endswith("컷"):
                            embed = await precut_embed(nextBoss, cutTime)
                    except ValueError:
                        return None
                else:
                    return None

                if embed != None:
                    await message.channel.send(embed=embed)

            except UnboundLocalError:
                embed = None
            
        #자음 입력(ex. ㅈㅋ)
        elif contains(bossList, lambda x: x.Name2 == bossName):
            nextBoss = find(bossList, lambda x: x.Name2 == bossName)

            try:
                # 보스 정보
                if len(param) == 1:
                    embed = await info_embed(nextBoss)
                # 컷 or 멍
                elif len(param) == 2:
                    # 컷
                    if param[len(param) - 1].endswith("ㅋ"):
                        embed = await cut_embed(nextBoss)

                    elif param[len(param) - 1].endswith("ㅁ"):
                        embed = await skip_embed(nextBoss)
                elif len(param) == 4:
                    try:
                        hour = int(param[1])
                        minute = int(param[2])
                        cutTime = datetime.datetime.combine(datetime.date.today(), datetime.time(hour, minute))
                        if param[len(param) - 1].endswith("ㅋ"):
                            embed = await precut_embed(nextBoss, cutTime)
                    except ValueError:
                        return None
                else:
                    return None

                await message.channel.send(embed=embed)
            except UnboundLocalError:
                embed = None
    except IndexError:
        await message.channel.send("보스 이름을 입력해 주세요")
    
    # 전체 보스타임 출력
    if message.content == "보스":
        embed=discord.Embed(title="전체 보스타임", color=0xf3bb76)
        
        for boss in bossList:
            nextTime = boss.NextTime
            if(nextTime != "모름"):
                nextTime = str(datetime.date.strftime(boss.NextTime, '%H:%M:%S'))

            if boss.Interval == 0:
                embed.add_field(name=boss.Name + " 리젠 주기 : 고정", value=nextTime)
            elif boss.Interval == int(boss.Interval):
                embed.add_field(name=boss.Name + " 리젠 주기 : " + str(int(boss.Interval)) + "시간", value=nextTime)
            else:
                embed.add_field(name=boss.Name + " 리젠 주기 : " + str(boss.Interval) + "시간", value=nextTime)
        await message.channel.send(embed=embed)

    # 전체 보스타임 출력(정렬)
    if message.content == "보탐":

        sortedList = bossList
        sortedList.sort(key = lambda x: str(x.NextTime))
        embed=discord.Embed(title="1시간 이내 보스타임 목록", color=0xf3bb76)
        
        for boss in sortedList:
            nextTime = boss.NextTime
            if(nextTime == "모름"):
                continue

            now = datetime.datetime.now()
            margin = datetime.timedelta(hours=1)
            if now - margin <= nextTime <= now + margin:
                if boss.Interval == 0:
                    embed.add_field(name=boss.Name + " 리젠 주기 : 고정", value=str(datetime.date.strftime(boss.NextTime, '%H:%M:%S')), inline=False)
                elif boss.Interval == int(boss.Interval):
                    embed.add_field(name=boss.Name + " 리젠 주기 : " + str(int(boss.Interval)) + "시간", value=str(datetime.date.strftime(boss.NextTime, '%H:%M:%S')), inline=False)
                else:
                    embed.add_field(name=boss.Name + " 리젠 주기 : " + str(boss.Interval) + "시간", value=str(datetime.date.strftime(boss.NextTime, '%H:%M:%S')), inline=False)
        await message.channel.send(embed=embed)

    # 분배 계산
    if(param[0] == "분배" and len(param) == 3):
        try:
            price = int(param[1])
            member = int(param[2])
            sellPrice = int(price * 0.95)
            exchangePrice = int((sellPrice * 95) / ((member - 1) * 100 + 95) / 0.95)
            distributePrice = int(exchangePrice * 0.95)
            embed=discord.Embed(title="분배계산", color=0xf3bb76)
            embed.add_field(name="판매금액 : " + str(price), value="거래소에 등록할 금액 : " + str(exchangePrice) + ", 분배금액 : " + str(distributePrice))
            await message.channel.send(embed=embed)
        except ValueError:
            await message.channel.send("분배 [가격] [인원수] 로 입력해 주세요")
            

    # 사다리
    if(param[0] == "사다리"):
        try:
            num = int(len(param) - 2) # 사다리 [인원] [당첨자수] 이기때문에 2를 뺌
            win = int(param[len(param) - 1])
            memberList = []

            if (win > num):
                await message.channel.send("당첨자수는 인원수보다 클 수 없습니다.")
            else:
                for i in range(1,len(param) - 1):
                    memberList.append({'Name':param[i],'Result':'꽝'})

                winner = 0
                while winner < win:
                    ran = random.randrange(num)

                    if memberList[ran]['Result'] == '꽝':
                        memberList[ran]['Result'] = '당첨'
                        winner = winner + 1
                
                for member in memberList:
                    await message.channel.send(member['Name'] + " : " + member['Result'])

        except ValueError:
            await message.channel.send("사다리 [이름] [이름] [당첨자수] 로 입력해 주세요")
    
bot.loop.create_task(task())
#asyncio.set_event_loop(loop)

try:
    bot.loop.run_until_complete(bot.start(token))
except SystemExit:
    channel = ''
