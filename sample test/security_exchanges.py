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
import string
import pandas as pd

import random


# url = 'https://www.sec.gov/Archives/edgar/data/320193/000032019318000145/a10-k20189292018.htm'
url = 'https://www.sec.gov/Archives/edgar/data/320193/000119312519074868/d720211d8a12b.htm'


def scrap_data(url):
	page = urlopen(url)

	# parse the html using beautiful soap and store in variable `soup`
	soup = BeautifulSoup(page.read(), 'html.parser')
	data = []
	elements = soup.findAll(text=re.compile('Securities registered pursuant.*'))
	if len(elements) > 0:
		for element in elements:
			if '12(b)' in element.lower():
				next_element = element.parent.parent.find_next_siblings('div')
				table = next_element[0].find('table')
				rows = table.findChildren('tr')
				table_data_row = rows[2]
				table_data_row_headers = rows[3].findChildren('td')
				data_columns = table_data_row.findChildren('td')
				headers = [value.text for value in table_data_row_headers]
				column1_values = [value.text for value in data_columns[0].findChildren('div')]
				column2_values = [value.text for value in data_columns[2].findChildren('div')]
				data.append([headers[0], headers[2]])
				for i in range(0, len(column1_values)):
					data.append([column1_values[i], column2_values[i]])


	else:
		elements = soup.findAll(text=re.compile('Securities to be registered pursuant.*'))
		for element in elements:
			if '12(b)' in element.lower():
				table = element.parent.parent.find_next_siblings('table')[0]
				rows = table.findAll('tr')
				for row in rows[1:]:
					if row.text.replace(' ', '') != '':
						cells = row.findAll('td')
						cells1 = cells[0].findAll('p')
						cells2 = cells[2].findAll('p')
						if len(cells1) > 1 and len(cells2) > 1:
							cell1_value = ' '.join([cell.text for cell in cells1])
							cell2_value = ' '.join([cell.text for cell in cells2])
							data.append([cell1_value.strip(), cell2_value.strip()])
						else:
							data.append([cells[0].text.strip(), cells[2].text.strip()])

	for i in data:
		print(i)
	file_name = url.split('/')[-1].split('.')[0]
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
		print('Usage: python security_exchanges.py "<URL>"')
