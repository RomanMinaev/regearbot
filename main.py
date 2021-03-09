import discord
from parse import GetGear
from spreadsheet import FaxRegear
from zvzbuilddict import ARMOR_list
from zvzbuilddict import H_list
from parse import itemlist_gear_check
from help_msg import help_msg

faxregear = FaxRegear()

bot_token_file = open('DISCORD TOKEN_production.txt', 'r')  # TODO: change to _production
GUILD = 'Fax'  # TODO: change to Fax
bot_token = bot_token_file.readline()
client = discord.Client()


@client.event
async def on_ready():
    guild = discord.utils.find(lambda g: g.name == GUILD, client.guilds)
    print(
        f'{client.user} is connected to {guild.name} (id: {guild.id})')


@client.event
async def on_message(message):
    global faxregear
    username = message.author
    if message.author == client.user:
        return

    channel = message.channel
    if message.content.startswith('..hello'):
        await channel.send('Hello!')

    if message.content.startswith('..help'):
        await channel.send(help_msg)

    if message.content.startswith('..URL'):
        await channel.send(faxregear.get_url())

    if message.content.startswith('..init'):
        if discord.utils.get(username.roles, name='Mechanic') is None:
            await message.add_reaction('<:FPepe:808012844783370270>')
        else:
            faxregear = FaxRegear()
            await message.add_reaction('<:Godbless:808014107789754369>')

    if message.content.startswith('!'):
        await message.add_reaction('<:Hmm:808011754029318225>')
        if ',' in message.content:
            ID_list = message.content.split(',')
            for ID in ID_list:
                try:
                    gear = GetGear(ID.replace('!', ''))
                except IndexError:
                    await message.add_reaction('<:FPepe:808012844783370270>')
                else:
                    if gear.get_ip() < 1300:
                        await message.add_reaction('<:Yikes:808013096215511084>')
                    else:
                        gear_check = itemlist_gear_check(gear)
                        if True:  # gear_check[1] in ARMOR_list and gear_check[0] in H_list:
                            if __name__ == '__main__':
                                faxregear.push(gear.push_package(), gear.get_UTC(), gear.get_ip(), f'=HYPERLINK("gear.get_link()","AO2D")')
                                await message.add_reaction('<:Godbless:808014107789754369>')
                            if gear_check[1] not in ARMOR_list:
                                await message.add_reaction('<:Nope:816695559653818390>')
                            if gear_check[0] not in H_list:
                                await message.add_reaction('<:Sayad:808011258006863903>')  # 😂

        else:
            ID = message.content
            try:
                gear = GetGear(ID.replace('!', ''))
            except IndexError:
                await message.add_reaction('<:FPepe:808012844783370270>')
            else:
                if gear.get_ip() < 1300:
                    await message.add_reaction('<:Yikes:808013096215511084>')
                else:
                    gear_check = itemlist_gear_check(gear)
                    if True:  # gear_check[1] in ARMOR_list and gear_check[0] in H_list:
                        if __name__ == '__main__':
                            faxregear.push(gear.push_package(), gear.get_UTC(), f'gear.get_ip() IP', f'=HYPERLINK("gear.get_link()","AO2D")')
                            await message.add_reaction('<:Godbless:808014107789754369>')
                    if gear_check[1] not in ARMOR_list:
                        await message.add_reaction('<:Nope:816695559653818390>')
                    if gear_check[0] not in H_list:
                        await message.add_reaction('<:Sayad:808011258006863903>')

client.run(bot_token)
