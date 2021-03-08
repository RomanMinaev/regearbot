import requests
import re
from bs4 import BeautifulSoup


class GetGear:
	def __init__(self, kill_id):
		self.kill_id = kill_id
		self.item_urls = []
		self.item_urls_killer = []
		html = requests.get(f'https://www.albiononline2d.com/en/scoreboard/events/{kill_id}')
		self.bs = BeautifulSoup(html.text, 'html.parser')
		bs_div = self.bs.find_all('div', {'class': 'character-slots'}, '#search string')
		killer_tag = bs_div[0]
		victim_tag = bs_div[1]
		for i in victim_tag:
			obj = re.findall(r'src=\S+', str(i))
			obj_str = obj[0]
			self.item_urls.append(obj_str[5:-1])
		for i in killer_tag:
			obj = re.findall(r'src=\S+', str(i))
			obj_str = obj[0]
			self.item_urls_killer.append(obj_str[5:-1])

	def get_bs(self):
		time_find = self.bs.find_all('p')
		time_chunk = str(time_find[-2])
		temp_list = time_chunk.split(',')
		time_smaller_chunk = temp_list[1]
		UTC_time = time_smaller_chunk[0:-4]

		return UTC_time


getgear = GetGear('201833197')
print(getgear.get_bs())
