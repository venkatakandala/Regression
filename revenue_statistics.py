# import libraries
try:
    # For Python 3.0 and later
    from urllib.request import urlopen
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen
from bs4 import BeautifulSoup

import re
import sys
import pandas as pd
import string

import random


def scrap_data(url):
	page = urlopen(url)

	# parse the html using beautiful soap and store in variable `soup`
	soup = BeautifulSoup(page.read(), 'html.parser')
	data = []
	elements = soup.findAll(text=re.compile('Selected Financial Data'))
	if len(elements) == 2:
		table_div = elements[1].find_parent('table').find_next_siblings('div')[1]
		table = table_div.find('table')
		rows = table.findAll('tr')
		row = rows[2]
		if row.text.replace(' ', '') != '':
			cells = row.findAll('td')
			data.append([
				cells[0].text.strip(),
				cells[1].text.strip(),
				cells[3].text.strip(),
				cells[5].text.strip(),
				cells[7].text.strip(),
				cells[9].text.strip()
			])
		for row in rows[3:]:
			if row.text.replace(' ', '') != '':
				cells = row.findAll('td')
				if len(cells) == 20:
					data.append([
						cells[0].text.strip(),
						cells[1].text.strip() + ' ' + cells[2].text.strip(),
						cells[5].text.strip() + ' ' + cells[6].text.strip(),
						cells[9].text.strip() + ' ' + cells[10].text.strip(),
						cells[13].text.strip() + ' ' + cells[14].text.strip(),
						cells[17].text.strip() + ' ' + cells[18].text.strip()
					])
				elif len(cells) == 15:
					data.append([
						cells[0].text.strip(),
						cells[1].text.strip(),
						cells[4].text.strip(),
						cells[7].text.strip(),
						cells[10].text.strip(),
						cells[13].text.strip()
					])
				elif len(cells) == 10 and cells[0].text.strip() != '':
					data.append([
						cells[0].text.strip(),
						cells[1].text.strip(),
						cells[3].text.strip(),
						cells[5].text.strip(),
						cells[7].text.strip(),
						cells[9].text.strip()
					])
	for i in data:
		print(i)
	file_name = url.split('/')[-1].split('.')[0].strip()
	if file_name == '' or file_name == None:
		letters = string.ascii_letters
		file_name = ''.join(random.sample(letters, 10))

	df = pd.DataFrame(data)
	df.to_csv(file_name + '.csv', index=False, header=False)


if __name__ == '__main__':
	if len(sys.argv) == 2:
		print('URL: ' + sys.argv[1])
		try:
			scrap_data(sys.argv[1])
		except Exception as e:
			print('Error occurred while scrapping: '+str(e))
	else:
		print('Invalid parameters')
		print('Usage: python revenue_statistics.py "<URL>"')
