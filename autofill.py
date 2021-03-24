import json
from json import JSONDecodeError

import requests

from regear_functions import Spreadsheet


def get_guildmember_list():
	respond = requests.get(
		'https://gameinfo.albiononline.com/api/gameinfo/guilds/6g1WhBpsQ_W2eldCMtuTrw/members')
	return respond


def get_last_death(playerId):
	respond = requests.get(
		f'https://gameinfo.albiononline.com/api/gameinfo/players/{playerId}/deaths')
	try:
		outp = respond.json()[0]['EventId']
	except IndexError:
		outp = None
	except JSONDecodeError:
		outp = None
	print(f'Last death : {outp}')
	return outp


def main_writer_json(outp_get_guildmember_list, SpreadsheetVariable):
	try:
		raw_json = outp_get_guildmember_list.json()
		hot_json = {k['Name']: k['Id'] for k in raw_json}
		events_json = {k: get_last_death(hot_json[k]) for k in hot_json.keys()}
	except JSONDecodeError:
		return
	print(f'events_json: {events_json}')

	with open('guild_members.json', 'w') as handler:
		json.dump(hot_json, handler, indent=4)

	with open('guild_events.json', 'r') as handler:
		old_events = json.load(handler)
	print(f'old_events: {old_events}')

	new_events = old_events

	for i in events_json:
		op = events_json[i]
		print(f'Processing {op}')
		try:
			if old_events[i] != events_json[i] and op is not None:
				print(f'{op} IS NOT IN OLD_EVENTS!!! APPENDING IT INTO SPREADSHEET!')
				try:
					SpreadsheetVariable.push(str(op))
				except TimeoutError:
					try:
						SpreadsheetVariable.push(str(op))
					except TimeoutError:
						SpreadsheetVariable.push(str(op))
				new_events[i] = op
				print(new_events)
		except KeyError:
			continue

	with open('guild_events.json', 'w') as handler:
		print('IN ENCLOSING GUILD_EVENTS_JSON')
		json.dump(new_events, handler, indent=4)


if __name__ == "__main__":

	outp_get_guildmember_list = get_guildmember_list()
	raw_json = outp_get_guildmember_list.json()
	hot_json = {k['Name']: k['Id'] for k in raw_json}
	events_json = {k: get_last_death(hot_json[k]) for k in hot_json.keys()}
	with open('guild_events.json', 'w') as handler:
		json.dump(events_json, handler, indent=4)

	spreadsheet = Spreadsheet()
	print(spreadsheet.url())
	while True:
		main_writer_json(get_guildmember_list(), spreadsheet)
