import discord
from parse import GetGear
from spreadsheet import FaxRegear
import keep_alive
from zvzbuilddict import ARMOR_list
from zvzbuilddict import H_list
from parse import itemlist_gear_check

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
                try:
                    gear = GetGear(ID.replace('`', ''))
                except IndexError:
                    await message.add_reaction('❌')
                else:
                    if gear.get_ip() < 1300:
                        await message.add_reaction('😂')
                    else:
                        gear_check = itemlist_gear_check(gear)
                        if gear_check[1] in ARMOR_list and gear_check[0] in H_list:
                            if __name__ == '__main__':
                                faxregear.push(gear.push_package(), gear.get_UTC())
                            if gear_check[1] not in ARMOR_list:
                                await message.add_reaction('😐')
                            if gear_check[0] not in H_list:
                                await message.add_reaction('😡')  # 😂

        else:
            ID = message.content
            try:
                gear = GetGear(ID.replace('`', ''))
            except IndexError:
                await message.add_reaction('❌')
            else:
                if gear.get_ip() < 1300:
                    await message.add_reaction('😂')
                else:
                    gear_check = itemlist_gear_check(gear)
                    if gear_check[1] in ARMOR_list and gear_check[0] in H_list:
                        if __name__ == '__main__':
                            faxregear.push(gear.push_package(), gear.get_UTC())
                            await message.add_reaction('✅')
                    if gear_check[1] not in ARMOR_list:
                        await message.add_reaction('😐')
                    if gear_check[0] not in H_list:
                        await message.add_reaction('😡')

client.run(bot_token)
