'''
scrape.py
Scrape data from players and export to CSV file
'''

import sys
import requests
import csv
from bs4 import BeautifulSoup


if __name__ == "__main__":
	if (len(sys.argv) != 3):
		print("USAGE: python3 scrape.py <POSITION> <SEASON>")

	else:
		# Build URL based on user preference
		url = "http://www.nfl.com/stats/categorystats?archive=false&conference=null&statisticPositionCategory="
		url += sys.argv[1]
		url +="&season="
		url += str(sys.argv[2])
		url += "&seasonType=REG&experience=&tabSeq=1&qualified=true&Submit=Go"
		response = requests.get(url)

		# In cases requests.get() fails fails
		if response.status_code != 200:
			print("ERROR: status_code", response.status_code)

		html = response.content

		soup = BeautifulSoup(html, "lxml")

		nfl_table = soup.find("tbody")

		# print(nfl_table.prettify())
	
		for wrapper in nfl_table.find_all("td"):
			print(wrapper.text.strip())