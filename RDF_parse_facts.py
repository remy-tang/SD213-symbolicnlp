# -*- coding: utf-8 -*-
"""
Created on Wed Jun 15 09:28:08 2022

@author: Remy
"""

def replace_all(predicate):
    predicate = predicate.replace(",","_").replace("(","").replace(")","").replace("'","_").replace(".","").replace("ʻ","_").replace("ʼ","_").replace(" ","").replace("/","").replace("ʾ","").replace("&","and").replace("%22","").replace("%2F","").replace("!","").replace("40","forty").replace('ʻ',"_").replace("50","fifty").replace("-","_").replace('"',"").replace("@","_")
    predicate = ''.join(i for i in predicate if not i.isdigit())
    return(predicate.lower())
    #this is the quickest method according to https://stackoverflow.com/questions/3411771/best-way-to-replace-multiple-characters-in-a-string

import re
from unidecode import unidecode

rfilename = "C:\\Users\Remy\SD213\Project\yago-wd-facts.txt"
wfilename = "C:\\Users\Remy\SD213\Project\\facts.pl"
write_relations = True
# Classes
search_a_class = True
classes_to_keep = ['hasOccupation','spouse','children','parent']
informations_to_keep = ['birthPlace','memberOf','knowsLanguage','nationality', 'deathPlace', 'award', 'gender', 'homeLocation', 'alumniOf']
index_of_class = 2
print_classes = False

# Ressources
keeped_persons = set()
index_of_ressource = 3
print_ressources = False
keeped_occupations = set(['Actor'])

# Other parameters
print_unknown_parse = False
counter = 0

f = open(rfilename, "r", encoding="utf-8")
lines = f.readlines()
if(write_relations):
    fw = open (wfilename, "w", encoding="utf-8")
    fw.write(":- set_prolog_flag(encoding,utf8).\n")
    fw.write(":- style_check(-singleton).\n")
    fw.write(":- encoding(utf8).\n")
    print('\nWriting predicates\n')
    print('Getting Interesting Persons')
for class_to_search in classes_to_keep :
    #classes = set()
    #ressources = set()
    
    for line in lines:
        match_schema = re.search(r'<http://yago-knowledge.org/resource/(\S+)>\s+<http://schema.org/(\w+)>\s+<http://yago-knowledge.org/resource/(\S+)>\s+.\n', line)
        
        if (match_schema != None):
            person = match_schema.group(1)
            tempclass = match_schema.group(index_of_class)
            #classes.add(tempclass)
            if ( tempclass == class_to_search):
                occupation = match_schema.group(index_of_ressource)
                #ressources.add(occupation)
                if (occupation in keeped_occupations and not("," in person)):
                    keeped_persons.add(person)
                elif (person in keeped_persons and not("," in occupation) and class_to_search != 'hasOccupation' ) :
                    keeped_persons.add(occupation)
                elif (occupation in keeped_persons and not("," in person) and class_to_search != 'hasOccupation' ) :
                    keeped_persons.add(person)

            if (write_relations and tempclass == class_to_search and person in keeped_persons):
                predicate = tempclass+"("+replace_all(match_schema.group(1))+","+replace_all(match_schema.group(3))+").\n"
                fw.write(unidecode(unidecode( predicate ,"utf-8")).replace("-","").replace("'","_").replace("%f","").replace('"',"").replace(",)",",JeanMi)").replace("!","").replace("@","_"))
                counter +=1
        # elif (match_yago != None):
        #     classes.add(match_yago.group(index_of_class))
        #     if match_yago.group(index_of_class) == class_to_search:
        #         ressources.add(match_yago.group(index_of_ressource))
        # elif (match_bioyago != None):
        #     classes.add(match_bioyago.group(index_of_class))
        #     if match_bioyago.group(index_of_class) == class_to_search:
        #         ressources.add(match_bioyago.group(index_of_ressource))
        # elif (print_unknown_parse):
        #     print(line)
                
        # if limit_iterations != 0:
        #     iteration += 1
        #     if iteration >= limit_iterations:
        #         break
        
        # line = f.readline() 
    # if (print_classes):
    #     print(classes)
    # if (print_ressources):
    #     print(ressources)
    print('\n' + str(class_to_search) + ':')
    print('keeped_persons :',len(keeped_persons))
    print('counter :',counter)
    
print('\nGetting Interesting Informations')
for information_to_search in informations_to_keep :
    for line in lines:
        match_schema = re.search(r'<http://yago-knowledge.org/resource/(\S+)>\s+<http://schema.org/(\w+)>\s+<http://yago-knowledge.org/resource/(\S+)>\s+.\n', line)
        
        if (match_schema != None):
            person = match_schema.group(1)
            tempclass = match_schema.group(index_of_class)
            information = match_schema.group(index_of_ressource)
            if (write_relations and tempclass == information_to_search and person in keeped_persons):
                predicate = tempclass+"("+replace_all(person)+","+replace_all(information)+").\n"
                fw.write(unidecode(unidecode(predicate,"utf_8")).replace("-","").replace("'","_").replace("%f","").replace('"',"").replace("!","").replace(",)",",JeanMi)").replace("@","_"))
                counter +=1
    print('\n' + str(information_to_search) + ':')
    print('counter :',counter)

fw.close()