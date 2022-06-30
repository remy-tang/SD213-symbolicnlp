# -*- coding: utf-8 -*-
"""
Created on Wed Jun 15 09:28:08 2022

@author: Remy
"""

import re

filename = "C:/Users/Remy/SD213/Project/yago-wd-facts.txt"

# Classes
class_to_search = "Person"
index_of_class = 3
print_classes = False

# Ressources
index_of_ressource = 1
print_ressources = True

# Other parameters
limit_iterations = 0

print_unknown_parse = False

with open(filename, "r", encoding="utf-8") as f:
    
    classes = set()
    ressources = set()
    line = f.readline()
    iteration = 0
    
    while len(line) != 0:
        match_schema = re.search(r'<http://schema.org/(\w+)>\s+<http://www.w3.org/2000/01/rdf-schema#(\w+)>\s<http://schema.org/(\w+)>\s+.\n', line)
        match_yago = re.search(r'<http://yago-knowledge.org/resource/(\w+)>\s+<http://www.w3.org/2000/01/rdf-schema#(\w+)>\s<http://schema.org/(\w+)>\s+.\n', line)
        match_bioyago = re.search(r'<http://yago-knowledge.org/resource/(\w+)>\s+<http://www.w3.org/2000/01/rdf-schema#(\w+)>\s+<http://bioschemas.org/(\w+)>\s+.\n', line)
        
        if (match_schema != None):
            classes.add(match_schema.group(index_of_class))
            if match_schema.group(index_of_class) == class_to_search:
                ressources.add(match_schema.group(index_of_ressource))
        elif (match_yago != None):
            classes.add(match_yago.group(index_of_class))
            if match_yago.group(index_of_class) == class_to_search:
                ressources.add(match_yago.group(index_of_ressource))
        elif (match_bioyago != None):
            classes.add(match_bioyago.group(index_of_class))
            if match_bioyago.group(index_of_class) == class_to_search:
                ressources.add(match_bioyago.group(index_of_ressource))
        elif (print_unknown_parse):
            print(line)
                
        if limit_iterations != 0:
            iteration += 1
            if iteration >= limit_iterations:
                break
        
        line = f.readline()
        
    if (print_classes):
        print(classes)
    if (print_ressources):
        print(ressources)