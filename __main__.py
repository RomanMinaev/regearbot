import discord
from parse import GetGear
from spreadsheet import FaxRegear
from multiprocessing import Process
import keep_alive

faxregear = FaxRegear()

bot_token_file = open('DISCORD TOKEN.txt', 'r')
GUILD = 'SuSliK'
bot_token = bot_token_file.readline()
client = discord.Client()


@client.event
async def on_ready():
    guild = discord.utils.find(lambda g: g.name == GUILD, client.guilds)
    print(
        f'{client.user} is connected to {guild.name} (id: {guild.id})')

keep_alive.keep_alive()


@client.event
async def on_message(message):
    global faxregear
    username = message.author
    if message.author == client.user:
        return

    channel = message.channel
    if message.content.startswith('..hello'):
        await channel.send('Hello!')

    if message.content.startswith('..URL'):
        await channel.send(faxregear.get_url())

    if message.content.startswith('..init'):
        if discord.utils.get(username.roles, name='Mechanic') is None:
            await message.add_reaction('❌')
        else:
            faxregear = FaxRegear()
            await message.add_reaction('✅')

    if message.content.startswith('`'):
        await message.add_reaction('🤔')
        if ',' in message.content:
            ID_list = message.content.split(',')
            for ID in ID_list:
                gear = GetGear(ID.replace('`', ''))
                if __name__ == '__main__':
                    try:
                        action_process = Process(target=faxregear.push(gear.push_package(), gear.get_UTC()))
                        action_process.start()
                        action_process.join(timeout=10)
                        action_process.terminate()
                    except IndexError:
                        await message.add_reaction('❌')
                    else:
                        await message.add_reaction('✅')
        else:
            ID = message.content
            gear = GetGear(ID.replace('`', ''))
            if __name__ == '__main__':
                try:
                    action_process = Process(target=faxregear.push(gear.push_package(), gear.get_UTC()))
                    action_process.start()
                    action_process.join(timeout=10)
                    action_process.terminate()
                except IndexError:
                    await message.add_reaction('❌')
                else:
                    await message.add_reaction('✅')


client.run(bot_token)
