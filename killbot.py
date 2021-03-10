import discord
import json
import time

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
	if message.content.startswith('..hello'):
		await channel.send('Hello!')

	if message.content.startswith('..init'):
		if discord.utils.get(username.roles, name='Mechanic') is None:
			await message.add_reaction('<:FPepe:808012844783370270>')
		else:
			await message.add_reaction('<:Godbless:808014107789754369>')
			while True:
				with open('lastevent.json', '') as events:
					last_events_json = json.load(events)
					last_events1 = last_events_json['last_event']
				time.sleep(30)
				with open('lastevent.json', 'r') as events:
					last_events_json = json.load(events)
					last_events2 = last_events_json['last_event']

				for i in range(len(last_events1)):
					if last_events2[i] != last_events1[i]:
						await channel.send(f'{last_events2[i]}')


client.run(bot_token)