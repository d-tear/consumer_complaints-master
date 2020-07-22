#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 20 19:05:23 2020

@author: davidtyrpak
"""

import csv

import sys

from collections import Counter


def max_percentage(input_list):
    """
    calculate the highest (rounded) percentage duplication in a given list
    
    e.g. ["a", "a", "b"] -> 66
    
    Arguments
    ---------------------------
    input_list : list type
    
    
    
    Returns
    --------------------------
    
    the highest (rounded) percentage duplication, int type (the percentage is rounded using standard conventions)
    (i.e., Any percentage between 0.5% and 1%, inclusive, should round to 1% and anything less than 0.5% should round to 0%)
    """

    count = Counter(input_list).items()

    #a dictionary with key = entry, and value = the percentage of times that entry appears in the list
    percentages = {x: round(float(y) / len(input_list) * 100) for x, y in count}
    
    
    return max(percentages.values())



def generate_report(path_to_csv, output_dir):
    
   """ 
   Generates a summarized consumer complaint report
   
   Arguments
   -------------------------------
   
   path_to_csv : string type, the path to the csv file of consumer complaints
   
   output_dir: string type, the path to the output directory where the report should be generated
   
   Returns
   -------------------------
   
   A nested list of summarized complaints, where each inner list is the summerized data for one finanical product on
   a given year.
   
   This function also writes the nested list to a csv file inside output_dir
   
   """
   
   summarized_data = [] # a nested list, and each inner list is a row of summarized data 
   
   
   
   with open(path_to_csv, 'r', newline='') as f_input:
    csv_input = csv.DictReader(f_input)
    
    #a stable sort of 'Date recived' and then 'Product' will allow us to summarize data over each year and product for that year
    sorted_data = sorted(csv_input, key = lambda row: (row['Date received'], row['Product'])) 
    #sorted_data is a list of OrderedDicts
    #Each OrderedDict has column names as keys, and corresponding row data as values. We have as many OrderderedDicts as we have rows
    #in the input csv file
    
   #grab the very first Year and Product, both should be sorted in numeric/alphabetical order 
   current_date = sorted_data[0]['Date received']

   current_year = current_date.split('-')[0] #grab yyyy from yyyy-mm-dd
   
   current_product = sorted_data[0]['Product']
   
   row_counter = 0 #use this to loop through each OrderedDict/row 
   
   product_complaint_counter = 0 #total number of complaints received for that product and year
   
   at_least_one_complaint = set() #total number of companies receiving at least one complaint for that product and year
   
   bad_companies = [] # add a company to this list each time find a complaint for the given year and given product. 
   #The worst company is the one repeated the most in this list
   
   #iterate through each row of the dataset
   while row_counter < len(sorted_data):
       
       company = sorted_data[row_counter]['Company']
       
       year = sorted_data[row_counter]['Date received']
       
       product = sorted_data[row_counter]['Product']
       
       #if the year hasnt changed, we are still  need to summarize product data for the current year
       if year == current_year:
           
           #if year and product are the same, update our metrics for that product for this year
           if product == current_product:
               
               product_complaint_counter += 1
               
               
               #append the company to the list of bad companies for that product and year
               bad_companies.append(company)
               
               if company not in at_least_one_complaint:
                   
                   at_least_one_complaint.add(company)
               else:
                   pass
            
           #if we make it here, we have iterated through all rows of the current product for the current year.
           #so we need to create the row data for this product of this year, AND update our product collection variables
           #We DONT need to update the year
           else:
               row_data = [current_product, current_year, product_complaint_counter, len(at_least_one_complaint),max_percentage(bad_companies)]
               
               #append our inner list to summarized data nest list
               summarized_data.append(row_data)
               
               ##Now we need to update our product collection variables.##
               
               #update the current product
               current_product = sorted_data[row_counter]['Product']
               
               #clear our list of bad companies
               bad_companies.clear()
               
               #reset our number of product complaints to zero
               product_complaint_counter = 0
               
               #and clear our set of companies that had at least one complaint
               at_least_one_complaint.clear()
               
               
    
              
        
       # row_counter += 1
    
               
               
               
       
       
       
      
   
   


   
   
   
   
   
    

                    
                    
                    
                    
                        
                
                
        
        
        
        
       
       
       
    
        
        