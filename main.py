import discord
from regear_functions import Spreadsheet

bot_token_file = open('DISCORD TOKEN.txt', 'r')  # TODO: change to _production
GUILD = 'SuSliK'  # TODO: change to Fax
bot_token = bot_token_file.readline()
client = discord.Client()
sh = Spreadsheet()


@client.event
async def on_ready():
    guild = discord.utils.find(lambda g: g.name == GUILD, client.guilds)
    print(
        f'{client.user} is connected to {guild.name} (id: {guild.id})')


@client.event
async def on_message(message):
    global sh
    username = message.author
    if message.author == client.user:
        return

    channel = message.channel

    if message.content.startswith('..init'):  # creates new spreadsheet
        if discord.utils.get(username.roles, name='Mechanic') is None:
            await message.add_reaction('❌')
            embed_msg = discord.Embed(
                title='**Error**',
                description='**..init** requires **Mechanic** role to run.',
                color=discord.Color.red()
            )
            await channel.send(embed=embed_msg)
        else:
            await message.add_reaction('⏲')
            sh = Spreadsheet()
            await message.add_reaction('✅')
            embed_msg = discord.Embed(
                title='**Success (click me)**',
                description='New spreadsheet was generated!',
                color=discord.Color.green(),
                url=sh.url()
            )
            await channel.send(embed=embed_msg)

    if message.content.startswith('..sort'):
        if discord.utils.get(username.roles, name='Mechanic') is None:
            await message.add_reaction('❌')
            embed_msg = discord.Embed(
                title='**Error**',
                description='**..sort** requires **Mechanic** role to run.',
                color=discord.Color.red()
            )
            await channel.send(embed=embed_msg)
        else:
            sh.sort()
            await message.add_reaction('✅')

    if message.content.startswith('..URL') or message.content.startswith('..url'):
        embed_msg = discord.Embed(
            title='**URL (click me)**',
            description='URL to a current spreadsheet.',
            color=discord.Color.green(),
            url=sh.url()
        )
        await channel.send(embed=embed_msg)

    if message.content.startswith('!'):
        await message.add_reaction('⏲')
        EventId = message.content[1:]
        try:
            sh.push(EventId)
            await message.add_reaction('✅')
        except UnboundLocalError:
            embed_msg = discord.Embed(
                title='**Error**',
                description='You need to **..init** first.\n'
                            '**..init** requires **Mechanic** role to run.',
                color=discord.Color.red()
            )
            await channel.send(embed=embed_msg)

    if message.content.startswith('+'):
        if discord.utils.get(username.roles, name='Mechanic') is None:
            await message.add_reaction('❌')
            embed_msg = discord.Embed(
                title='**Error**',
                description='**+** requires **Mechanic** role to run.',
                color=discord.Color.red()
            )
            await channel.send(embed=embed_msg)
        else:
            row_number = message.content.replace('+', '')
            row_number_list = row_number.split(' ')
            if row_number_list[0] == '1':
                await message.add_reaction('❌')
                embed_msg = discord.Embed(
                    title='**Error**',
                    description='You are trying to **tick** a title cell.',
                    color=discord.Color.red()
                )
                await channel.send(embed=embed_msg)
            else:
                sh.tick(row_number_list[0], row_number_list[1])
                await message.add_reaction('✅')

    if message.content.startswith('..help'):
        embed_msg = discord.Embed(
            title='Available commands:',
            description='**..help** - Shows this message.\n'
                        '\n'
                        '**..init** - Creates new spreadsheet.\n'
                        'Requires **Mechanic** role.\n'
                        '\n'
                        '**..sort** - Sorts spreadsheet.\n'
                        'Requires **Mechanic** role.\n'
                        '\n'
                        '**..url** or **..URL** - Sends URL to a current spreadsheet.\n'
                        '\n'
                        '**!EventId** - Pushes regear request to spreadsheet.\n'
                        '\n'
                        '**+ROW_NUM CHEST_NUM** - Ticks a row and writes assigned chest number\n',
            color=discord.Color.green()
        )
        embed_msg.set_image(url='https://yt3.ggpht.com/ooDmRtyMCL1W6SJyqsPRoJD6ag63CqYGD0FPMDmGhvvga4'
                                '6HrHgeCiBCvMxl-OpBkagBBYShfA=w640-fcrop64=1,32b75a57cd48a5a8-nd-c0xffffffff-rj-k-no')
        embed_msg.set_footer(text='OopsieDoopsie#0412')
        await channel.send(embed=embed_msg)

client.run(bot_token)
