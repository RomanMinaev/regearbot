import requests
import re
from bs4 import BeautifulSoup
import json
from requests import ReadTimeout


class GetGear:
	def __init__(self, kill_id):
		self.kill_id = kill_id
		self.item_urls = []
		self.item_urls_killer = []
		self.LINK = f'https://www.albiononline2d.com/en/scoreboard/events/{kill_id}'
		html = requests.get(self.LINK, timeout=20)
		self.bs = BeautifulSoup(html.text, 'html.parser')
		bs_div = self.bs.find_all('div', {'class': 'character-slots'}, '#search string')
		killer_tag = bs_div[0]
		victim_tag = bs_div[1]
		for i in victim_tag:
			obj = re.findall(r'src=\S+', str(i))
			obj_str = obj[0]
			self.item_urls.append(re.sub('(?<=&)a\S+;', '', obj_str[5:-1]))
		for i in killer_tag:
			obj = re.findall(r'src=\S+', str(i))
			obj_str = obj[0]
			self.item_urls_killer.append(re.sub('(?<=&)a\S+;', '', obj_str[5:-1]))

	def title(self):
		return self.bs.title.string[0:-27]

	def itemlist(self):
		return self.item_urls

	def itemlist_regearable(self):
		regearables = ['HEAD', '1H', '2H', 'MAIN', 'OFF', 'ARMOR', 'SHOES']
		regearables_urls = []
		for i in self.item_urls:
			if any(map(i.__contains__, regearables)):
				regearables_urls.append(i)
		return regearables_urls

	def itemlist_killer(self):
		return self.item_urls_killer

	def ign(self):
		return self.bs.title.string.split()[2]

	def ign_killer(self):
		return self.bs.title.string.split()[0]

	def push_package(self):
		package = [self.bs.title.string.split()[2]]
		regearables = ['HEAD', '1H', '2H', 'MAIN', 'OFF', 'ARMOR', 'SHOES']
		regearables_urls = []
		for i in self.item_urls:
			if any(map(i.__contains__, regearables)):
				z = f'=IMAGE("{i}")'
				regearables_urls.append(z)

		for i in regearables_urls:
			package.append(i)
		return package

	def get_UTC(self):
		time_find = self.bs.find_all('p')
		time_chunk = str(time_find[-2])
		temp_list = time_chunk.split(',')
		time_smaller_chunk = temp_list[-1]
		UTC_time = time_smaller_chunk[0:-4]
		return UTC_time

	def get_ip(self):
		ip_find = self.bs.find_all('h3')
		content_ip = ip_find[2]
		dirty_ip_list = re.findall(r'>\S+<', str(content_ip))
		dirty_ip = dirty_ip_list[0]
		clean_ip = dirty_ip[1:-1]
		return int(clean_ip)

	def get_link(self):
		return self.LINK


def itemlist_gear_check(getgear):
	reglist = getgear.itemlist_regearable()
	gear_list = []
	for i in reglist:
		out = i.split('/')
		item = out[-1]
		split_item = item.split('.')
		itemname = split_item[0]
		if '@' in itemname:
			itemname = itemname[0:-2]
		b_itemname = itemname[3:]
		gear_list.append(b_itemname)
	gear_check_list = []
	for i in gear_list:
		if 'ARMOR_' in i:
			gear_check_list.append(i)
		if '2H_' in i:
			gear_check_list.append(i)
		if 'MAIN_' in i:
			gear_check_list.append(i)
	return gear_check_list


class GetGuildmembers:
	def __init__(self):
		html = requests.get(
			'https://gameinfo.albiononline.com/api/gameinfo/guilds/6g1WhBpsQ_W2eldCMtuTrw/members')  # guild Fax
		bs = BeautifulSoup(html.text, 'html.parser')
		names = re.findall(r'(?<="Name":")\S+?(?=","Id)', str(bs))
		IDs = re.findall(r'(?<="Id":")\S+?(?=","Gui)', str(bs))
		number_of_players = len(names)
		player_dict = {}
		for number in range(number_of_players):
			player_dict[names[number]] = IDs[number]

		data = {'players': [player_dict]}
		with open('guildmembers.json', 'w') as dump:
			json.dump(data, dump, indent=4)


class GetLastEvents:
	def __init__(self):
		with open('guildmembers.json', 'r') as data:
			datapack2 = json.load(data)
			players_data_dict = datapack2['players']
			players_data = players_data_dict[0]

		players_list = list(dict.keys(players_data))
		players_ID_list = list(dict.values(players_data))

		EventId_list = []
		last_EventId_list = []
		for number in range(len(players_list)):
			html = requests.get(
				f'https://gameinfo.albiononline.com/api/gameinfo/players/{players_ID_list[number]}/deaths')  # guild Fax
			bs = BeautifulSoup(html.text, 'html.parser')
			event_ID = re.findall(r'(?<="EventId":)\S+?(?=,"Time)', str(bs))
			try:
				last_event_ID = event_ID[0]
			except IndexError:
				continue
			EventId_list.append(event_ID)
			last_EventId_list.append(last_event_ID)
		event_dict = {}
		last_event_dict = {}
		for number2 in range(len(players_list)):
			try:
				event_dict[players_list[number2]] = EventId_list[number2]
			except IndexError:
				continue
			if last_EventId_list[number2] != '':
				try:
					last_event_dict[players_list[number2]] = last_EventId_list[number2]
				except IndexError:
					continue
		data2 = {f'last_event': [last_event_dict]}
		with open('lastevent.json', 'w') as dump:
			json.dump(data2, dump, indent=4)


def get_title(EventId):
	while True:
		try:
			html = requests.get(f'https://www.albiononline2d.com/en/scoreboard/events/{EventId}', timeout=20)
		except RuntimeError:
			continue
		except ReadTimeout:
			continue
		break
	bs = BeautifulSoup(html.text, 'html.parser')
	bs_h1 = bs.find_all('h1', {'class': 'page-title'}, '#search string')
	title = re.findall(f'(?<=>).+(?=<)', str(bs_h1))
	return title[0]
