from googleapiclient import discovery
from oauth2client.service_account import ServiceAccountCredentials

CREDENTIALS_FILE = 'fax-regear-e746f082262e.json'
credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, ['https://www.googleapis.com/auth'
                                                                                  '/spreadsheets',
                                                                                  'https://www.googleapis.com/auth'
                                                                                  '/drive'])


class FaxRegear:
    count = 1

    def __init__(self):
        self.service = discovery.build('sheets', 'v4', credentials=credentials)
        spreadsheet_body = {
            'properties': {'title': 'FAX REGEAR', 'locale': 'en_US'},
            'sheets': [{'properties': {'sheetType': 'GRID',
                                       'sheetId': 0,
                                       'title': 'GOD BLESS',
                                       'gridProperties': {'hideGridlines': False, 'rowCount': 1000, 'columnCount': 7}}}]
        }
        self.spreadsheet = self.service.spreadsheets().create(body=spreadsheet_body).execute()
        driveService = discovery.build('drive', 'v3', credentials=credentials)
        driveService.permissions().create(fileId=self.spreadsheet['spreadsheetId'], body={'type': 'anyone', 'role': 'reader'}, fields='id').execute()
        self.service.spreadsheets().batchUpdate(spreadsheetId=self.spreadsheet['spreadsheetId'], body={
            "requests":
                {
                    "updateDimensionProperties": {
                        "range": {
                            "sheetId": 0,
                            "dimension": "COLUMNS",  # COLUMNS - потому что столбец
                            "startIndex": 0,  # Столбцы нумеруются с нуля
                            "endIndex": 1  # startIndex берётся включительно, endIndex - НЕ включительно,
                            # т.е. размер будет применён к столбцам в диапазоне [0,1), т.е. только к столбцу A
                        },
                        "properties": {
                            "pixelSize": 317  # размер в пикселях
                        },
                        "fields": "pixelSize"  # нужно задать только pixelSize и не трогать другие параметры столбца
                    }
                },
        }).execute()
        self.service.spreadsheets().batchUpdate(spreadsheetId=self.spreadsheet['spreadsheetId'], body={
            "requests":
                {
                    "updateDimensionProperties": {
                        "range": {
                            "sheetId": 0,
                            "dimension": "COLUMNS",  # COLUMNS - потому что столбец
                            "startIndex": 1,  # Столбцы нумеруются с нуля
                            "endIndex": 6  # startIndex берётся включительно, endIndex - НЕ включительно,
                            # т.е. размер будет применён к столбцам в диапазоне [0,1), т.е. только к столбцу A
                        },
                        "properties": {
                            "pixelSize": 128  # размер в пикселях
                        },
                        "fields": "pixelSize"  # нужно задать только pixelSize и не трогать другие параметры столбца
                    }
                },
        }).execute()
        self.service.spreadsheets().batchUpdate(spreadsheetId=self.spreadsheet['spreadsheetId'], body={
            "requests":
                {
                    "updateDimensionProperties": {
                        "range": {
                            "sheetId": 0,
                            "dimension": "ROWS",  # COLUMNS - потому что столбец
                            "startIndex": 0,  # Столбцы нумеруются с нуля
                            "endIndex": 1000  # startIndex берётся включительно, endIndex - НЕ включительно,
                            # т.е. размер будет применён к столбцам в диапазоне [0,1), т.е. только к столбцу A
                        },
                        "properties": {
                            "pixelSize": 128  # размер в пикселях
                        },
                        "fields": "pixelSize"  # нужно задать только pixelSize и не трогать другие параметры столбца
                    }
                },
        }).execute()
        self.service.spreadsheets().batchUpdate(spreadsheetId=self.spreadsheet['spreadsheetId'], body={
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
                                        "startRowIndex": 0,
                                        "endRowIndex": 1000,
                                        "startColumnIndex": 0,
                                        "endColumnIndex": 1
                                    },
                                "fields": "userEnteredFormat"
                            }
                    }
                ]
        }).execute()

    def get_url(self):
        spreadsheetURL = self.spreadsheet['spreadsheetUrl']
        return spreadsheetURL

    def get_id(self):
        spreadsheetId = self.spreadsheet['spreadsheetId']
        return spreadsheetId

    def push(self, package):
        body_insides = {
            "valueInputOption": 'USER_ENTERED',
            "data": [
                {
                    "range": f'A{self.count}:F{self.count}',
                    "majorDimension": "ROWS",
                    "values": [
                        package
                    ]
                }
            ]
        }
        self.service.spreadsheets().values().batchUpdate(spreadsheetId=self.spreadsheet['spreadsheetId'], body=body_insides).execute()
        self.count = self.count + 1
