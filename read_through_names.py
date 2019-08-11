#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  7 10:57:56 2019

@author: JayMessina
"""
import openpyxl
from bs4 import BeautifulSoup
import requests

def try_link(linkfirst, version, linksecond, fullName):
    return

'''
    fantasy points calculation by position and returns the total calculated for each game
    Since items is a list of <td> tags, we can just get the text from that item in the list
'''
def calculate_points(position, items):
    points = 0
    try:
        if position == "QB":
            yds_pass = float(items[13].text)
            td_pass = float(items[14].text)
            intercep = float(items[15].text)
            rush_yds = float(items[22].text)
            rush_td = float(items[24].text)
            #fumb = float(items[34])
            points = yds_pass/25 + td_pass*4 + intercep*-2 + rush_yds/10 + rush_td*6 
            #fumb*-2
        elif position == "TE":
            # Is there a way to get the information by the attribute data-stat? that seems to be the only consistent thing among players
            # Works for: Rob Gronkowski
            # Fails for: Delanie Walker (only 1 row, not fumbles), Eric Ebron (has an entire section for passing unlike gronk), Ed Dickson (doesn't even have fumbles)
            print(items)
            print('yds_rec', items[10].text, 'td', items[12].text, 'fmb', items[17].text)
            # print(items)
            yds_rec = float(items[12].text)
            td = float(items[14].text)
            fmb = float(items[17].text)
            points = yds_rec/10 + td*6 + fmb*-2
        elif position == "WR":
            rec_yds = float(items[12].text)
            rec_td = float(items[14].text)
            rush_yds = float(items[18].text)
            rush_td = float(items[20].text)
            fmb = float(items[23].text)
            points = rec_yds/10 + rec_td*6 + rush_yds/10 + rush_td*6 + fmb*-2
        elif position == "RB":
            rush_yds = float(items[11].text)
            rush_td = float(items[13].text)
            rec_yds = float(items[16].text)
            rec_td = float(items[18].text)
            fmb = float(items[23].text)
            points = rush_yds/10 + rush_td*6 + rec_yds/10 + rec_td*6 + fmb*-2
        elif position == "K":
            #points calculation
            xpm = float(items[10].text)
            xpa = float(items[11].text)
            fgm = float(items[13].text)
            fga = float(items[14].text)
            pts = float(items[17].text)
            points = (xpm- (xpa-xpm)) + (fgm*3 - (fga-fgm)) 
        else:
            #wr/te/rb calc
            points = 0
    except:
        # print("skipping points calculation for...", firstName, lastName)
        print("skip")
        # continue
    # print(points)
    return points


# Get the fantasy points for this player
def get_points(link_half, year):
    link = link_half + "/fantasy/" + year
    a = requests.get(link)
    soup = BeautifulSoup(a.text, 'lxml')

    ret_points = []

    try:
        tb = soup.find("tbody")
        row = tb.findAll("tr")
    except:
        print("No fantasy log found for:", link)

    for x in row:
        items = x.findAll("td")
        # fantasy points are under the FantPt column, which is always the 3rd to last column
        try:
            pts = float(items[-3].text)
        except:
            # in case the cell is empty, let's just put 0 there... though this might skew training data
            pts = 0
        ret_points.append(pts)

    return ret_points






def main():
    book2 = openpyxl.Workbook()
    book2 = openpyxl.load_workbook('all_players_2019.xlsx')
    sheet2 = book2.get_sheet_by_name('Sheet1')   
    row_count2 = sheet2.max_row

    count = 0

    # prev_position = sheet2.cell(row=2, column=2).value  
    
    for i in range (2, row_count2+1):


        position = sheet2.cell(row=i, column=2).value
        wb = openpyxl.Workbook()
        sheet = wb.active

        #########debug stuff#############
        if count == 10:
           break
        #################################

        s = sheet2.cell(row=i, column=1).value
        x = s.split(",")
        firstName = x[-1][1:]
        lastName = x[0]
        version = 0
        year = "2018"
        link = "https://www.pro-football-reference.com/players/" + lastName[0] + "/" + lastName[:4] + firstName[:2] + "0" + str(version) + "/gamelog/" + year + "/"
        #make soup request for data to formulate spreadsheet
        #open a spreadsheet, add fields, save it
        
        ########################more debug stuff#######################
        # link = "https://www.pro-football-reference.com/players/G/GronRo00/gamelog/2018/"
        # firstName = "Rob"
        # lastName = "Gronkowski"

        # link = "https://www.pro-football-reference.com/players/W/WalkHu00/gamelog/2018/"
        # firstName = "Delanie"
        # lastName = "Walker"

        # link = "https://www.pro-football-reference.com/players/E/EbroEr00/gamelog/2018/"
        # firstName = "Eric"
        # lastName = "Ebron"

        # position = "TE"
        ###############################################################

        a = requests.get(link)
        soup = BeautifulSoup(a.text, 'lxml')

        # print("got here", link)
        points = get_points("https://www.pro-football-reference.com/players/" + lastName[0] + "/" + lastName[:4] + firstName[:2] + "0" + str(version), year)
        point_count = 0;

        try:
            tb = soup.find("tbody")
            row = tb.findAll("tr")

            # print(row)

        except:
            # Here, need to handle 2 cases..
            #   - either player is new and doesn't have 2018 data
            #   - or player has a different version # due to sharing a URL
        
            print("skipping for " + firstName + " " + lastName + "...")
            continue

        for x in row:
            items = x.findAll("td")
            counter = 0
            append_row = [lastName, firstName, position]

            for y in items:
                if(counter == 0):
                    if(y.string!="None"):
                        append_row.append(y.text)
            
            
            append_row.append(points[point_count])
            point_count += 1
            sheet.append(append_row)

        
        dest_filename = firstName + "_" + lastName + year + ".xlsx"
        dest_path = year + "_data/" + dest_filename
        # wb.save(filename = dest_filename)
        wb.save(dest_path)

        count +=1
        
main()