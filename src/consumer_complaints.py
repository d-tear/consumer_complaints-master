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
        
        """Extract the total number of unique years from the input_csv file of consumer complaints
        
        Returns
        __________________________
        
        A set containing the unique years from the input_csv file of consumer complaints
        """
        
        
        self.unique_years = set()
        
        with open(self.input_csv, newline='') as csv_file:
            
            reader = csv.DictReader(csv_file)
    
            for row in reader:
                
                date = row['Date received'] #This is the column that contains dates in format yyyy-mm-dd 
                
                year = date.split('-')[0] #grab yyyy from yyyy-mm-dd
                
                if year not in self.unique_years:
                    
                    self.unique_years.add(year)
        
        return self.unique_years
    
    
    def get_product_complaint_total(self, year, product):
       
        """Extract the total number of complaints for a given product on a given year
        
        Parameters
        -----------------------------------------------------------
        year : string-type, "yyyy" e.g. "2019"
        product : string-type, financial product name e.g. "Debt collection" (note it is case sensitive)
        
        Returns
        ----------
        the total number of complaints for that product on that year, type-int
        """
        
        product_count = 0 
        
        with open(self.input_csv, newline='') as csv_file:
            
            reader = csv.DictReader(csv_file)
    
            for row in reader:
                
                date = row['Date received'] #This is the column that contains dates in format yyyy-mm-dd 
                
                row_year = date.split('-')[0] #grab yyyy from yyyy-mm-dd
                
                row_product = row['Product'] #grab the product name from the Product column
                
                if row_year == year and row_product == product:
                    
                    product_count = product_count + 1
                    
                else:
                    pass
                
        return product_count
        
        
                    
                    
                    
                    
                    
                    
                    
                        
                
                
        
        
        
        
       
       
       
    
        
        