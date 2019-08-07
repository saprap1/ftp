#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  7 10:57:56 2019

@author: JayMessina
"""
import openpyxl
from bs4 import BeautifulSoup
import requests

def try_link(linkfirst, version, linksecond):
    link = linkfirst + str(version) + linksecond
    a = requests.get(link)
    soup = BeautifulSoup(a.text, 'lxml')
    if version == 4:
        return "na"
    print("try_link", link)
    try:
        # This will fail if a 2018 gamelog doesn't exist
        tb = soup.find("tbody")
        row = tb.findAll("tr")
        return link
    except:
        # increase the version and try again
        version += 1
        try_link(linkfirst, version, linksecond)


def main():
    book2 = openpyxl.Workbook()
    book2 = openpyxl.load_workbook('all_players_2019.xlsx')
    sheet2 = book2.get_sheet_by_name('Sheet1')   
    row_count2 = sheet2.max_row

    count = 0

    for i in range (2, row_count2+1):

        if count == 10:
            break

        wb = openpyxl.Workbook()
        # dest_filename = 'data_2018.xlsx'
        sheet = wb.active

        s = sheet2.cell(row=i, column=1).value
        x = s.split(",")
        firstName = x[-1][1:]
        lastName = x[0]
        #https://www.pro-football-reference.com/players/B/BradTo00/gamelog/2018/
        version = 0
        year = "2018"
        link = "https://www.pro-football-reference.com/players/" + lastName[0] + "/" + lastName[:4] + firstName[:2] + "0" + str(version) + "/gamelog/" + year + "/"
        #make soup request for data to formulate spreadsheet
        #open a spreadsheet, add fields, save it
        
        a = requests.get(link)
        soup = BeautifulSoup(a.text, 'lxml')

        print("got here", link)

        try:
            tb = soup.find("tbody")
            row = tb.findAll("tr")
        except:
            # Here, need to handle 2 cases..
            #   - either player is new and doesn't have 2018 data
            #   - or player has a different version # due to sharing a URL

            # Gets an error here bc the player page lied to me and indicated a player as active by bolding the font
            # but the player's last active season is 2017, not 2018. We don't need this data, so we can skip it.
            # print(count, "ERROR with", link)
            
            
            # link = try_link("https://www.pro-football-reference.com/players/" + lastName[0] + "/" + lastName[:4] + firstName[:2] + "0", version, "/gamelog/" + year + "/")
            # if link == "na":
                # continue
            # a = requests.get(link)
            # soup = BeautifulSoup(a.text, 'lxml')
            # tb = soup.find("tbody")
            # row = tb.findAll("tr")
            

            # version += 1
            print("continuing..")
            count +=1
            continue

        for x in row:
            items = x.findAll("td")
            counter = 0
            append_row = [link]

            for y in items:
                if(counter == 0):
                    if(y.string!="None"):
                        append_row.append(y.text)

            sheet.append(append_row)

        dest_filename = firstName + "_" + lastName + year + ".xlsx"
        wb.save(filename = dest_filename)

        count +=1
        #page += p.a["href"]
        #s = x[-1][1:] + " " + x[0]
        #print(s)
        
main()