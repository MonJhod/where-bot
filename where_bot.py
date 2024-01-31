# Permission int 18136036801600

import discord
from discord.ext import commands
import logging
from IPChecker import IPChecker

global channel
channel = None
global debug
debug = False

logger = logging.getLogger('discord.bot')
logger.setLevel(logging.DEBUG)  # Set to logging.INFO to reduce verbosity
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

intents = discord.Intents.default()
intents.messages = True        # Enable messages intents
intents.message_content = True # Enable message content intent (if using Discord API v1.5+)
intents.guilds = True    # If you're using guild-specific features

bot = commands.Bot(command_prefix='$', intents=intents)

def ip_changed(new_ip):
    global channel
    if channel:
        bot.loop.create_task(channel.send(f"Server IP changed: {new_ip}"))
    else:
        logger.error("ip_changed ==> Error: No channel set")
        
def ip_same(ip):
    global channel
    if debug:
        if channel:
            bot.loop.create_task(channel.send(f"Same IP: {ip}"))
        else:
            logger.error("ip_changed ==> Error: No channel set")
            
ip_checker = IPChecker().set_on_ip_change(ip_changed).set_on_ip_same(ip_same)

@bot.command(name='debug')
async def debug_toggle(ctx):
    global debug
    logger.info(f'Debug command received  (Server: {ctx.guild.name}, Channel: {ctx.channel.name})')
    debug = not debug
    if debug:
        await ctx.send("Debug enabled!")
    else:
        await ctx.send("Debug disabled!")

@bot.command(name='port')
async def port(ctx, param=None):
    logger.info(f'Port command received with parameter: {param}  (Server: {ctx.guild.name}, Channel: {ctx.channel.name})')
    ip_checker.set_port(param)
    await ctx.send(f'Port set: {param}')

@bot.command(name='interval')
async def interval(ctx, param=None):
    logger.info(f'Interval command received with parameter: {param}  (Server: {ctx.guild.name}, Channel: {ctx.channel.name})')
    try:
        ip_checker.set_interval(int(param))
        await ctx.send(f'Interval set: {param}s')
    except:
        logger.error(f'interval ==> Error: Interval could not be set  (interval: {param})')
    
@bot.command(name='start')
async def start(ctx):
    logger.info(f'Start command received  (Server: {ctx.guild.name}, Channel: {ctx.channel.name})')
    if channel is None:
        await ctx.send("Error: please set channel by typing $here in channel.")
    elif ip_checker.port is None:
        await ctx.send("Error: please set port with $port <port>.")
    else:
        ip_checker.start()
        await ctx.send('Counter started!')

@bot.command(name='stop')
async def stop(ctx):
    logger.info(f'Stop command received  (Server: {ctx.guild.name}, Channel: {ctx.channel.name})')
    ip_checker.stop()
    await ctx.send('Counter Stopped!')

@bot.command(name='here')
async def here(ctx):
    global channel
    logger.info(f'Here command received  (Server: {ctx.guild.name}, Channel: {ctx.channel.name})')
    channel = ctx.channel
    await ctx.send(f'Channel set: {channel.name}')

# Your bot token
bot.run('MTIwMjA2NDI2MjI2MDg1MDczOA.GXA3jq.5LGPYIextzZeLUC_o1JewuOtWvqOaeo5BY7Zcc')