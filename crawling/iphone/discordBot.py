
import time
import discord
from discord.ext import tasks
from discord.ext.commands import Bot
from datetime import datetime
import pymysql
import asyncio


ip = "192.168.30.15"
port = 1883
passwd = open("/home/yshong/project/playground/crawling/iphone/passwd.txt", "r").readline()

conn = pymysql.connect(host='192.168.30.15', user='root', password=passwd, db='crwaling', charset='utf8')
cur = conn.cursor()


TOKEN = open("/home/yshong/project/playground/crawling/iphone/TOKEN.txt", "r").readline()
CHANNEL_ID = '945540335495426079'
global mychannel
mychannel = ''

client = discord.Client()
intents = discord.Intents.default()

global last, rtx3060ti_last , rtx3070_last
last = 13
rtx3060ti_last = 1
rtx3070_last = 1

# !로 시작하면 명령어로 인식
bot = Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
  print(f'logged in as {bot.user}')

# !hello 명령어 처리
@bot.command()
async def hello(ctx):
  global mychannel
  await ctx.reply('Hi, there!')
  mychannel = ctx.channel

# !bye 명령어 처리
@bot.command()
async def bye(ctx):
  await ctx.reply('See you later!')
  
@bot.command()
async def start(ctx):

    bot.loop.create_task(every_twenty_sec(ctx.channel))



#@bot.loop(seconds=15)
async def every_twenty_sec(mychannel):
    global last, rtx3060ti_last , rtx3070_last
    
    if(mychannel is None):
        print("Channel is None")
        return
    
    while True:
        print('running msg process...')
            
        index = iphone_get_last_notice()
        
        while(last <= index):
            text = get_one(last)
            
            if(text is not None):
                await mychannel.send(text)
            last+=1
            
            
        index_rtx = rtx_get_last_notice("rtx3060ti")
        
        while(rtx3060ti_last <= index_rtx):
            text = rtx_get_one(rtx3060ti_last, "rtx3060ti")
            
            if(text is not None):
                await mychannel.send(text)
            rtx3060ti_last += 1
            
            
        index_rtx3070 = rtx_get_last_notice("rtx3070")
        
        while(rtx3070_last <= index_rtx3070):
            text = rtx_get_one(rtx3070_last, "rtx3070")
            if(text is not None):
                await mychannel.send(text)
            rtx3070_last += 1
        
        await asyncio.sleep(10)        
    
    
def iphone_get_last_notice():
    cur.execute("SELECT num, text FROM iphone ORDER BY num DESC LIMIT 1")

    row = cur.fetchall()
    
    if(len(row) > 0):
        return int(row[0][0])
    return 0

def rtx_get_last_notice(gpu_name):
    cur.execute("SELECT num, text FROM " + gpu_name + " ORDER BY num DESC LIMIT 1")

    row = cur.fetchall()
    
    if(len(row) > 0):
        return int(row[0][0])
    return 0

def get_one(index_num):
    
    cur.execute("SELECT text FROM iphone WHERE num=" + str(index_num))
    row = cur.fetchall()
    
    if(len(row) > 0):
        return row[0][0]
    return None

def rtx_get_one(index_num, gpu_name):
    
    cur.execute("SELECT text FROM "+ gpu_name + " WHERE num=" + str(index_num))
    row = cur.fetchall()
    
    if(len(row) > 0):
        return row[0][0]
    return None
    
bot.run(TOKEN)