#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 20 19:05:23 2020

@author: davidtyrpak
"""

import re

import os

import csv

import sys

from collections import Counter



def is_correct_date_format(date):
    
    """
    Ensures date is in the correct format of yyyy-mm-dd or yyyy-dd-mm
    
    Some examples of incorrect format: 
        
    1) yyyy/mm/dd (using slashes instead of hyphens)
    
    2) yy-mm-dd (using 2 digits instead of 4 digits for year)
    
    Parameters
    ----------
    date : string type, e.g. "2019-09-24"
    (assumes yyyy-mm-dd or yyyy-dd-mm --> Note that this code DOESNT check yyyy-dd-mm vs yyyy-mm-dd)
    The code only assumes you have 4 digits, followed by a hyphen, then two digits, a hyphen, and then two digits

    Returns
    -------
    True if date is yyyy-mm-dd or yyyy-dd-mm
    False if not

    """
    
    #find beginning of line, then 4 digits, then a hyphen, then 2 digits, 
    #then a hyphen, then 2 digits, and then the end of the ine
    date_pattern = "^[0-9]{4}-[0-9]{2}-[0-9]{2}$"
    
    x = re.search(date_pattern, date)
    
    #if the pattern doesnt match the txt, x will be None
    if x is not None:
        return True
    else:
        return False




def file_is_empty(path_to_file):
    """
    Check if a given file is empty
    
    Parameters
    ----------
    path_to_file : string type, the path to the file ("/Users/davidtyrpak/Desktop//my_file.csv")

    Returns
    -------
    True if file is empty., False if not

    """
    
    return os.stat(path_to_file).st_size == 0
    


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



def generate_report(input_csv_file, output_csv_file):
    
    """ 
    Generates a summarized consumer complaint report
   
    Arguments
    -------------------------------
   
    input_csv_file : string type, the path to the csv file of consumer complaints ("/Users/davidtyrpak/Desktop/consumer_complaints.csv")
   
    output_csv_file: string type, the path (including filename) where the summarized consumer complaint report should be generated (e.g. /"Users/davidtyrpak/Desktop/report.csv")
   
    Returns
   -------------------------
   
    Does not return anyting.
   
    Writes a single csv report that shows for each financial product and year, 
    the total number of complaints, number of companies receiving a complaint, 
    and the highest percentage of complaints directed at a single company.
   
    """
   
    #ensure input_csv_file has a non-zero size/ is not empty
    if file_is_empty(input_csv_file):
        raise IOError(f"Warning! {input_csv_file} is empty! Please ensure you have the correct file path and that the file is not empty.")
    
    summarized_data = [] # a nested list, and each inner list is a row of summarized data 
   
   
   
    with open(input_csv_file, 'r', newline='') as f_input:
       
        csv_input = csv.DictReader(f_input)
        
        #a stable sort of year and then 'Product' will allow us to summarize data over each year and product for that year
        #To grab yyyy from 'Date recieved': row['Date received'].split('-')[0] 
        
        sorted_data = sorted(csv_input, key = lambda row: (row['Date received'].split('-')[0], row['Product'])) 
        #sorted_data is a list of OrderedDicts
        #Each OrderedDict has column names as keys, and corresponding row data as values. We have as many OrderderedDicts as we have rows
        #in the input csv file
        
    #grab the very first Year and Product, both should be sorted in numeric/alphabetical order 
    current_date = sorted_data[0]['Date received']
    
    #ensure current_date is in format yyyy-mm-dd or yyyy-dd-mm
    if is_correct_date_format(current_date):
        pass
    else:
        print(f"Warning! The dates of the 'Date recieved' column of {input_csv_file} are not in the correct format")
        print("The correct format is yyyy-mm-dd or yyyy-dd-mm")
        print("Common incorrect formats are yy-mm-dd or yyyy/mm/dd")
        print(f"Your incorrect date was {current_date}")
        raise ValueError()
    
    current_year = current_date.split('-')[0] #grab yyyy from yyyy-mm-dd
    
    current_product = sorted_data[0]['Product'].lower() #grab product name and make it lowercase
    
    
    product_complaint_counter = 0 #total number of complaints received for that product and year
    
    at_least_one_complaint = set() #total number of companies receiving at least one complaint for that product and year
    
    bad_companies = [] # add a company to this list each time find a complaint for the given year and given product. 
    #The worst company is the one repeated the most in this list
   
    #iterate through each row of the dataset
    for row_counter in range(0, len(sorted_data), 1):
        
        company = sorted_data[row_counter]['Company']
        
        new_date = sorted_data[row_counter]['Date received']
        
        #ensure new_date is in format yyyy-mm-dd or yyyy-dd-mm
        if is_correct_date_format(new_date):
            pass
        else:
            print(f"Warning! The dates of the 'Date recieved' column of {input_csv_file} are not in the correct format")
            print("The correct format is yyyy-mm-dd or yyyy-dd-mm. Ensure all dates are in this format")
            print("Common incorrect formats are yy-mm-dd or yyyy/mm/dd")
            print(f"Your incorrect date was {new_date}")
            raise ValueError()
        
        new_year = new_date.split('-')[0] #grab yyyy from yyyy-mm-dd
        
        new_product = sorted_data[row_counter]['Product'].lower() #grab product name and make it lowercase
        
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
            
            #maintain sort order
            summarized_data.sort(key = lambda row: row[0])
            
            #The final results file has to be sorted in alphabetical order by Product name.
            #So, we'll sort in place by Product (index 0) each time we append new data. 
            #In practice, I find this is much fatser than doing one big sort at the very end
            summarized_data.sort(key = lambda row: row[0])
            
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
            
            #maintain sort order
            summarized_data.sort(key = lambda row: row[0])
             
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
                
                #maintain sort order
                summarized_data.sort(key = lambda row: row[0])
            
            #if the final row keeps the year the same but changes the product, we need to add data for current_product AND new product
            elif new_year == current_year and new_product != current_product:
                
                row_data = [current_product, current_year, product_complaint_counter, 
                            len(at_least_one_complaint),max_percentage(bad_companies)]
                
                summarized_data.append(row_data)
                
                #maintain sort order
                summarized_data.sort(key = lambda row: row[0])
                
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
                
                #maintain sort order
                summarized_data.sort(key = lambda row: row[0])
                
            elif new_year != current_year:
                
                #but first add our existing summarized data for the current product and current year
                row_data = [current_product, current_year, product_complaint_counter, 
                            len(at_least_one_complaint),max_percentage(bad_companies)]
                
                #append our inner list to summarized data nest list
                summarized_data.append(row_data)
                
                #maintain sort order
                summarized_data.sort(key = lambda row: row[0])
                 
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
                
                #maintain sort order
                summarized_data.sort(key = lambda row: row[0])
                

   
    
    with open(output_csv_file, 'w', newline='') as csvfile:
        
        writer = csv.writer(csvfile)
           
        writer.writerows( summarized_data)       
           
        

    
             
#generate_report("/Users/davidtyrpak/Downloads/complaints.csv", "/Users/davidtyrpak/Desktop")              
           
       
       
def main():

    input_file = sys.argv[1]  

    output_file =  sys.argv[2]   
    
    generate_report(input_file, output_file)  

if __name__ == '__main__':

    main()            

    
      
   
   


   
   
   
   
   
    

                    
                    
                    
                    
                        
                
                
        
        
        
        
       
       
       
    
        
        