
import time
import discord
from discord.ext import tasks
from discord.ext.commands import Bot
from datetime import datetime
import pymysql


ip = "192.168.30.15"
port = 1883
passwd = open("passwd.txt", "r").readline()

conn = pymysql.connect(host='192.168.30.15', user='root', password=passwd, db='crwaling', charset='utf8')
cur = conn.cursor()


TOKEN = open("TOKEN.txt", "r").readline()
CHANNEL_ID = '945540335495426079'
mychannel = ''

intents = discord.Intents.default()

# !로 시작하면 명령어로 인식
bot = Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
  print(f'logged in as {bot.user}')

# !hello 명령어 처리
@bot.command()
async def hello(ctx):
  await ctx.reply('Hi, there!')
  await ctx.channel.send("hoho")
  
  global mychannel
  mychannel = ctx.channel

# !bye 명령어 처리
@bot.command()
async def bye(ctx):
  await ctx.reply('See you later!')
  
@bot.command()
async def start(ctx):
    print('running msg process...')
    last = 13
    rtx_last = 1
    
    while(True):
        
        index, nono = iphone_get_last_notice()
        
        while(last <= index):
            text = get_one(last)
            await ctx.channel.send(text)
            last+=1
            
        index_rtx, nono2 = rtx_get_last_notice()
        
        while(rtx_last <= index_rtx):
            text = rtx_get_one(rtx_last)
            await ctx.channel.send(text)
            rtx_last += 1
        
        time.sleep(20)
        
def insert_data(data):
    
    sql = "INSERT INTO iphone (text, date) VALUES('" + str(data) + "', '" + str(datetime.now()) +  "')"
    cur.execute(sql)
    conn.commit()
    
def iphone_get_last_notice():
    cur.execute("SELECT num, text FROM iphone ORDER BY num DESC LIMIT 1")

    row = cur.fetchall()
    
    if(len(row) > 0):
        return int(row[0][0]), row[0][1]
    return row, None

def rtx_get_last_notice():
    cur.execute("SELECT num, text FROM rtx3060ti ORDER BY num DESC LIMIT 1")

    row = cur.fetchall()
    
    if(len(row) > 0):
        return int(row[0][0]), row[0][1]
    return row, None

def get_one(index_num):
    
    cur.execute("SELECT text FROM iphone WHERE num=" + str(index_num))
    row = cur.fetchall()
    
    if(len(row) > 0):
        return row[0][0]
    return row

def rtx_get_one(index_num):
    
    cur.execute("SELECT text FROM rtx3060ti WHERE num=" + str(index_num))
    row = cur.fetchall()
    
    if(len(row) > 0):
        return row[0][0]
    return row
    
bot.run(TOKEN)