import os
import re
import discord
from discord.ext import commands
from datetime import datetime

client = commands.Bot(command_prefix='+', self_bot=True,
                      guild_subscription_options=discord.GuildSubscriptionOptions.off())


def sanitize_name(name):
    return re.sub(r'[<>:"/\\|?*]', '-', name)


@client.event
async def on_message(message: discord.Message):
    image_types = ["png", "jpeg", "gif", "jpg", "mp4", "mov", "webp"]

    if message.channel.id == CHANNEL_ID:
        # new directory for the attachments
        sanitized_channel_name = sanitize_name(message.channel.name)
        sanitized_guild_name = sanitize_name(message.guild.name)
        channel_dir = f'{sanitized_guild_name} - {sanitized_channel_name}/'
        os.makedirs(channel_dir, exist_ok=True)

        for attachment in message.attachments:
            if any(attachment.filename.lower().endswith(image) for image in image_types):

                await attachment.save(f'{channel_dir}{attachment.filename}')
                print(
                    f'Server: {message.guild.name} (ID: {message.guild.id}) | '
                    f'Channel: {message.channel.name} (ID: {message.channel.id}) | '
                    f'Attachment {attachment.filename} has been saved to directory > {channel_dir}')


async def download_attachments(GUILD_ID, CHANNEL_ID, start_date, end_date):
    guild = client.get_guild(GUILD_ID)
    if not guild:
        print(f'User is not a member of guild with ID {GUILD_ID}')
        return

    channel = guild.get_channel(CHANNEL_ID)
    if not channel:
        print(f'Channel with ID {CHANNEL_ID} not found')
        return

    async for message in channel.history(limit=None, after=start_date, before=end_date):
        await on_message(message)


async def userInfo():
    print('-' * 20)
    print('Logged in as')
    print(f'User: {client.user.name}')
    print(f'ID: {client.user.id}')
    print('-' * 20)


@client.event
async def on_ready():
    await userInfo()
    await download_attachments(GUILD_ID, CHANNEL_ID, START_DATE, END_DATE)

    os._exit(0)


def start_downloader(TOKEN_IN, GUILD_ID_IN, CHANNEL_ID_IN, START_DATE_IN, END_DATE_IN):
    global client, GUILD_ID, CHANNEL_ID, START_DATE, END_DATE
    TOKEN = TOKEN_IN
    GUILD_ID = GUILD_ID_IN
    CHANNEL_ID = CHANNEL_ID_IN
    START_DATE = datetime.strptime(START_DATE_IN, '%Y-%m-%d')
    END_DATE = datetime.strptime(END_DATE_IN, '%Y-%m-%d')

    client.run(TOKEN)


if __name__ == '__main__':
    # format: 'TOKEN HERE'
    TOKEN_IN = 'TOKEN HERE'

    # format: 123456789101112131
    GUILD_ID_IN = 138194444645040128
    CHANNEL_ID_IN = 1023685109242663043

    # format: 'YYYY-MM-DD'
    START_DATE_IN = '2023-04-01'
    END_DATE_IN = '2023-04-02'

    start_downloader(TOKEN_IN=TOKEN_IN, GUILD_ID_IN=GUILD_ID_IN,
                     CHANNEL_ID_IN=CHANNEL_ID_IN, START_DATE_IN=START_DATE_IN, END_DATE_IN=END_DATE_IN)
