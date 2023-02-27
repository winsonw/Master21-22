
import json
import math
import pandas as pd
from tqdm import tqdm
import re
from nltk.stem import SnowballStemmer
import csv
import os
import numpy as np
from nltk.corpus import stopwords
import os


    

#------------- Read file ------------------------------------
def readInvertedIdx():
    file_path = "output-data/task2_InvertedIndex.json"
    with open(file_path, 'r') as j:
        InvertedIdx_dict = json.loads(j.read())

    return InvertedIdx_dict



def readCandidate():
    file_path = "coursework-1-data/candidate-passages-top1000.tsv"
    candidate_df = pd.read_csv(file_path, sep='\t', header=None)
    return candidate_df
    


def readTestQueries():
    filepath = "coursework-1-data/test-queries.tsv"
    test_df = pd.read_csv(filepath, sep='\t', header=None)
    return test_df



def read_pid_TermCounts():
    # Read and load file
    file_path = "output-data/task2_pid_TermCounts.json"
    with open(file_path, 'r') as j:
        termCounts_dict = json.loads(j.read())
    return termCounts_dict



def processTermCounts(pid_termCounts_dict):

    pid_termFreq_dict = dict()

    # Calculate the each terms' frequency in this passage
    for pid in pid_termCounts_dict:
        pid_termFreq_dict[pid] = dict()

        totalTerms = sum(pid_termCounts_dict[pid].values())
        for word in pid_termCounts_dict[pid].keys():
            pid_termFreq_dict[pid][word] = pid_termCounts_dict[pid][word] / totalTerms

    return pid_termFreq_dict

#--------------------------------------------------
# Calculate TF-IDF
#--------------------------------------------------


def calIDF(passages_num, invertedIdx_dict):
    idf_dict = dict()
    for word in invertedIdx_dict:
        if len(invertedIdx_dict[word]) == 0:
            continue
        else:
            idf_dict[word] = math.log10(passages_num / (len(invertedIdx_dict[word].keys())))

    return idf_dict
     


#------------------------------------------------------------------
def cal_pid_TF_IDF(termFreq_dict, idf_dict):
    
    pid_TF_IDF_dict = termFreq_dict.copy()
    # pid: {word: xx, word: xx}

    for pid in tqdm(termFreq_dict):
        for word in termFreq_dict[pid]:
            # Record the TF of this word in this passage
            TF = termFreq_dict[pid][word]
            # Calculate IDF of this word
            IDF = idf_dict[word]
            # TF-IDF
            pid_TF_IDF_dict[pid][word] = TF * IDF

    return pid_TF_IDF_dict
        


#------------------------------------------------------------------
def calQueryCounts(idf_dict):

    test_df = readTestQueries()

    qid_words_dict = dict()
    # Process all the query
    for idx, data in tqdm(test_df.iterrows()):
        qid = str(data[0])
        query = data[1]

        # qid_words_dict = {qid: {word: xxx}}
        qid_words_dict[qid] = dict()

        # Normalisation
        query = query.lower() # Convert to lowercase to avoid case mismatch
        query = re.sub(r'[^\w\s]',' ', query) # Remove punctuations

        words = query.split()
        for word in words:
            # Stemming:
            english_stemmer = SnowballStemmer('english')
            word = english_stemmer.stem(word)

            # Remove stop words
            if word in list(stopwords.words('english')):
                continue

            # Check if the word is already in dictionary
            if word not in qid_words_dict[qid].keys():
                qid_words_dict[qid][word] = 1
            else:
                qid_words_dict[qid][word] += 1
    
    writeJson(qid_words_dict, "output-data/task3_qid_TermCounts.json")
    return qid_words_dict




def cal_qid_TF_IDF(qid_words_dict, idf_dict):

    qid_TF_IDF_dict = dict()
    # Process all the query
    for qid in tqdm(qid_words_dict):
        qid_TF_IDF_dict[qid] = dict()

        # Calculate the sum of all words in this qid
        qid_totalTerms = sum(qid_words_dict[qid].values())

        for word in qid_words_dict[qid]:
            # Calculate the FREQUENCY of each words in this qid
            TF = qid_words_dict[qid][word] / qid_totalTerms

            # get the TF-IDF of this qid of each word
            IDF = idf_dict[word] if word in idf_dict else 0

            # score
            qid_TF_IDF_dict[qid][word] = TF * IDF
    
    # The result is a dict {qid: {word: TF-IDF, word1: TF-IDF....} ....}
    return qid_TF_IDF_dict






#------------------------------------------------------------------
def rankResult(output_path, unsorted_path):
    

    unsorted_pd = pd.read_csv(unsorted_path)
    # Add headers to process
    unsorted_pd.columns = ["qid", "pid", "score"]
    unsorted_pd.dropna()

    test_queries_df = pd.read_csv("coursework-1-data/test-queries.tsv", sep='\t', header=None)

    # Empty the file if exsit
    if (os.path.exists(output_path)):
        open(output_path, 'w').close()

    for idx, data in tqdm(test_queries_df.iterrows()):
        qid = str(data[0])
        # Extract all the rows with this qid
        qid_df = unsorted_pd[unsorted_pd["qid"].isin([qid])]

        # print(qid_df)

        extracted_df = qid_df.sort_values(by='score', ascending=False).head(100)
        # append data frame to CSV file
        extracted_df.to_csv(output_path, mode='a', index=False, header=False)





