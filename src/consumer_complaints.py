#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 20 19:05:23 2020

@author: davidtyrpak
"""

import csv

import sys

import os

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
        
        #a stable sort of year and then 'Product' will allow us to summarize data over each year and product for that year
        #To grab yyyy from 'Date recieved': row['Date received'].split('-')[0] 
        
        sorted_data = sorted(csv_input, key = lambda row: (row['Date received'].split('-')[0], row['Product'])) 
        #sorted_data is a list of OrderedDicts
        #Each OrderedDict has column names as keys, and corresponding row data as values. We have as many OrderderedDicts as we have rows
        #in the input csv file
        print(sorted_data)
    #grab the very first Year and Product, both should be sorted in numeric/alphabetical order 
    current_date = sorted_data[0]['Date received']
    
    current_year = current_date.split('-')[0] #grab yyyy from yyyy-mm-dd
    
    current_product = sorted_data[0]['Product']
    
    
    product_complaint_counter = 0 #total number of complaints received for that product and year
    
    at_least_one_complaint = set() #total number of companies receiving at least one complaint for that product and year
    
    bad_companies = [] # add a company to this list each time find a complaint for the given year and given product. 
    #The worst company is the one repeated the most in this list
   
    #iterate through each row of the dataset
    for row_counter in range(0, len(sorted_data), 1):
        
        company = sorted_data[row_counter]['Company']
        
        new_date = sorted_data[row_counter]['Date received']
        
        new_year = new_date.split('-')[0] #grab yyyy from yyyy-mm-dd
        
        new_product = sorted_data[row_counter]['Product']
        
        #if the year AND product havent changed AND we are not on the final row
        if new_year == current_year and new_product == current_product and row_counter < (len(sorted_data) - 1):
            
           
                
            product_complaint_counter += 1
            
            
            #append the company to the list of bad companies for that product and year
            bad_companies.append(company)
            
            if company not in at_least_one_complaint:
                
                at_least_one_complaint.add(company)
            else:
                pass
           
                
         #if the year hasnt changed but the product has AND we are not on the final row
        elif new_year == current_year and new_product != current_product and row_counter < (len(sorted_data) - 1):
            
            #at this point, the new_product variable is different fron current_product, which was the previous row(s)
            #we need to add our summarized data for current_product
            row_data = [current_product, current_year, product_complaint_counter, 
                        len(at_least_one_complaint),max_percentage(bad_companies)]
            
            #append our inner list to summarized data nest list
            summarized_data.append(row_data)
            
            ##Now we need to clear AND update our product collection variables.##
            
            #clear
            #----------------------------------------
            
            #clear our list of bad companies
            bad_companies.clear()
            
            #reset our number of product complaints to zero
            product_complaint_counter = 0
            
            #and clear our set of companies that had at least one complaint
            at_least_one_complaint.clear()
            
            #Now add information for the new_product
            #----------------------------------------
            bad_companies.append(company)
            
            product_complaint_counter += 1
            
            at_least_one_complaint.add(company)
            
            #update the current product
            current_product = new_product
        
         #if the year has changed AND we are not on the final row, we need to update our product AND year variables
        elif new_year != current_year and row_counter < (len(sorted_data) - 1):
            
            
            
            #but first add our existing summarized data for the current product and current year
            row_data = [current_product, current_year, product_complaint_counter, 
                        len(at_least_one_complaint),max_percentage(bad_companies)]
            
            #append our inner list to summarized data nest list
            summarized_data.append(row_data)
             
             ##Now we need to clear AND update our product collection and year variables.##
             
             #clear
             #---------------------------------------------------
             
             #clear our list of bad companies
            bad_companies.clear()
                
            #reset our number of product complaints to zero
            product_complaint_counter = 0
                
            #and clear our set of companies that had at least one complaint
            at_least_one_complaint.clear()
            
            #Now add information for the new_product for this year
            #---------------------------------------------------
            bad_companies.append(company)
                
            product_complaint_counter += 1
                
            at_least_one_complaint.add(company)
                
            #update the current product
            current_product = new_product
            
            #update current year
            current_year = new_year
        
         #if we are on the final row, we require some additional logic
        elif row_counter == (len(sorted_data) - 1):
            
            #if the final row doesnt the year or product, we need just need to add the new data and summarize 
            if new_year == current_year and new_product == current_product:
                
                #update product counter for new_product
                product_complaint_counter += 1
                    
                #append the company to the list of bad companies for that product and year
                bad_companies.append(company)
                    
                if company not in at_least_one_complaint:
                        
                     at_least_one_complaint.add(company)
                else:
                    pass
                
                row_data = [current_product, current_year, product_complaint_counter, 
                            len(at_least_one_complaint),max_percentage(bad_companies)]
                
                summarized_data.append(row_data)
            
            #if the final row keeps the year the same but changes the product, we need to add data for current_product AND new product
            elif new_year == current_year and new_product != current_product:
                
                row_data = [current_product, current_year, product_complaint_counter, 
                            len(at_least_one_complaint),max_percentage(bad_companies)]
                
                summarized_data.append(row_data)
                
                
                #clear
                #----------------------------------------
                
                #clear our list of bad companies
                bad_companies.clear()
                
                #reset our number of product complaints to zero
                product_complaint_counter = 0
                
                #and clear our set of companies that had at least one complaint
                at_least_one_complaint.clear()
                
                #Now add information for the new_product
                #----------------------------------------
                bad_companies.append(company)
                
                product_complaint_counter += 1
                
                at_least_one_complaint.add(company)
                
                #update the current product
                current_product = new_product
                
                #and summarize for new product
                row_data = [current_product, current_year, product_complaint_counter, 
                            len(at_least_one_complaint),max_percentage(bad_companies)]
                
                summarized_data.append(row_data)
                
            elif new_year != current_year:
                
                #but first add our existing summarized data for the current product and current year
                row_data = [current_product, current_year, product_complaint_counter, 
                            len(at_least_one_complaint),max_percentage(bad_companies)]
                
                #append our inner list to summarized data nest list
                summarized_data.append(row_data)
                 
                 ##Now we need to clear AND update our product collection and year variables.##
                 
                 #clear
                 #---------------------------------------------------
                 
                 #clear our list of bad companies
                bad_companies.clear()
                    
                #reset our number of product complaints to zero
                product_complaint_counter = 0
                    
                #and clear our set of companies that had at least one complaint
                at_least_one_complaint.clear()
                
                #Now add information for the new_product for this year
                #---------------------------------------------------
                bad_companies.append(company)
                    
                product_complaint_counter += 1
                    
                at_least_one_complaint.add(company)
                    
                #update the current product
                current_product = new_product
                
                #update current year
                current_year = new_year
                
                #and summarize for new product
                row_data = [current_product, current_year, product_complaint_counter, 
                            len(at_least_one_complaint),max_percentage(bad_companies)]
                
                summarized_data.append(row_data)
                
                
                
                
                
                
            
            
   
    #output results csv file into the directory specified by output_dir
    results_location = os.path.join(output_dir, "results.csv")
    
    with open(results_location, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(summarized_data)        
           
    return summarized_data      

    
               
generate_report("/Users/davidtyrpak/Desktop/consumer_complaints.csv", "/Users/davidtyrpak/Desktop")              
               
       
       
       
      
   
   


   
   
   
   
   
    

                    
                    
                    
                    
                        
                
                
        
        
        
        
       
       
       
    
        
        