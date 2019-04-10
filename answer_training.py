# -*- coding: utf-8 -*-
"""
Created on Sat Mar  9 12:45:34 2019

@author: Raja Rajan
"""

import pickle
import collections
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

#input from book
key = []
key.append("A computer is a machine or device that performs processes, calculations and operations based on instructions provided by a software or hardware program. It is designed to execute applications and provides a variety of solutions by combining integrated hardware and software components.")
key.append( "A Computer is an electronic machine that can solve different problems, process data, store & retrieve data and perform calculations faster and efficiently than humans")

key = [item.lower() for item in key] #conversion of key to lowercase text

stop_words = set(stopwords.words('english'))  #to remove stopwords
arr_of_cbm = collections.deque()

for i in range(0,len(key)):   
    
    word_tokens = word_tokenize(key[i])

    filtered_sentence = [w for w in word_tokens if not w in stop_words]
    
    filtered_sentence = []
    
    for w in word_tokens:
        if w not in stop_words:
            filtered_sentence.append(w)   #filtering of stopwords from key
    
    
    text =nltk. word_tokenize(key[i])
    text = nltk.pos_tag(filtered_sentence)  #appending pos tag
    
    noun = ["NN","NNS","NNP","NNPS","PRP","PRP$","WP","WP$"]
    
    dict_index = 0
    text_index = 0
    for i in text:
        if noun.count(i[1]) > 0:
            break
        else:
            text_index += 1
            continue
    cbm = {}
    lst = collections.deque()
    lst.append(text[text_index][0])
    cbm[dict_index] = lst
    
    for i in range(text_index+1,len(text)):
        if text[i][0] is ',' or text[i][0] is '&':
            continue
        elif noun.count(text[i][1]) > 0:
            
            cbm[dict_index].append(text[i][0])
            dict_index += 1
            lst = collections.deque()
            cbm[dict_index] = lst
            cbm[dict_index].append(text[i][0])
        elif text[i][0] is '.':
            dict_index += 1
            lst = collections.deque()
            cbm[dict_index] = lst
    
        else:
            
            cbm[dict_index].append(text[i][0])
            
    
    arr_of_cbm.append(cbm)

with open("answer_book.txt","wb") as fp: 
    #saving arr_of_cbm list of dictionaries in Hard disk
    pickle.dump(arr_of_cbm,fp)


