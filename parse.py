import requests
import re
from bs4 import BeautifulSoup


class GetGear:
	def __init__(self, kill_id):
		self.kill_id = kill_id
		self.item_urls = []
		self.item_urls_killer = []
		self.LINK = f'https://www.albiononline2d.com/en/scoreboard/events/{kill_id}'
		html = requests.get(self.LINK, timeout=10)
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
