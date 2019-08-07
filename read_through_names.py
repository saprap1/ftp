#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  7 10:57:56 2019

@author: JayMessina
"""
import openpyxl

def main():
    book2 = openpyxl.Workbook()
    book2 = openpyxl.load_workbook('all_players_2019.xlsx')
    sheet2 = book2.get_sheet_by_name('Sheet1')   
    row_count2 = sheet2.max_row
    for i in range (1, row_count2+1):
        s = sheet2.cell(row=i, column=1).value
        x = s.split(",")
        firstName = x[-1][1:]
        lastName = x[0]
        #https://www.pro-football-reference.com/players/B/BradTo00/gamelog/2018/
        version = "00"
        year = "2018"
        link = "https://www.pro-football-reference.com/players/" + lastName[0] + "/" + lastName[:4] + firstName[:2] + version + "/gamelog/" + year + "/"
        #make soup request for data to formulate spreadsheet
        #open a spreadsheet, add fields, save it
        
        #page += p.a["href"]
        #s = x[-1][1:] + " " + x[0]
        #print(s)
        
main()