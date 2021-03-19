import discord
import json
import asyncio
import re
from parse import get_title

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
	username = message.author
	if message.author == client.user:
		return

	channel = message.channel
	if message.content.startswith('..killbot_hello'):
		await channel.send('Hello!')

	if message.content.startswith('..killbot_init'):
		if discord.utils.get(username.roles, name='Mechanic') is None:
			await message.add_reaction('<:FPepe:808012844783370270>')
		else:
			await message.add_reaction('<:Godbless:808014107789754369>')
			while True:

				with open('lastevent.json', 'r') as events:
					print('first open')
					last_events_json = json.load(events)
					last_events1 = last_events_json['last_event']
					last_event1 = last_events1[0]
					last_event1_items = list(last_event1.items())

				await asyncio.sleep(20)

				with open('lastevent.json', 'r') as events:
					print('second open')
					last_events_json = json.load(events)
					last_events2 = last_events_json['last_event']
					last_event2 = last_events2[0]
					last_event2_items = list(last_event2.items())

				for i in range(len(last_event1_items)):
					try:
						if last_event2_items[i] != last_event1_items[i]:
							to_send = last_event2_items[i]
							regex_respond = re.findall(f"(?<=', ')\S+(?=')", str(to_send))
							try:
								str_regex_respond = regex_respond[0]
							except IndexError:
								pass
							else:
								title = get_title(str_regex_respond)
								embed = discord.Embed(
									title=title,
									color=discord.Color.dark_red())
								embed.add_field(name='EventId', value=str_regex_respond)
								await channel.send(embed=embed)
					except IndexError:
						pass

client.run(bot_token)
