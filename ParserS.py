from bs4 import BeautifulSoup
import requests
import csv

URL = 'https://auto.ria.com/car/mitsubishi/'
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0', 'accept': '*/*'}


def get_html(url, params=None):
	r = requests.get(url, headers=HEADERS, params=params)
	return r


def get_content(html):
	soup = BeautifulSoup(html, 'html.parser')
	items = soup.find_all('div', class_='content-bar')

	cars = []
	for item in items:
		cars.append({
			'title': item.find('span', class_='blue bold').get_text(strip=True),
			'link': item.find('a', class_='address').get('href')
			})

	return cars


def save_file(items, path):
		with open(path, 'w', newline='') as file:
			writer = csv.writer(file, delimiter=';')
			writer.writerow(['Маркаю', 'Ссылка'])
			for item in items:
				writer.writerow([item['title'], item['link']])


def parse():
	html = get_html(URL)
	if html.status_code == 200:
		cars = []
		pages = 3
		for page in range(1, pages + 1):
			print('Парсинг страницы', page, 'из', pages, '...')
			html = get_html(URL, params={'page': page})
			cars.extend(get_content(html.text))

		save_file(cars, 'cars.csv')
	else:
		print('Error')


if __name__ == '__main__':
	parse()  