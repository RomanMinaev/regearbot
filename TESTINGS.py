import requests
import re
from bs4 import BeautifulSoup
import json


respond1 = ('TheRealRaquis', '')
respond2 = ('TheRealRaquis', '204533097')
responds = [respond1, respond2]

for respond in responds:
	regex_respond = re.findall(f"(?<=', ')\S+(?=')", str(respond))
	try:
		str_regex_respond = regex_respond[0]
	except IndexError:
		pass
	else:
		print(str_regex_respond)
		while True:
			try:
				html = requests.get(f'https://www.albiononline2d.com/en/scoreboard/events/{str_regex_respond}', timeout=20)
			except RuntimeError:
				continue
			break
		bs = BeautifulSoup(html.text, 'html.parser')
		bs_h1 = bs.find_all('h1', {'class': 'page-title'}, '#search string')
		title = re.findall(f'(?<=>).+(?=<)', str(bs_h1))
		print(title)
