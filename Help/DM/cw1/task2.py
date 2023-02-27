# Task 2

# Use 'candidate-passages-top1000.tsv' for this task
# Build an inverted index for the collection 


import pandas as pd
import json
import re
from tqdm import tqdm
from nltk.stem import SnowballStemmer
from nltk.corpus import stopwords
import nltk
import os
nltk.download('stopwords')



#------------------------------------------------------------------
def readTask1():
    english_stopwords_list = list(stopwords.words('english'))

    with open("output-data/task1_textProbs.json", "r") as j:
        data_dict = json.loads(j.read())

    words_dict = dict()
    # Remove stop words
    for word in tqdm(data_dict):
        if not word in english_stopwords_list:
            words_dict[word] = dict() # Create a new dict to store inverted index

    return words_dict





#------------------------------------------------------------------
def writeJson(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f)




#------------------------------------------------------------------
def calInvertedIdx(path, inverted_dict):

    english_stopwords_list = list(stopwords.words('english'))

    # Create a dict to calculate term frequency for Task3
    term_count_dict = dict()

    # Parsing
    df = pd.read_csv(path, sep='\t', header=None)

    # Tokenization
    for idx, data in tqdm(df.iterrows()):
        id = data[1]
        sentences = data[3]

        # Create a dict to calculate frequency of terms
        if id not in term_count_dict:
            term_count_dict[id] = dict()

        # Normalisation
        sentences = sentences.lower() # Convert to lowercase to avoid case mismatch
        sentences = re.sub(r'[^\w\s]',' ', sentences) # Remove punctuations

        words = sentences.split()
        for word in words:
            # Normalisation: replace french letters with english
            translationTable = str.maketrans("éàèùâêîôûç", "eaeuaeiouc")
            word = word.translate(translationTable)

            # Stemming:
            english_stemmer = SnowballStemmer('english')
            word = english_stemmer.stem(word)

            # Remove stop words
            if word in english_stopwords_list:
                continue # Do not need to process

            # Check if the word is already in dictionary
            if word not in inverted_dict.keys():
                continue
            else:
                if id in inverted_dict[word].keys():
                    inverted_dict[word][id] += 1
                else:
                    inverted_dict[word][id] = 1

            # After checking the words
            if word not in term_count_dict[id].keys():
                term_count_dict[id][word] = 1
            else:
                term_count_dict[id][word] += 1
    
        




#------------------------------------------------------------------
if __name__ == "__main__":
    
    if not os.path.isdir("output-data"):
        os.mkdir(os.path.join("output-data", "./"))

    data_dict = readTask1()
    file_path = "coursework-1-data/candidate-passages-top1000.tsv"
    calInvertedIdx(file_path, data_dict)


