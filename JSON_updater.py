from parse import GetLastEvents
import time

i = 0
while True:
	GetLastEvents()
	print(f'ok')
	print('started sleeping')
	time.sleep(60)
	print('woke up')
