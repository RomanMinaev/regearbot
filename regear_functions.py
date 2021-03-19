from requests import get
import json
import math
from googleapiclient import discovery
from oauth2client.service_account import ServiceAccountCredentials


def get_kill(eventId):
	"""
	Parses gameinfo.albiononline.com for an event and creates items pictures URLs. Uses JSONs.
	:param eventId: (ex. https://www.albiononline2d.com/en/scoreboard/events/208053435 <- those numbers)
	:return: URLs from JSON
	"""
	link = \
		'https://gameinfo.albiononline.com/api/gameinfo/events/' + eventId
	html = get(link, timeout=10)

	with open('out.json', 'w') as data:
		json.dump(html.json(), data, indent=4)
	with open('out.json', 'r') as data:
		info = json.load(data)

	equipment = info["Victim"]["Equipment"]
	equip_dict = dict()
	equip_dict['EventId'] = str(info['EventId'])
	equip_dict['BattleId'] = str(info['BattleId'])
	equip_dict['Time'] = (info['TimeStamp'].split('.')[0]).replace('T', '\n')
	equip_dict['Victim'] = info['Victim']['Name']
	equip_dict['Victim_IP'] = math.floor(info['Victim']['AverageItemPower'])
	equip_dict['Killer'] = info['Killer']['Name']
	equip_dict['Killer_IP'] = math.floor(info['Killer']['AverageItemPower'])
	for i in equipment.keys():
		try:
			equip_dict[i] = \
				f"https://render.albiononline.com/v1/item/{equipment[i]['Type']}.png?count=1&quality={equipment[i]['Quality']}"
		except TypeError:
			try:
				equip_dict[i] = \
					f"https://render.albiononline.com/v1/item/{equipment[i]['Type']}.png?count=1"
			except TypeError:
				equip_dict[i] = None

	with open('out_URLs.json', 'w') as data:
		json.dump(equip_dict, data, indent=4)

	return equip_dict


