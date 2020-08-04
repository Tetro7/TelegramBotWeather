import telebot
import json
# Парсер погоды с сайта Яндекса
import parsingWeatherWeb as p

# Загрузка базы данных пользователей 
if __name__ == '__main__':
	with open('db.txt','r') as db:
		baseData = json.load(db)

# Активация телеграмм бота
bot = telebot.TeleBot('1249203447:AAFjk8vLOVOpomxisA85XnfRyEpAN3b4t7Q')

# Создание клавишь выбора ответа
keyboard1 = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard1.row('Да', 'Нет')


# Обработчик команд отправляемых боту
@bot.message_handler(commands=['weather', 'start', 'delet'])
def registrWeather(message):

	# Приветствие и подсказка для пользователя
	if message.text == '/start':
		bot.send_message(message.chat.id, 'Привет ,{0}! Если хочешь получать информацию о погоде то введи команду /weather'.format(message.from_user.username))

	# Активация регистрации пользователя
	if message.text == '/weather':
		bot.send_message(message.chat.id, 'Хотите получать информацию о погоде каждый день?', reply_markup=keyboard1)

	# Отмена регестрации пользователя
	if message.text == '/delet':
		del baseData[str(message.from_user.id)]


# Обработчик всех вводимых сообщений от пользователя
@bot.message_handler(content_types=['text'])
def checkRegister(message):

	# Если пользователь согласился на регестрации, то происходит проверка вводимого им города
	if str(message.from_user.id) in list(baseData.keys()) and baseData[str(message.from_user.id)]['register'] == False:

		# Если сайт погоды ответит на запрос, то город существует
		if p.get_html(p.URL + str(message.text)).status_code == 200:

			# Далее осуществляется внесение всех данных о пользователе в базу данных 
			baseData[str(message.from_user.id)]['city'] = message.text
			baseData[str(message.from_user.id)]['register'] = True
			bot.send_message(message.chat.id, 'Вы успешно прошли регистрацию! Напишите слово - погода, чтобы узнать погоду в вашем городе сейчас')
			with open('db.txt','w') as db:
				json.dump(baseData, db)
		else:
			bot.send_message(message.chat.id, 'Введён не корректный город!')


	# Если пользователь ответит Да, то он вносится в базу данных и далее бот предложит ввести пользователю его город
	if message.text == 'Да':

		# Если пользователя ещё не было в базе, то для него создаётся своя ячейка, иначе бот сообщит, что пользователь ранее уже был зарегестрирован на рассылку
		if not (str(message.from_user.id) in list(baseData.keys())):
			baseData[str(message.from_user.id)] = {'city': 0, 'register': False}
			bot.send_message(message.chat.id, 'Введите свой город на английском (Пример: orel)')
				
		elif str(message.from_user.id) in list(baseData.keys()) and baseData[str(message.from_user.id)]['register'] == True:
			bot.send_message(message.chat.id, 'Вы уже зарегестрированы!')	

	elif message.text == 'Нет':
		bot.send_message(message.chat.id, 'Жаль')


	# Отправляет пользователю информацию о погоде 
	if message.text.lover() == 'погода':
		if baseData[str(message.from_user.id)]['register'] == True:
			weatherNow = p.parser(baseData[str(message.from_user.id)]['city'])
			bot.send_message(message.chat.id, 'Сейчас в {0} {1} {2}'.format(baseData[str(message.from_user.id)]['city'], weatherNow['temp'], weatherNow['day']))
		else:
			bot.send_message(message.chat.id, 'Вы не зарегестрированы! Пройдите регестрацию')

bot.polling(none_stop=True, interval=0)