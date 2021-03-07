from parse import GetGear
from spreadsheet import FaxRegear

if message.content.startswith('..play'):  # Guess a word game starts here
	await channel.send('Игра в виселицу:')
	current_game = GameLogic()
	await channel.send(current_game.show_word_pl())
	# await channel.send(current_game.show_word_op())
	while True:
		msg = await client.wait_for('message')
		if current_game.game_state() or msg.clean_content == '..stop':
			break
		if msg.clean_content == '..tries':
			await channel.send(current_game.fail_count)
			msg = await client.wait_for('message')
		reply = current_game.give_answ(msg.clean_content)
		try:
			await channel.send(reply)
		except discord.errors.HTTPException:
			await channel.send('Какая-то хуйня я хз')
		await channel.send(current_game.show_word_pl())
		if current_game.game_state() or msg.clean_content == '..stop':
			break

	await channel.send('Игра окончена.')

	pass