class Spreadsheet:
	"""
	Class for working with regear spreadsheet.
	__init__ creates new spreadsheet.
	"""
	def __init__(self):
		self.count = 2
		CREDENTIALS_FILE = 'fax-regear-c42cdf23fca5.json'

		credentials = ServiceAccountCredentials.from_json_keyfile_name(
			CREDENTIALS_FILE, [
				'https://www.googleapis.com/auth'
				'/spreadsheets',
				'https://www.googleapis.com/auth'
				'/drive'])

		self.service = discovery.build('sheets', 'v4', credentials=credentials)
		self.spreadsheet = self.service.spreadsheets().create(
			body={
				'properties': {
					'title': 'FAX Regear',
					'locale': 'en_US'
				},
				'sheets': [
					{
						'properties': {
							'sheetType': 'GRID',
							'sheetId': 0,
							'title': 'God Bless',
							'gridProperties': {
								'hideGridlines': False,
								'rowCount': 1000,
								'columnCount': 13
							}
						}
					}
				]
			}).execute()
		driveService = discovery.build('drive', 'v3', credentials=credentials)
		driveService.permissions().create(
			fileId=self.spreadsheet['spreadsheetId'],
			body={'type': 'anyone', 'role': 'reader'},
			fields='id'
		).execute()

		self.service.spreadsheets().batchUpdate(  # ign column
			spreadsheetId=self.spreadsheet['spreadsheetId'],
			body={
				'requests': {
					'updateDimensionProperties': {
						'range': {
							'sheetId': 0,
							'dimension': 'COLUMNS',
							'startIndex': 0,
							'endIndex': 1
						},
						'properties': {
							'pixelSize': 320
						},
						'fields': 'pixelSize'
					}
				}
			}
		).execute()

		self.service.spreadsheets().batchUpdate(  # items columns
			spreadsheetId=self.spreadsheet['spreadsheetId'],
			body={
				'requests': {
					'updateDimensionProperties': {
						'range': {
							'sheetId': 0,
							'dimension': 'COLUMNS',
							'startIndex': 1,
							'endIndex': 8
						},
						'properties': {
							'pixelSize': 128
						},
						'fields': 'pixelSize'
					}
				}
			}
		).execute()

		self.service.spreadsheets().batchUpdate(  # checkmark and chest number columns
			spreadsheetId=self.spreadsheet['spreadsheetId'],
			body={
				'requests': {
					'updateDimensionProperties': {
						'range': {
							'sheetId': 0,
							'dimension': 'COLUMNS',
							'startIndex': 11,
							'endIndex': 14
						},
						'properties': {
							'pixelSize': 128
						},
						'fields': 'pixelSize'
					}
				}
			}
		).execute()

		self.service.spreadsheets().batchUpdate(  # rows
			spreadsheetId=self.spreadsheet['spreadsheetId'],
			body={
				'requests': {
					'updateDimensionProperties': {
						'range': {
							'sheetId': 0,
							'dimension': 'ROWS',
							'startIndex': 0,
							'endIndex': 1
						},
						'properties': {
							'pixelSize': 30
						},
						'fields': 'pixelSize'
					}
				}
			}
		).execute()

		self.service.spreadsheets().batchUpdate(  # rows
			spreadsheetId=self.spreadsheet['spreadsheetId'],
			body={
				'requests': {
					'updateDimensionProperties': {
						'range': {
							'sheetId': 0,
							'dimension': 'ROWS',
							'startIndex': 1,
							'endIndex': 1000
						},
						'properties': {
							'pixelSize': 128
						},
						'fields': 'pixelSize'
					}
				}
			}
		).execute()

		self.service.spreadsheets().values().batchUpdate(  # titles
			spreadsheetId=self.spreadsheet['spreadsheetId'],
			body={
				"valueInputOption": 'USER_ENTERED',
				"data": [
					{
						"range": 'A1:A1',
						"majorDimension": "ROWS",
						"values": [['IGN']]
					},
					{
						"range": 'B1:B1',
						"majorDimension": "ROWS",
						"values": [['Main Hand']]
					},
					{
						"range": 'C1:C1',
						"majorDimension": "ROWS",
						"values": [['Off Hand']]
					},
					{
						"range": 'D1:D1',
						"majorDimension": "ROWS",
						"values": [['Head']]
					},
					{
						"range": 'E1:E1',
						"majorDimension": "ROWS",
						"values": [['Armor']]
					},
					{
						"range": 'F1:F1',
						"majorDimension": "ROWS",
						"values": [['Shoes']]
					},
					{
						"range": 'G1:G1',
						"majorDimension": "ROWS",
						"values": [['Cape']]
					},
					{
						"range": 'H1:H1',
						"majorDimension": "ROWS",
						"values": [['Mount']]
					},
					{
						"range": 'I1:I1',
						"majorDimension": "ROWS",
						"values": [['Avg IP']]
					},
					{
						"range": 'J1:J1',
						"majorDimension": "ROWS",
						"values": [['Time']]
					},
					{
						"range": 'K1:K1',
						"majorDimension": "ROWS",
						"values": [['Link']]
					},
					{
						"range": 'L1:L1',
						"majorDimension": "ROWS",
						"values": [['Status']]
					},
					{
						"range": 'M1:M1',
						"majorDimension": "ROWS",
						"values": [['Chest']]
					}
				]
			}
		).execute()

		self.service.spreadsheets().batchUpdate(  # titles font
			spreadsheetId=self.spreadsheet['spreadsheetId'],
			body={
				"requests":
					[
						{
							"repeatCell":
								{
									"cell":
										{
											"userEnteredFormat":
												{
													"horizontalAlignment": 'CENTER',
													"verticalAlignment": 'MIDDLE',
													"textFormat":
														{
															"bold": True,
															"fontSize": 14
														}
												}
										},
									"range":
										{
											"sheetId": 0,
											"startRowIndex": 0,
											"endRowIndex": 1,
											"startColumnIndex": 0,
											"endColumnIndex": 14
										},
									"fields": "userEnteredFormat"
								},
						}
					]
			}
		).execute()

		self.service.spreadsheets().batchUpdate(  # IGN font
			spreadsheetId=self.spreadsheet['spreadsheetId'],
			body={
				"requests":
					[
						{
							"repeatCell":
								{
									"cell":
										{
											"userEnteredFormat":
												{
													"horizontalAlignment": 'CENTER',
													"verticalAlignment": 'MIDDLE',
													"textFormat":
														{
															"bold": True,
															"fontSize": 18
														}
												}
										},
									"range":
										{
											"sheetId": 0,
											"startRowIndex": 1,
											"endRowIndex": 1000,
											"startColumnIndex": 0,
											"endColumnIndex": 1
										},
									"fields": "userEnteredFormat"
								},
						}
					]
			}
		).execute()

		self.service.spreadsheets().batchUpdate(  # IP, Time, Link font
			spreadsheetId=self.spreadsheet['spreadsheetId'],
			body={
				"requests":
					[
						{
							"repeatCell":
								{
									"cell":
										{
											"userEnteredFormat":
												{
													"horizontalAlignment": 'CENTER',
													"verticalAlignment": 'MIDDLE',
													'wrapStrategy': 'LEGACY_WRAP',
													"textFormat":
														{
															"bold": True,
															"fontSize": 16
														}
												}
										},
									"range":
										{
											"sheetId": 0,
											"startRowIndex": 1,
											"endRowIndex": 1000,
											"startColumnIndex": 8,
											"endColumnIndex": 14
										},
									"fields": "userEnteredFormat"
								},
						}
					]
			}
		).execute()

	def url(self):
		"""
		Returns current spreadsheet's URL
		:return: URL
		"""
		return self.spreadsheet['spreadsheetUrl']

	def push(self, eventId):
		"""
		Uses get_kill function to parse for AO event, pushes results into current spreadsheet.
		:param eventId:  (ex. https://www.albiononline2d.com/en/scoreboard/events/208053435 <- those numbers)
		"""
		to_push = get_kill(eventId)
		part_one = '=IMAGE("'
		part_two = '")'
		part_three = '=HYPERLINK("https://www.albiononline2d.com/en/scoreboard/events/'
		part_four = '","AO2D")'
		self.service.spreadsheets().values().batchUpdate(
			spreadsheetId=self.spreadsheet['spreadsheetId'],
			body={
				"valueInputOption": 'USER_ENTERED',
				"data": [
					{
						"range": f'A{self.count}:A{self.count}',
						"majorDimension": "ROWS",
						"values": [[to_push['Victim']]]
					},
					{
						"range": f'B{self.count}:B{self.count}',
						"majorDimension": "ROWS",
						"values": [[f"{part_one}{to_push['MainHand']}{part_two}"]]
					},
					{
						"range": f'C{self.count}:C{self.count}',
						"majorDimension": "ROWS",
						"values": [[f"{part_one}{to_push['OffHand']}{part_two}"]]
					},
					{
						"range": f'D{self.count}:D{self.count}',
						"majorDimension": "ROWS",
						"values": [[f"{part_one}{to_push['Head']}{part_two}"]]
					},
					{
						"range": f'E{self.count}:E{self.count}',
						"majorDimension": "ROWS",
						"values": [[f"{part_one}{to_push['Armor']}{part_two}"]]
					},
					{
						"range": f'F{self.count}:F{self.count}',
						"majorDimension": "ROWS",
						"values": [[f"{part_one}{to_push['Shoes']}{part_two}"]]
					},
					{
						"range": f'G{self.count}:G{self.count}',
						"majorDimension": "ROWS",
						"values": [[f"{part_one}{to_push['Cape']}{part_two}"]]
					},
					{
						"range": f'H{self.count}:H{self.count}',
						"majorDimension": "ROWS",
						"values": [[f"{part_one}{to_push['Mount']}{part_two}"]]
					},
					{
						"range": f'I{self.count}:I{self.count}',
						"majorDimension": "ROWS",
						"values": [[f"{to_push['Victim_IP']}"]]
					},
					{
						"range": f'J{self.count}:J{self.count}',
						"majorDimension": "ROWS",
						"values": [[f"{str(to_push['Time'])}"]]
					},
					{
						"range": f'K{self.count}:K{self.count}',
						"majorDimension": "ROWS",
						"values": [[f'{part_three}{to_push["EventId"]}{part_four}']]
					}
				]
			}).execute()
		if to_push['Victim_IP'] < 1300:
			self.service.spreadsheets().values().batchUpdate(
				spreadsheetId=self.spreadsheet['spreadsheetId'],
				body={
					"valueInputOption": 'USER_ENTERED',
					"data": [
						{
							"range": f'I{self.count}:I{self.count}',
							"majorDimension": "ROWS",
							"values": [[f"{to_push['Victim_IP']}\nLOW IP!"]]
						}
					]
				}).execute()

			self.service.spreadsheets().batchUpdate(  # IP, Time, Link font
				spreadsheetId=self.spreadsheet['spreadsheetId'],
				body={
					"requests":
						[
							{
								"repeatCell":
									{
										"cell":
											{
												"userEnteredFormat":
													{
														"horizontalAlignment": 'CENTER',
														"verticalAlignment": 'MIDDLE',
														'wrapStrategy': 'LEGACY_WRAP',
														"textFormat":
															{
																"bold": True,
																"fontSize": 16
															},
														"backgroundColor":
															{
																"red": 1.0,
																"blue": 0.0,
																"green": 0.0
															}
													}
											},
										"range":
											{
												"sheetId": 0,
												"startRowIndex": self.count-1,
												"endRowIndex": self.count,
												"startColumnIndex": 8,
												"endColumnIndex": 9
											},
										"fields": "userEnteredFormat"
									},
							}
						]
				}
			).execute()

		self.count = self.count + 1

	def sort(self):
		"""
		Sorts current spreadsheet by IGN and then by time.
		:return:
		"""
		self.service.spreadsheets().batchUpdate(
			spreadsheetId=self.spreadsheet['spreadsheetId'],
			body={
				"requests": [
					{
						"sortRange": {
							"range": {
								"sheetId": 0,
								"startRowIndex": 0,
								"endRowIndex": 1000,
								"startColumnIndex": 0,
								"endColumnIndex": 14
							},
							"sortSpecs": [
								{
									"dimensionIndex": 0,
									"sortOrder": "ASCENDING"
								},
								{
									"dimensionIndex": 9,
									"sortOrder": "ASCENDING"
								},
							]
						}
					}
				]
			}).execute()

	def tick(self, num, chestnum):
		"""
		Exists to checkmark regeared requests.
		:param num: Number of a row
		:param chestnum: Number of a chest
		"""
		if num == '1' or num == 1:
			return
		self.service.spreadsheets().values().batchUpdate(
			spreadsheetId=self.spreadsheet['spreadsheetId'],
			body={
				"valueInputOption": 'USER_ENTERED',
				"data": [
					{
						"range": f'L{num}:L{num}',
						"majorDimension": "ROWS",
						"values": [
							[
								f'=IMAGE('
								f'"https://upload.wikimedia.org/wikipedia/commons/thumb/7/73/Flat_tick_icon.svg/1200px-Flat_tick_icon.svg.png"'
								f')'
							]
						]
					}
				]
			}
		).execute()
		self.service.spreadsheets().values().batchUpdate(
			spreadsheetId=self.spreadsheet['spreadsheetId'],
			body={
				"valueInputOption": 'USER_ENTERED',
				"data": [
					{
						"range": f'M{num}:M{num}',
						"majorDimension": "ROWS",
						"values": [
							[f'{chestnum}']
						]
					}
				]
			}
		).execute()
