import os
import re
import time
import discord
from discord.ext import commands
from datetime import datetime
from dotenv import load_dotenv


class DiscordImageDownloader():
    def __init__(self):
        self.client = commands.Bot(command_prefix='+', self_bot=True,
                                   guild_subscription_options=discord.GuildSubscriptionOptions.off())
        self.client.event(self.on_ready)
        self.client.event(self.on_message)
        self.count = 0

    def sanitize_name(self, name):
        return re.sub(r'[<>:"/\\|?*]', '-', name)

    async def on_message(self, message: discord.Message):
        image_types = ["png", "jpeg", "gif", "jpg", "mp4", "mov", "webp"]

        if message.channel.id == CHANNEL_ID:
            # new directory for the attachments
            sanitized_channel_name = self.sanitize_name(message.channel.name)
            sanitized_guild_name = self.sanitize_name(message.guild.name)
            channel_dir = f'{sanitized_guild_name} - {sanitized_channel_name}'
            os.makedirs(channel_dir, exist_ok=True)

            for attachment in message.attachments:
                if any(attachment.filename.lower().endswith(image) for image in image_types):
                    # check if the file already exists and generate a new name with the Unix time if needed
                    new_filename = attachment.filename
                    while os.path.exists(f'{channel_dir}/{new_filename}'):
                        file_name, file_extension = os.path.splitext(
                            attachment.filename)
                        unix_time = int(time.time_ns())
                        new_filename = f'{file_name}_{unix_time}{file_extension}'

                    await attachment.save(f'{channel_dir}/{new_filename}')
                    self.count += 1
                    print(
                        f'Server: {message.guild.name} (ID: {message.guild.id}) | '
                        f'Channel: {message.channel.name} (ID: {message.channel.id}) | '
                        f'Attachment {new_filename} has been saved to directory > {channel_dir}')

    async def download_attachments(self, GUILD_ID, CHANNEL_ID, start_date, end_date):
        guild = self.client.get_guild(GUILD_ID)
        if not guild:
            print(f'User is not a member of guild with ID {GUILD_ID}')
            return

        channel = guild.get_channel(CHANNEL_ID)
        if not channel:
            print(f'Channel with ID {CHANNEL_ID} not found')
            return

        async for message in channel.history(limit=None, after=start_date, before=end_date):
            await self.on_message(message)

        print(f"Downloaded {self.count} images")

    async def userInfo(self):
        print('-' * 25)
        print('Logged in as')
        print(f'User: {self.client.user.name}')
        print(f'ID: {self.client.user.id}')
        print('-' * 25)

    async def on_ready(self):
        await self.userInfo()
        await self.download_attachments(GUILD_ID, CHANNEL_ID, START_DATE, END_DATE)

        os._exit(0)

    def start_downloader(self, TOKEN_IN, GUILD_ID_IN, CHANNEL_ID_IN, START_DATE_IN, END_DATE_IN):
        global client, GUILD_ID, CHANNEL_ID, START_DATE, END_DATE
        TOKEN = TOKEN_IN
        GUILD_ID = GUILD_ID_IN
        CHANNEL_ID = CHANNEL_ID_IN
        START_DATE = datetime.strptime(START_DATE_IN, '%Y-%m-%d')
        END_DATE = datetime.strptime(END_DATE_IN, '%Y-%m-%d')

        self.client.run(TOKEN)


if __name__ == '__main__':
    load_dotenv()
    TOKEN_IN = os.getenv('TOKEN_IN')
    GUILD_ID_IN = int(os.getenv('GUILD_ID_IN'))
    CHANNEL_ID_IN = int(os.getenv('CHANNEL_ID_IN'))
    START_DATE_IN = os.getenv('START_DATE_IN')
    END_DATE_IN = os.getenv('END_DATE_IN')

    DiscordImageDownloader().start_downloader(TOKEN_IN=TOKEN_IN, GUILD_ID_IN=GUILD_ID_IN,
                                              CHANNEL_ID_IN=CHANNEL_ID_IN, START_DATE_IN=START_DATE_IN, END_DATE_IN=END_DATE_IN)
