#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 20 19:05:23 2020

@author: davidtyrpak
"""

import csv

class ConsumerReports:
    
    def __init__(self, input_csv):
        
        self.input_csv = input_csv
        
        
        
    
    def get_unique_yrs(self):
        
        self.unique_years = set()
        
        with open(self.input_csv, newline='') as csv_file:
            
            reader = csv.DictReader(csv_file)
    
            for row in reader:
                
                date = row['Date received'] #This is the column that contains dates in format yyyy-mm-dd 
                
                year = date.split('-')[0] #grab yyyy from yyyy-mm-dd
                
                if year not in self.unique_years:
                    
                    self.unique_years.add(year)
        
        return self.unique_years
        
    
        
        