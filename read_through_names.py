#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  7 10:57:56 2019

@authors: Jay Messina, Priya Sapra
"""
import openpyxl
from bs4 import BeautifulSoup
import requests
import pandas as pd

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
def get_fant_points(link_half, year):

    # It broke at https://www.pro-football-reference.com/players/S/SpenDi00/fantasy/2017 because no fantasy log exists
    # Error: 
    '''
    Traceback (most recent call last):
      File "read_through_names.py", line 204, in <module>
        main()
      File "read_through_names.py", line 160, in main
        points = get_points("https://www.pro-football-reference.com/players/" + lastName[0] + "/" + lastName[:4] + firstName[:2] + "0" + str(version), year)
      File "read_through_names.py", line 90, in get_points
        for x in row:
    UnboundLocalError: local variable 'row' referenced before assignment
    '''

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



'''
- doesn't write dataframe into excel yet (have that stuff commented out rn)
- currently set to run for 2018 only
- have't tried running the whole thing entirely, so there might be bugs there (there's a thing with the arrays not being the same length...
    i know you can fill those spots with something, but I can't figure that out)
'''
def main():
    book2 = openpyxl.Workbook()
    book2 = openpyxl.load_workbook('all_players_2019.xlsx')
    sheet2 = book2.get_sheet_by_name('Sheet1')   
    row_count2 = sheet2.max_row

    count = 0

    # for i in range (2, row_count2+1):
    for i in range (822, row_count2+1):

        position = sheet2.cell(row=i, column=2).value
        # wb = openpyxl.Workbook()
        # sheet = wb.active        

        s = sheet2.cell(row=i, column=1).value
        x = s.split(",")
        firstName = x[-1][1:]
        lastName = x[0]
        version = 0
        year = "2018"
        # year = "2017"
        
        if firstName == "Derek" and lastName == "Carr":
            version = 2
            # print("here")
        
        link = "https://www.pro-football-reference.com/players/" + lastName[0] + "/" + lastName[:4] + firstName[:2] + "0" + str(version) + "/gamelog/" + year + "/"

        
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

        # link = "https://www.pro-football-reference.com/players/G/GrifGa00/gamelog/2018"
        # firstName = "Garret"
        # lastName = "Griffin"
        # position = "TE"
        ###############################################################

        #make soup request for data to formulate spreadsheet
        #open a spreadsheet, add fields, save it
        a = requests.get(link)
        soup = BeautifulSoup(a.text, 'lxml')

        # print("got here", link)

        # get ALL the fantasy points for this player in 1 soup request to the fantasy page
        # each entry is the fantasy points scored for that game
        fantasy_points = []
        fantasy_points = get_fant_points("https://www.pro-football-reference.com/players/" + lastName[0] + "/" + lastName[:4] + firstName[:2] + "0" + str(version), year)
        point_count = 0;    # pointer to current index of fantasy points

        try:
            tb = soup.find("tbody")
            row = tb.findAll("tr")

        except:
            # Here, need to handle 2 cases..
            #   - either player is new and doesn't have 2018/2017 data
            #   - or player has a different version # due to sharing a URL
            print("skipping data collection for " + firstName + " " + lastName + "...")
            continue
        
        ##########################
        # features_wanted =  {'opp_name', 'pts', 'opp_pts', 'game_location','game_result','overtimes', 'wins','losses', 'date_game'}
        # qb_features = {"pass_yds", "pass_td", "pass_int", "rush_yds", "rush_td"}
        # # can't find fumbles for running back
        # rb_features = {"rush_yds", "rush_td", "rec_yds", "rec_td"}
        # wr_features = {"rec_yds", "rec_td", "rush_yds", "rush_td", "fumbles"}
        # te_features = {"rec_yds", "rec_td", "fumbles"}
        # k_features = {"xpm", "xpa", "fgm", "fga", "scoring"}
        ##########################

        # determine what features we want to focus on for each position
        features_wanted = []
        if position == "QB":
            features_wanted = ["pass_yds", "pass_td", "pass_int", "rush_yds", "rush_td"]
        elif position == "RB":
            features_wanted = ["rush_yds", "rush_td", "rec_yds", "rec_td", "fumbles"]
        elif position == "WR":
            features_wanted = ["rec_yds", "rec_td", "rush_yds", "rush_td", "fumbles"]
        elif position == "TE":
            features_wanted = ["rec_yds", "rec_td", "fumbles"]
        elif position == "K":
            features_wanted = ["xpm", "xpa", "fgm", "fga", "scoring"]
        else:
            # skip the player if it's not one that is specified (can adjust this later on...)
            print("Invalid position (not QB, RB, WR, TE, K). Skipping:", position)
            continue

        # initialize all the keys in the dictionary
        # the dataframe will be constructed using the data held in the dictionary
        # key: column name/category, value: list of the stats in the order of the game
        '''
        put this info in the filename
        data_dict["last_name"] = []
        data_dict["first_name"] = []
        data_dict["position"] = []
        '''
        data = []

        # Trying to make a dictionary for each of the columns
        # for each row (game) in this player's gamelog...
        for x in row:

            # add data
            # data_dict["last_name"].append(lastName)
            # data_dict["first_name"].append(firstName)
            # data_dict["position"].append(position)

            # get all the data for that particular game
            # items = x.findAll("td")
            # counter = 0
            # append_row = [lastName, firstName, position]

            # cherry-pick the exact "features" (data) that we want
            #labels = []

            data_append = []

            for f in features_wanted:
                try:
                    stat = x.find("td", {'data-stat': f})
                    #labels.append(f)
                    # print(stat)
                    data_append.append(float(stat.text))
                    # print("here", f, stats.text)
                except:
                    print("data-stat", f, "not found. Skipping this feature for", firstName, lastName)
                    data_append.append(0.0)
                    continue
            try:
                data_append.append(float(fantasy_points[point_count]))
            except:
                data_append.append(0.0)

            data.append(data_append)
            point_count += 1
        print(i)

        print(data)
        # create dataframe from the dictionary
        features_wanted.append("fantasy points")
        df = pd.DataFrame.from_records(data, columns=features_wanted)
        print(df)

        dest_filename = firstName + "_" + lastName + "_" + position + "_" + year + ".xlsx"
        dest_path = year + "_data/" + dest_filename

        writer = pd.ExcelWriter(dest_path)
        df.to_excel(writer, 'Sheet1')
        writer.save()

        
        
        # wb.save(dest_path)

        # count +=1
        
main()