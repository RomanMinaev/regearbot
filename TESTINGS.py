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