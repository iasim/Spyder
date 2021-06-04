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
import numpy as np
import scipy.spatial
import re
import pandas as pd

###
### NICE PARSER ###
###

a_file = open("C:/Users/Radha/OneDrive - Drexel University/College/Senior Design/CI 491 Senior Project I/Natural Language Processing/Compare/NICE.csv", "r")

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

a_file = open("C:/Users/Radha/OneDrive - Drexel University/College/Senior Design/CI 491 Senior Project I/Natural Language Processing/Compare/CT.txt", "r")

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

def loadGloveModel(File):
    print("Loading Glove Model")
    f = open(File, encoding="utf8")
    gloveModel = {}
    for line in f:
        splitLines = line.split()
        word = splitLines[0]
        wordEmbedding = np.array([float(value) for value in splitLines[1:]])
        gloveModel[word] = wordEmbedding
    print(len(gloveModel)," words loaded!")
    return gloveModel

def preprocess(raw_text):
    # keep only words
    letters_only_text = re.sub("[^a-zA-Z]", " ", raw_text)
    # convert to lower case and split
    words = letters_only_text.lower().split()
    # remove stopwords
    stopword_set = set(stopwords.words("english"))
    cleaned_words = list(set([w for w in words if w not in stopword_set]))
    return cleaned_words

def cosine_distance_wordembedding_method(s1, s2, s3, s4):
    try:
        vector_1 = np.mean([model[word] for word in preprocess(s1)],axis=0)
        vector_2 = np.mean([model[word] for word in preprocess(s3)],axis=0)
        cosine = scipy.spatial.distance.cosine(vector_1, vector_2)
        rounded = round((1-cosine)*100,2)
        if rounded >= 75:
            return ('{} | {} | {} | {}%'.format(s2, s1, s4, rounded))
    except KeyError:
        pass

model = loadGloveModel('C:/Users/Radha/OneDrive - Drexel University/College/Senior Design/CI 491 Senior Project I/Natural Language Processing/Compare/gloveFile.txt')

for c, d in end_COURSE:
    for k, n in end_NICE:
        results = cosine_distance_wordembedding_method(d, c, n, k)
        print(results)
