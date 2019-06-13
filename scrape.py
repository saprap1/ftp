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

		# Parse using bs4
		html = response.content
		soup = BeautifulSoup(html, "lxml")

		# Contents of overall table
		nfl_table = soup.find("tbody")

		# Number of categories of statistics (i.e. "team", "Att", "TD", etc)
		num_cat = len(soup.find_all("th", {"class": "thd2"}))

		# Parse html of all the categories so we can add to list
		###### THIS SKIPS THE "YDS" CATEGORY BECAUSE THAT HAS CLASS "thd2 order1 right sortable" ########
		categories = soup.find_all("th", {"class": "thd2 right sortable"})

		# categories = soup.find_all("th", {"class": ["thd2 right sortable", "thd2 order1 right sortable"]})
		# categories = soup.find_all("th", attrs={"class": "thd2 right sortable", "class":"thd2 order1 right sortable"})
		# categories = soup.select("th.hd2 right sortable.thd2 order1 right sortable")

		# Add all the different category headers to a list -- initialize with the standard categories that are for every position
		cat_headers = ["Rk", "Player", "Team", "Pos"]
		for item in categories:
			cat_headers.append(item.find("a").text)
		# print(cat_headers)


	
		# Find all the players with their stats 
		players = nfl_table.find_all("td")

		count = 0					# Keep track of what's been printed so far
		reset = num_cat+1		# A reset value for count
		num_players = len(players)

		table = []					# maintain a table where...
		row = []					#... each row contains all the data per player
		

		# Add each player with all the stats for that player
		for wrapper in players:
			count += 1
			if count == reset:
				# New row for each player
				table.append(row)
				row = []
				count = 1
			# Make sure to remove all the extra whitespace
			row.append(wrapper.text.strip())

		'''
		# Print table
		for r in table:
			print(r)
		'''

		# Write to data.csv
		with open('data.csv', 'w') as csv_file:
			writer = csv.writer(csv_file)
			writer.writerow(cat_headers)
			for r in table:
				writer.writerow(r)