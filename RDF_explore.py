# -*- coding: utf-8 -*-
"""
Created on Wed Jun 15 10:36:23 2022

@author: Remy
"""

import re

filename = "C:/Users/Remy/SD213/Project/yago-wd-facts.txt"
class_to_search = "Person"
lines_to_print = 100

print_only_match = False

with open(filename, "r", encoding="utf-8") as f:
    
    for i in range(lines_to_print):
        line = f.readline()
        match_schema = re.search(r'<http://schema.org/(\w+)>\s+<http://www.w3.org/2000/01/rdf-schema#(\w+)>\s<http://schema.org/(\w+)>\s+.\n', line)
        match_yago = re.search(r'<http://yago-knowledge.org/resource/(\w+)>\s+<http://www.w3.org/2000/01/rdf-schema#(\w+)>\s<http://schema.org/(\w+)>\s+.\n', line)
        
        if (print_only_match):
            if (match_schema != None or match_yago != None):
                print(line)
        else:
            print(line)