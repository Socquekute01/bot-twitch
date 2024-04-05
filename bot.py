import discord
import asyncio

# Thông tin cấu hình bot
TOKEN = ''
CHANNEL_ID =  # ID của kênh Discord bạn muốn theo dõi

twitch_links = []

intents = discord.Intents.default()
intents.message_content = True

intents.message_content = True 
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print('Bot đã sẵn sàng')

@client.event

async def on_guild_join(guild):
    channel = guild.system_channel
    if channel is not None:
        await channel.send('Hello ae trong kênh chat T715. Nay làm việc hết mình nhé ae ^^')

        command_info = """
        **Các lệnh và chức năng của tui nè <3 :**

        - `bot --ls`: Xem danh sách các liên kết Twitch đã được thêm.
        - `bot --complete`: Đánh dấu người dùng đầu tiên trong danh sách Twitch đã hoàn thành.
        - `bot --done`: Rời khỏi server Discord.

        """
        await channel.send(command_info)

@client.event
async def on_message(message):
    if message.author.bot or message.channel.id != CHANNEL_ID:
        return
    if 'https://www.twitch.tv/' in message.content:
        start_index = message.content.find('https://www.twitch.tv/')
        twitch_link = message.content[start_index:]
        if twitch_link not in twitch_links:
            twitch_links.append(twitch_link)
            await message.channel.send(f'Đã thêm liên kết Twitch: {twitch_link}')
    
    if message.content == 'bot --command':
        command_info = """
        **Các lệnh và chức năng:**

        - `bot --ls`: Xem danh sách các liên kết Twitch đã được thêm.
        - `bot --done`: Rời khỏi server Discord.
        - `bot --complete`: Đánh dấu người dùng đầu tiên trong danh sách Twitch đã hoàn thành.

        """
        await message.channel.send(command_info)
    
    if message.content == 'bot --ls':
        if twitch_links:
            links_message = "\n".join(twitch_links)
            await message.channel.send('Danh sách liên kết Twitch:\n' + links_message)
        else:
            await message.channel.send('Không có liên kết Twitch nào trong danh sách.')

    if message.content == 'bot --done':
        await message.channel.send('Tạm biệt ae! Sớm gặp lại nha!')
        await client.close()

    if message.content.startswith('bot --complete'):
        if len(twitch_links) > 0:
            removed_link = twitch_links.pop(0)
            await message.channel.send(f'Người dùng {removed_link} đã live xong')
        else:
            await message.channel.send('Danh sách người dùng đã trống.')

@client.event
async def on_guild_remove(guild):
    channel = guild.system_channel
    if channel is not None:
        await channel.send('Ae trong kênh ngủ ngon hẹn mai gặp lại nhé <3')

client.run(TOKEN)
