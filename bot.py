import argparse
import datetime
import os.path
import logging

import discord
from discord.ext import commands

from settings import get_config, get_logger
from utils import steam


parser = argparse.ArgumentParser(description='Process arguments.')
parser.add_argument('--config_file', dest='config_file', default='./config/local.yaml', help='config file path')

PATH = parser.parse_args().config_file
CONFIG = get_config(PATH)
LOGGER = get_logger()

bot = commands.Bot(command_prefix='!')


@bot.event
async def on_error(event, *args, **kwargs):

    if event == 'on_message':
        LOGGER.info(f'Unhandled message: {args[0]}\n')
    else:
        raise


@bot.event
async def on_ready():

    LOGGER.info(f'[{datetime.datetime.now()}] {bot.user.name} connected')
    guild = discord.utils.get(bot.guilds, name='Уютный чатик')
    if guild:
        LOGGER.info(f'Guild: {guild.name}\nMembers online:')

        for member in guild.members:
            LOGGER.info(f'{member.name}')


@bot.command(name='echo', help='Checks if the bot is online')
async def echo(context):

    await context.send('Cozy Bot online')


@bot.command(name='list', help='Shows server list')
async def query_sync(context, no_of_servers: int = 10):

    data = await steam.get_server_list_with_players(LOGGER)

    text = 'Server > Map - Players - Privacy\n\n'
    # text += 'ʕノ•ᴥ•ʔノ ︵ ┻━┻'
    for server in data.get('data', []):
        text += (f'{server.get("server_name", "_server_")}\n'
                 f'{server.get("map", "_map_"):>30} '
                 f'{server.get("player_count", "_players_on_"):>2}/'
                 f'{server.get("max_players", "_players_max_"):} '
                 f'{"✔" if server.get("password_protected", 0) else ""}\n')

    text += f'\nPlayers online: {data.get("total_player_count", 0)}'

    await context.send(text)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    logging.info('Config file: %s' % PATH)
    logging.info('Starting bot...')

    bot.run(CONFIG['discord_token'])
