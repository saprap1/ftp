#Get data from pro football reference
import requests
import lxml.html as lh
import pandas as pd
import re
from bs4 import BeautifulSoup
import requests
import openpyxl
import os
import string

from datetime import datetime
from datetime import timedelta 


def getSheet(link_first, link_second, version, name, dist_feet, avg_speed, posts, drives, year, avg_min):
    link = link_first + version + link_second
    a = requests.get(link)
    soup = BeautifulSoup(a.text, 'lxml')

    tb = soup.find("tbody")
    try:
        row = tb.findAll("tr")
        getW = soup.find('span', {'itemprop': 'weight'})
        weight = getW.text[0:3]
    except:
        v = int(version) + 1
        version = "0" + str(v)
        #print (link + " " + version)
        getSheet(link_first, link_second, version, name, dist_feet, avg_speed, posts, drives, year, avg_min)
        print(name)
        return
    global counting
    counting += 1
    print(name + " " + str(counting))
    labels = ['GM', 'Date', 'Weight', 'MP', 'FGA', '3PA', 'FTA', 'ORB', 'DRB', 'AST', 'TO', 'Fouls', 'PTS', 'dist_feet', 'avg_speed', "post_ups", "drives", "Injury"]
    
    bigL = []
    for x in row:
        items = x.findAll("td")
        counter = 0
        L = []
        for y in items:
            if(counter == 0):
                if(y.string=="None"):
                    print(y.string)
                    continue

            '''
            0 = game
            1 = date
            8 = minutes played
            10 = fga
            13 = 3fga
            16 = fta
            18 = offensive rebounds
            19 = def rebounds
            21 = assists
            24 = turnovers
            25 = personal fouls
            26 = points
            '''

            stats_to_ints = [0, 10, 13, 16, 18, 19, 21, 24, 25, 26]
            date = 1
            minutes = 8
            
            
            if (counter in stats_to_ints or counter == date or counter == minutes):
                if (counter in stats_to_ints):
                    x = y.string
                    if (x!=None):
                        L.append(int(x))
                    else:
                        L.append("")
                else:
                    if(counter==minutes):
                        s = y.text.split(":")
                        sInt0 = float(s[0])
                        sInt1 = float(s[1])
                        sInt1 /= 60
                        sInt1 = round(sInt1, 2)
                        
                        sInt0 += sInt1
                        L.append(sInt0)
                        
                        divisor = sInt0/avg_min
                        divisor = (round(divisor, 2))
                        
                    #date appending
                    else:
                        L.append(y.text)
                        L.append(int(weight))
            counter+=1
        if (len(L)>3):
            #float(str(round(answer, 2)))
            
            L.append(float(dist_feet)*divisor)
            L.append(float(avg_speed))
            L.append(float(posts)*divisor)
            L.append(float(drives)*divisor)
        if(len(L)==3):
            zero = [0,0,0,0,0,0,0,0,0,0,0,0,0,0]
            L.extend(zero)

        if(len(L)!=0):
            L.append("")
            #L.append("")
            bigL.append(L)
            

    df = pd.DataFrame.from_records(bigL, columns=labels)
    df.dropna()
    #print(df)
    filename = name + ".xlsx"
    if(year=="2014"):
        path = "bball_reference_2013-2014/" + filename
    elif year=="2015":
        path = "bball_reference_2014-2015/" + filename
    elif year=="2019":
        path = "bball_reference_2018-2019/" + filename
        
    writer = pd.ExcelWriter(path)
    df.to_excel(writer,'Sheet1')
    writer.save()



def loadSportsVu(book, sheet, row_count, year):
    
    for i in range (2, row_count+1):
        s = sheet.cell(row=i, column=2).value
        if (s == None):
            continue
        #call function on s
        name = s[1:]
        
        name = re.sub(r'[^\w\s]','',name)
        
        if(name == "JJ Barea"):
            name = "Jose Barea"
        elif(name=="Henry Walker"):
            name = "Bill Walker"
        elif(name == "Luc Mbah a Moute"):
            name = "Luc Mbaha"
        elif(name == "Mo Williams"):
            name = "Maurice Williams"
        elif(name == "Nene"):
            name = "Nene Hilario"
        elif(name == "Cedi Osman"):
            name = "De-Cedi Osman"
        elif(name == "Clint Capela"):
            name = "Ca-Clint Capela"
        elif(name == "Frank Ntilikina"):
            name = "La-Frank Ntilikina"
        elif(name == "Maxi Kleber"):
            name = "Maxi Klebi"
            
        arr = name.split(" ")
        version = "01"
        #column 5 and 6
        avg_min = sheet.cell(row=i, column=4).value
        dist_feet = sheet.cell(row=i, column=5).value
        avg_speed = sheet.cell(row=i, column=6).value
        posts = sheet.cell(row=i, column=7).value
        drives = sheet.cell(row=i, column=8).value
        
        if (len(arr[1])>=5):
            link_first = ("https://www.basketball-reference.com/players/" + arr[0][0] + "/" + arr[1][0:5] + arr[0][0:2])
            #link_first += version
            link_second = "/gamelog/" + year + "/"
            link_first = link_first.lower()
            link_second = link_second.lower()
        else:
            link_first = ("https://www.basketball-reference.com/players/" + arr[0][0] + "/" + arr[1] + arr[0][0:2])
            link_second = "/gamelog/" + year + "/"
            link_first = link_first.lower()
            link_second = link_second.lower()
        f = name + "_" + year
        getSheet(link_first, link_second, version, f, dist_feet, avg_speed, posts, drives, year, avg_min)


