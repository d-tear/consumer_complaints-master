#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 26 11:24:37 2020

@author: davidtyrpak
"""
import unittest
 
from consumer_complaints import is_correct_date_format 

from consumer_complaints import max_percentage

#Enure dates are correclty analyzed as being yyyy-mm-dd or yyyy-dd-mm
class TestDateFormats(unittest.TestCase):
    
    #Should be True
    def testCorrectFormat(self):
        
        self.assertTrue(is_correct_date_format("2019-09-24"))
        
    #Incorrect format with backslashes instead of hyphens, should be false
    def testIncorrectBackslashFormat(self):
       
       self.assertFalse(is_correct_date_format("2019/09/24"))
    
    #Incorrect format yy-mm-dd instead of yyyy-mm-dd
    def testIncorrectYearDigits(self):
        self.assertFalse(is_correct_date_format("19-09-24"))
  
        
#Ensure percentages are correclty calculated--> the number of times an entry is repeated divided by the total number of entries
class TestMaxPercentage(unittest.TestCase):
    
    #list is made entirely out of repeats of one entry. max_percentage be 100%
    def testSingleEntry(self):
        self.assertTrue(max_percentage(["b", "b", "b", "b"]), 100)
    
    #a single entry should contitutes 100% of the list
    def testSingleNumberEntry(self):
        
        #a single entry, the number 1, contitutes 100% of the list
        self.assertTrue(max_percentage([1]), 100)
                        
    #a single entry should contitutes 100% of the list
    def testSingleStringEntry(self):
        
        #a single entry, the letter a, contitutes 100% of the list
        self.assertTrue(max_percentage(["a"]), 100)
    
    
    #two entries are repeated twice
    def testTwoMaxEntries_A(self):
        self.assertTrue(max_percentage(["a", "a", "b", "b"]), 50)
    
    #two entries are repeated twice, but there is third unique entry
    def testTwoMaxEntries_B(self):
        self.assertTrue(max_percentage(["a", "a", "b", "b", "c"]), 40)
    
    #each entry is unique
    def testAllUnique(self):
        self.assertTrue(max_percentage(["a", "b", "c"]), 33)
        
    
        
                   
                   

if __name__ == '__main__':
    unittest.main()        
    
    
     
 