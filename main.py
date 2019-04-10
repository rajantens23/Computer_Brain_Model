# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 20:41:45 2019

@author: Raja Rajan"""

#handwritten recognizor

#convert recognized paragraph into CBM
import pickle
import collections
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

key = "A computer is a machine or device that performs processes, computations , operations based on instructions provided by a software or hardware program. It is developed to execute applications and provides a variety of solutions by combining integrated hardware and software components."
key = key.lower()
stop_words = set(stopwords.words('english'))

word_tokens = word_tokenize(key)

filtered_sentence = [w for w in word_tokens if not w in stop_words]

filtered_sentence = []

for w in word_tokens:
    if w not in stop_words:
        filtered_sentence.append(w)


text =nltk. word_tokenize(key)
text = nltk.pos_tag(filtered_sentence)

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
        
    

#compare student's CBM with pre-trained Books CBM
from nltk.stem import WordNetLemmatizer 

lemmatizer = WordNetLemmatizer() 
lemmatizer.lemmatize("rocks")

arr_of_cbm = pickle.load(open("answer_book.txt","rb"))

for i in range(0,len(cbm)):
    for j in range(0,len(cbm[i])):    
        cbm[i][j] = lemmatizer.lemmatize(cbm[i][j])

for i in range(0,len(arr_of_cbm)):
    for j in range(0,len(arr_of_cbm[i])):
        for k in range(0,len(arr_of_cbm[i][j])):
            arr_of_cbm[i][j][k] = lemmatizer.lemmatize(arr_of_cbm[i][j][k])

filename = 'finalized_model.sav'
loaded_model = pickle.load(open(filename, 'rb'))

        
max_score = -99999
max_index = -1
"""
for i in range(0,len(cbm)):
    for j in range(0,len(arr_of_cbm)):
        score = 0
        for k in range(0,len(arr_of_cbm[j])):
            if len(cbm[i]) == len(arr_of_cbm[j][k]):
                flag=0
                print("equal")
                for l in range(0,len(cbm[i])):                    
                    if cbm[i][l]==arr_of_cbm[j][k][l] or loaded_model.most_similar(cbm[i][l]).count(arr_of_cbm[j][k][l]) > 0:
                        flag = 1
                        print(102)
                        continue
                    else:
                        flag = 0
                        print(cbm[i][l],arr_of_cbm[j][k][l])
                        print(105)
                        break
                if flag == 1:
                    score += 1
                    print(score)
            else:
                print("unequal")
        score = (score/len(arr_of_cbm[j])) * 100
        ##print(score)
        if score > max_score:
            max_score = score
            max_index = j
"""        
max_score = -9999
max_index = -1
for i in range(0,len(arr_of_cbm)):
    score = 0
    for j in range(0,len(arr_of_cbm[i])):
        for k in range(0,len(cbm)):
            if len(cbm[k]) == len(arr_of_cbm[i][j]):
                flag = 0
                for n in range(0,len(cbm[k])):
                    lcv = loaded_model.most_similar(cbm[k][n])
                    similarity_list = []
                    for row_i in range(0,len(lcv)):
                        similarity_list.append(lcv[row_i][0])
                    if cbm[k][n] == arr_of_cbm[i][j][n] or similarity_list.count(arr_of_cbm[i][j][n]) > 0:
                        #print(cbm[k][n],arr_of_cbm[i][j][n])
                        flag = 1
                    else:
                        #print("not "+cbm[k][n],arr_of_cbm[i][j][n])
                        flag=0
                        break
                if flag == 1:
                    score += 1
    score =( score/len(arr_of_cbm[i]) )  * 100                
    if score > max_score:
        max_score = score
        max_index = i
    #print("End of question")        
                    
#output the score

print("Student's score is : "+str(max_score/100 * 2))
print("Matched with answer no : " + str(max_index+1 ))