# gets a list of the active players only under the given letter
def getActivePlayers(letter):

    url = "https://www.pro-football-reference.com/players/" + letter + "/"
    a = requests.get(url)           # get all the players with last name starting with letter
    soup = BeautifulSoup(a.text, 'lxml')
    content = soup.find("div", {"class":"section_content"})
    players = content.find_all("b")     # bolded name indicates active

    player_names = []
    player_url = []                 # this is what can be added to the URL to get the gamelog data for the player
                                    # it's the first 4 letters of the last name concatendated with the first 2 letters of the first name
    for wrapper in players:
        p = wrapper.text            # this is the string "FIRST_NAME LAST_NAME (POS)"
        p_content = p.split(" ")    # ["FIRST_NAME", "LAST_NAME", "(POS)"]
        player_names.append(p_content)

    for lst in player_names:
        name = ""
        name += lst[1][:4]  # first 4 letters of the last name
        name += lst[0][:2]  # first 2 letters of the first name
        player_url.append(name)

    return player_url


if __name__ == "__main__":
    #this would load a list of all NFL players and then make a call to scrape
    '''
    book1 = openpyxl.Workbook()
    book1 = openpyxl.load_workbook('2013-2014_combined_red.xlsx')
    sheet1 = book1.get_sheet_by_name('Sheet1')   
    row_count1 = sheet1.max_row
    year = "2014"
    #loadSportsVu(book1, sheet1, row_count1, year)
    '''



    # loop through each letter of the alphabet and get all the active players
    # (I'm trying to think of a more efficient way to do this bc this is pretty slow, but... I don't think there is a better way)
    letters = list(string.ascii_uppercase)
    player_url = []
    for l in letters:
         player_url += getActivePlayers(l)
    

    # list of all the URLS for the 2018 game logs for every currently ACTIVE player in the NFL (according to pro football reference)
    active_urls = []
    for p in player_url:
        # construct URL and add to active_urls
        u = "https://www.pro-football-reference.com/players/" + p[0] + "/" + p + "00/gamelog/2018/"
        active_urls.append(u)

    for u in active_urls:
        print(u)


    




    #link = link_first + version + link_second
    # link is always "https://www.pro-football-reference.com/players/" + <first letter last name> + "/" + <first 4 letters last name> + <first 2 letters first name> + "00/gamelog/" + <season> + "/"
    link = "https://www.pro-football-reference.com/players/B/BradTo00/gamelog/2018/"

    # link = "https://www.pro-football-reference.com/players/B/BreeDr00/gamelog/2018/"
    # link = "https://www.pro-football-reference.com/players/T/TuraKe00/gamelog/2018/"


    a = requests.get(link)
    soup = BeautifulSoup(a.text, 'lxml')

    tb = soup.find("tbody")
    row = tb.findAll("tr")
    getW = soup.find('span', {'itemprop': 'weight'})
    weight = getW.text[0:3]
    print(weight)
    print("---------------------------------------------------")
    labels = ["Date", "G#", "Cmp", "Att", "Cmp%", "Yds", "TD", "Int", "Rate", "Sk", "Yds", "Y/A", "AY/A", "Att", "Yds", "Y/A	TD", "Tgt", "	Rec", "Yds", "Y/R", "TD", "Ctch%", "Y/Tgt	TD", "Pts", "	Fmb", "FF	", "FR", "Yds", "TD"]
    
    bigL = [["a", "b", "c"], ["d", "e", "f", "g"]]
    l = ["1", "2", "3", "4"]
    

    wb  = openpyxl.Workbook();
    # wb = openpyxl.load_workbook(filename = 'data.xlsx')
    dest_filename = 'data.xlsx'
    ws1 = wb.active
    ws1.title = "active players"

    for x in row:
        items = x.findAll("td")
        counter = 0
        L = []

        append_row = []
        # print(items)

        # ws1.append(items)
        for y in items:
            if(counter == 0):
                if(y.string!="None"):
                    print(y.string)
                    append_row.append(y.text)

        # append_row = append_row[1:]
        ws1.append(append_row)
        print("---------------------------------------------------")
  
    
    # wb = Workbook()
    # ws = wb.active
    # df = pd.DataFrame.from_records(bigL, columns=l)


   


    # for row in range(1, len(labels)):
    #     # ws1.append(range(600))
    #     # ws1.append(labels)
    #     row = tb.findAll("tr")
    #     items = x.findAll("td")
    #     ws1.append(items)

    # print(wb.get_sheet_names());

    wb.save(filename = dest_filename)


    # df = pd.DataFrame.from_records(bigL, columns=labels)
    # filename = "data.xlsx"
    # writer = pd.ExcelWriter(filename)
    # df.to_excel(writer,'Sheet1')
    # writer.save()
    # df.to_excel("data.xlsx")    
    

    '''
    try:
        row = tb.findAll("tr")
        getW = soup.find('span', {'itemprop': 'weight'})
        weight = getW.text[0:3]
    except:
        v = int(version) + 1
        version = "0" + str(v)
        #print (link + " " + version)
        getSheet(link_first, link_second, version, name, dist_feet, avg_speed, posts, drives, year, avg_min)
        print(name)
        return
    global counting
    counting += 1
    print(name + " " + str(counting))
    labels = ['GM', 'Date', 'Weight', 'MP', 'FGA', '3PA', 'FTA', 'ORB', 'DRB', 'AST', 'TO', 'Fouls', 'PTS', 'dist_feet', 'avg_speed', "post_ups", "drives", "Injury"]
    '''
# main()