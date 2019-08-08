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


    if version == 4:
        return "na"
    link = linkfirst + str(version) + linksecond
    a = requests.get(link)
    soup = BeautifulSoup(a.text, 'lxml')

    '''
    # Check if this is the right player's page
    # (players with different names might have earlier link versions)
    title = soup.find("title")
    print("FROM PAGE:", title.text, "LOOKING FOR", fullName)
    if (title.text).find(fullName) != -1:
        print("try_link: found correct page...", link)
        # well... I found out that there are multiple Josh Allen's
        return
    '''
    
    '''
    # print("try_link", link)
    try:
        # This will fail if a 2018 gamelog doesn't exist
        tb = soup.find("tbody")
        row = tb.findAll("tr")
        return link
    except:
        # increase the version and try again
        version += 1
        try_link(linkfirst, version, linksecond)
    '''

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

        '''
        # dest_filename = firstName + "_" + lastName + year + ".xlsx"
        if (position.find('/') != -1):
            pos_split = position.split("/")
            position = pos_split[0] + "-" + pos_split[1]

        # only finish up the workbook if there is a NEW position
        if (prev_position != position):
            dest_filename = position + "_data" + year + ".xlsx"
            wb.save(filename = dest_filename)
            prev_position = position
            # start a new workbook
            wb = openpyxl.Workbook()
            sheet = wb.active
        '''
    
        if count == 4:
           break

        s = sheet2.cell(row=i, column=1).value
        x = s.split(",")
        firstName = x[-1][1:]
        lastName = x[0]
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
            
            # fullName = firstName + " " + lastName
            # link = try_link("https://www.pro-football-reference.com/players/" + lastName[0] + "/" + lastName[:4] + firstName[:2] + "0", version, "/gamelog/" + year + "/", fullName)
            '''
            if link == "na":
                continue
            a = requests.get(link)
            soup = BeautifulSoup(a.text, 'lxml')
            tb = soup.find("tbody")
            row = tb.findAll("tr")
            '''
            print("skipping for " + firstName + " " + lastName + "...")
            continue

        for x in row:
            items = x.findAll("td")
            counter = 0
            append_row = [lastName, firstName, position]

            # print(items)

            for y in items:
                if(counter == 0):
                    if(y.string!="None"):
                        append_row.append(y.text)
            
            '''
            fantasy points calculation by position
            Since items is a list of <td> tags, we can just get the text from that item in the list

            Some players don't have *all* the data (if u look here:got here https://www.pro-football-reference.com/players/B/BarkMa00/gamelog/2018/
                             you'll see that there is no 24th column)
                    -- column names are not consistent for all players...

            '''
            # print(x)
            if position == "QB":
                yds_pass = float(items[13].text)
                td_pass = float(items[14].text)
                intercep = float(items[15].text)
                rush_yds = float(items[22].text)
                rush_td = float(items[24].text)
                points = yds_pass/25 + td_pass*4 + intercep*-2 + rush_yds/10 + rush_td*6
            elif position == "TE":
                yds_rec = float(item[12].text)
                td = float(items[14].text)
                fmb = float(items[19].text)
                points = yds_rec/10 + td*6 + fmb*-2
            elif position == "WR":
                rec_yds = float(items[12].text)
                rec_td = float(items[14].text)
                rush_yds = float(items[18].text)
                rush_td = float(items[20].text)
                fmb = float(items[23].text)
                points = rec_yds/10 + rec_tc*6 + rush_yd/10 + rush_td*6 + fmb*-2
            elif position == "RB":
                rush_yds = float(items[11].text)
                rush_td = float(items[13].text)
                rec_yds = float(items[16].text)
                rec_td = float(items[18].text)
                fmb = float(items[23].text)
                points = rush_yds/10 + rush_td*6 + rec_yds/10 + rec_td*6 + fmb*-2
            elif position == "K":
                #points calculation
                xpm = float(item[10].text)
                xpa = float(item[11].text)
                fgm = float(item[13].text)
                fga = float(item[14].text)
                pts = float(item[17].text)
                points = (xpm- (xpa-xpm)) + (fgm*3 - (fga-fgm)) 
            else:
                #wr/te/rb calc
                points = 0
                   
            append_row.append(points)
            sheet.append(append_row)
            # sheet.append([points])

        
        dest_filename = firstName + "_" + lastName + year + ".xlsx"
        wb.save(filename = dest_filename)

        

        count +=1
        
main()