#-------------------------------------------------------
#--------Calculate cosine similarity of TF-IDF----------
#-------------------------------------------------------
def calTFIDF(candidate_df, pid_TF_IDF_dict, qid_TF_IDF_dict):

    # open the file in the write mode
    f = open('output-data/task3_unsorted_tfidf.csv', 'w', newline='')
    # create the csv writer
    writer = csv.writer(f)

    for idx, data in tqdm(candidate_df.iterrows()):
        qid = str(data[0])
        pid = str(data[1])

        # Calculate all the words contain in pid and qid
        all_words = set(list(qid_TF_IDF_dict[qid].keys()) + list(pid_TF_IDF_dict[pid].keys()))

        qid_tfidf_list = [(qid_TF_IDF_dict[qid][word] if word in qid_TF_IDF_dict[qid] else 0) for word in all_words]
        qid_tfidf_vector = np.array(qid_tfidf_list)

        pid_tfidf_list = [(pid_TF_IDF_dict[pid][word] if word in pid_TF_IDF_dict[pid] else 0) for word in all_words]
        pid_tfidf_vector = np.array(pid_tfidf_list)


        similarity = np.dot(qid_tfidf_vector, pid_tfidf_vector) / (np.linalg.norm(qid_tfidf_vector) * np.linalg.norm(pid_tfidf_vector))

        # Store to the csv file
        writer.writerow([qid, pid, similarity])

    # close the file
    f.close()

    # Rank the results according to 'test-queries.tsv'
    output_path = "output-data/tfidf.csv"
    unsorted_tfidf_path = "output-data/task3_unsorted_tfidf.csv"
    rankResult(output_path, unsorted_tfidf_path)




#-------------------------------------------------------
#-----------------------BM 25---------------------------
#-------------------------------------------------------
def BM25(candidate_df, qid_term_counts, invertedIdx_dict, pid_term_counts):
    # Some constants here
    r = 0
    R = 0
    k1 = 1.2
    k2 = 100
    b = 0.75

    # Calculate average document length
    total_length = 0
    for pid in pid_term_counts:
        total_length += sum(pid_term_counts[pid].values())

    avdl = total_length / len(pid_term_counts.keys())

    # open the file in the write mode
    f = open('output-data/task3_unsorted_bm25.csv', 'w', newline='')
    # create the csv writer
    writer = csv.writer(f)

    total_document = len(pid_term_counts)

    for idx, data in tqdm(candidate_df.iterrows()):
        qid = str(data[0])
        pid = str(data[1])

        score = 0
        # Calculate the score
        
        for word in qid_term_counts[qid]:
            # If this word is not in passage, do not need to calculate and add
            if word not in invertedIdx_dict:
                continue
            if pid not in invertedIdx_dict[word]:
                continue

            doc_number = len(invertedIdx_dict[word])
            dl = sum(pid_term_counts[pid].values())

            K = k1 * ((1-b) + b* (dl/avdl))
            first = math.log( ((r+0.5)/(R-r+0.5)) / ((doc_number-r+0.5)/(total_document-doc_number-R+r+0.5)) )

            f_i = invertedIdx_dict[word][pid] 
            second =  (k1+1)*f_i  / (K+f_i)

            qf = qid_term_counts[qid][word]
            third = (k2+1)*qf / (k2+qf)

            score += first*second*third

        # Store to the csv file
        writer.writerow([qid, pid, score])

    # close the file
    f.close()

    # Rank the results according to 'test-queries.tsv'
    output_path = "output-data/bm25.csv"
    unsorted_tfidf_path = "output-data/task3_unsorted_bm25.csv"
    rankResult(output_path, unsorted_tfidf_path)




#------------------------------------------------------------------
def writeJson(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f)   



if __name__ == "__main__":

    if not os.path.isdir("output-data"):
        os.mkdir(os.path.join("output-data", "./"))
        
    # Read file
    pid_termCounts_dict = read_pid_TermCounts()
    invertedIdx_dict = readInvertedIdx()
    candidate_df = readCandidate()
    

    # dict: {word: IDF}
    pid_termFreq_dict = processTermCounts(pid_termCounts_dict)
    idf_dict = calIDF(len(pid_termFreq_dict), invertedIdx_dict)

    # Calculate the TF-IDF of each passage
    pid_TF_IDF_dict = cal_pid_TF_IDF(pid_termFreq_dict, idf_dict)

    # Calculate the TF-IDF of each query
    qid_term_counts = calQueryCounts(idf_dict)
    qid_TF_IDF_dict = cal_qid_TF_IDF(qid_term_counts, idf_dict)

    # Calculate the consine similarity of each qid and pid
    calTFIDF(candidate_df, pid_TF_IDF_dict, qid_TF_IDF_dict)

    # Implement BM25
    BM25(candidate_df, qid_term_counts, invertedIdx_dict, pid_termCounts_dict)
    
