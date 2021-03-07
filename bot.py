import discord
from multiprocessing import Process
from parse import GetGear
from spreadsheet import FaxRegear
from discord.ext import commands

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


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    channel = message.channel
    if message.content.startswith('..hello'):
        await channel.send('Hello!')

    if message.content.startswith('..relog'):
        @commands.is_owner()
        async def restartbot(ctx):
            await ctx.bot.logout()
            await client.login(bot_token, bot=True)

    if message.content.startswith('..URL'):
        await channel.send(faxregear.get_url())

    if message.content.startswith('~'):
        await message.add_reaction('🤔')
        ID = message.content
        gear = GetGear(ID.replace('~', ''))
        if __name__ == '__main__':
            try:
                action_process = Process(target=faxregear.push(gear.push_package()))
                action_process.start()
                action_process.join(timeout=10)
                action_process.terminate()
            except IndexError:
                await message.add_reaction('❌')
            else:
                await message.add_reaction('✅')

client.run(bot_token)
