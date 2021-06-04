#!pip uninstall tensorflow tensorflow_hub 
#!pip install tensorflow tensorflow_hub

from absl import logging

import tensorflow as tf #
import tensorflow_hub as hub #
import matplotlib.pyplot as plt #
import numpy as np #
import os
import pandas as pd
import re
import seaborn as sns

tf.compat.v1.disable_eager_execution()



### NOTE: ###

### USE 'KEY' TO GET THE INDIVIDUAL NICE KEYS ###
### USE 'NICE' TO GET THE INDIVIDUAL NICE DESCRIPTIONS ###
### USE 'end_NICE' TO GET THE KEY + DESCRIPTION PAIRING ###

### USE 'COURSENAME' TO GET THE INDIVIDUAL COURSE NAMES ###
### USE 'COURSE' TO GET THE INDIVIDUAL COURSE DESCRIPTIONS ###
### USE 'end_COURSE' TO GET THE COURSENAME + COURSE PAIRING###

import nltk
from nltk import sent_tokenize
from nltk import word_tokenize
from nltk.probability import FreqDist
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import nltk.data
import itertools
import string

###
### NICE PARSER ###
###

a_file = open("C:/Users/socce/Downloads/School/2021 Winter (online)/Senior Design/Week 7/Sentence_Output_radha/NICE.csv", "r")
#MM TEST#a_file = open("C:/Users/socce/Downloads/School/2021 Winter (online)/Senior Design/Week 7/Manual_CT_to_NICE.csv", "r")

desc = []
KEY = []
desc2 = []
descend = []
end = []

#separate each sentence into words
for line in a_file:
  stripped_line2 = line.replace('"', '')
  stripped_line = stripped_line2.replace(',', '')
  line_list = stripped_line.split()
  desc.append(line_list)

#currently, the keys are connected to the first word
#E.G 'K2034Knowledge'
#separate the keys by taking the first 5 characters and appending it to the list named key
for s in desc:
    KEY.append(s[0][:5])

#replace the first word of each sentence, that includes the key, with the word 'Knowledge'
for word in desc:
    word[0] = 'Knowledge'

NICE = []
#join the individual words back into sentences
for sentence in desc:
    value = ' '.join([str(elem) for elem in sentence])
    NICE.append(value)

#connect the KEY with the descriptions stored in NICE
#print final result
end_NICE = list(zip(KEY, NICE))
#print(end_NICE)

###
### COURSE PARSER ###
###

a_file = open("C:/Users/socce/Downloads/School/2021 Winter (online)/Senior Design/Week 7/Sentence_Output_radha/CT.txt", "r")
#MM TEST#a_file = open("C:/Users/socce/Downloads/School/2021 Winter (online)/Senior Design/Week 7/Manual_CT_to_NICE.txt", "r")

#terms that we are not interested in
ignore = ['College/Department', 'Repeat Status', 'Restrictions', 'Corequisite', 'Prerequisites', '>>>']

list_of_lists = []
list_of_lists2 = []
#separate each sentence into words
for line in a_file:
    stripped_line = line.strip()
    list_of_lists2.append(stripped_line)
    line_list = stripped_line.split()
    list_of_lists.append(line_list)

a_file.close()

ans = []
#remove the terms that we are not interested in
#Listed above in the list named ignore
ans.append([sa for sa in list_of_lists2 if not any(sb in sa for sb in ignore)])

COURSE = []
temp = []
COURSENAME = []

#separate the descriptions from the rest of the text
for x in ans:
    for index, element in enumerate(x):
        if index % 2 != 0:
            COURSE.append(element)

#separate the course names from the rest of the text
for x in ans:
    for index, element in enumerate(x):
        if index % 2 == 0:
            temp.append(element)

#remove the unwanted information from the end of the course name
#E.G  3.0 Credits
for word in temp:
    COURSENAME.append(word[:-12])


#connect the COURSENAME with the descriptions stored in COURSE
#print final result
end_COURSE = list(zip(COURSENAME, COURSE))
#print(end_COURSE)





##Initial setup

module_url = "https://tfhub.dev/google/universal-sentence-encoder/1?tf-hub-format=compressed"

# Import the Universal Sentence Encoder's TF Hub module
embed = hub.Module(module_url)

similarity_input_placeholder = tf.compat.v1.placeholder(tf.string, shape=(None))
similarity_message_encodings = embed(similarity_input_placeholder)




##Sentence Encoder

final_results = [] #final_results will be a list containing lists of Course names, Course descriptions, and the correlations between that course and all the NICE Knowledge Descriptions
messages = [] #used by the Sentence Encoder; first item will always be the Course description, which is then compared to all NICE descriptions
for course in end_COURSE:
    result = [course[0], course[1]]

    messages.extend(NICE)
    messages.insert(0, (course[0] + " " + course[1]))
    
    with tf.compat.v1.Session() as session:
        session.run(tf.compat.v1.global_variables_initializer())
        session.run(tf.compat.v1.tables_initializer())
        message_embeddings_ = session.run(similarity_message_encodings, feed_dict={similarity_input_placeholder: messages})

        corr = np.inner(message_embeddings_, message_embeddings_)
        #print(corr[0])
        #heatmap(Courses_Name, Courses_Name + NICE_ID, corr)
        result.append(corr[0])
        final_results.append(result)

    messages = []




### Export to CSV
from csv import writer
from csv import reader
# Open the input_file in read mode and output_file in write mode
with open("C:/Users/socce/Downloads/School/2021 Winter (online)/Senior Design/Week 7/output_1.csv", 'w', newline='') as write_obj:
    csv_writer = writer(write_obj)
    
    course_num = 0
    ID_num = 1
    for course in final_results:
        for ID in KEY:
            row = []
            if final_results[course_num][2][ID_num] >= .70:
                row.append(course[0])
                row.append(ID)
                row.append(final_results[course_num][2][ID_num])
                csv_writer.writerow(row)
            ID_num = ID_num + 1
        course_num = course_num + 1
        ID_num = 1

