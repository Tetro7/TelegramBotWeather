from bs4 import BeautifulSoup
import requests


URL = 'https://yandex.ru/pogoda/'
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0', 'accept': '*/*'}

def get_html(url, params=None):
	site = requests.get(url, headers=HEADERS, params=params)
	return site

def get_content(html):
	soup = BeautifulSoup(html, 'html.parser')
	item = soup.find('a', class_='fact__basic')
	weather = {}
	weather['temp'] = item.find('span', class_='temp__value').get_text(strip=True)
	weather['day'] = item.find('div', class_='link__condition').get_text(strip=True)
	return weather

def parser(city):
	html = get_html(URL + str(city))
	info = get_content(html.text)
	return info

