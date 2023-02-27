# Use the data in 'passage-collection.txt' for this task.
# Extract terms (1-grams) from the raw text. 
# You can also perform basic text preprocessing steps.
# You can also choose not to.
# You should not remove stop words for Task 1


# Counts the number of occurrences of terms in the provided data set
# plot their probability of occurrence (normalised frequency) against their frequency ranking
# and qualitatively jusify that these terms follow Zipf's law


import re
import matplotlib.pyplot as plt
import json
from tqdm import tqdm
import pylab

from nltk.stem import SnowballStemmer

import os



#--------------------------------------------------------------
def writeJson(data, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f)




#--------------------------------------------------------------
def toStr(bytes_or_str):
    if isinstance(bytes_or_str, bytes):
        return bytes_or_str.decode('utf-8')
    return bytes_or_str # instance of str 



#--------------------------------------------------------------
#------------- Process this whole Passage ---------------------
#--------------------------------------------------------------
def getTextOccurences(path):
    # Parsing: create an empty dictionary
    words_dict = dict()

    # Tokenisation
    with open(path, "rb") as text_file:
        for line in tqdm(text_file):
            # Normalisation 
            line = toStr(line)  # Conver bytes to string
            line = line.lower() # Convert to lowercase to avoid case mismatch
            line = re.sub(r'[^\w\s]',' ',line) # Remove punctuations
            line = line.strip() # Remove the newline character

            words = line.split()
            for word in words:
                # Normalisation: replace french letters with english
                translationTable = str.maketrans("éàèùâêîôûç", "eaeuaeiouc")
                word = word.translate(translationTable)

                # Stemming:
                english_stemmer = SnowballStemmer('english')
                word = english_stemmer.stem(word)

                # Check if the word is already in dictionary
                if word in words_dict:
                    words_dict[word] = words_dict[word] + 1
                else:
                    words_dict[word] = 1

    text_file.close()

    return words_dict





#--------------------------------------------------------------
def calProbability(words_dict):
    # Sort the words_dict according to the occurrences of terms
    words_dict = dict(sorted(words_dict.items(), key=lambda x: x[1], reverse=True))

    # Calculate the each terms' probability of occurrece
    totalTerms = sum(words_dict.values())
    for key, _ in words_dict.items():
        words_dict[key] = words_dict[key] / totalTerms

    return words_dict




#--------------------------------------------------------------
def plotProbability(words_dict):
    """
    Plot their probability of occurrence (normalised frequency) against their frequency ranking 
    """

    # Plot the probability of occurrence against their frequency ranking 
    plt.plot(range(len(words_dict)), list(words_dict.values()))
    plt.xlabel('Frequency Ranking')
    plt.ylabel('Probability of Occurrence')
    plt.title('Empirical data distribution')
    plt.savefig('images/empirical_distribution.png')




#--------------------------------------------------------------
def calZipf(totalSize):
    # Calculate Zipf's Law
    probability_list = []
    # Calculate H_n
    H_n = 0
    for i in range(1, totalSize + 1):
        H_n += 1/i
    #Calculate the possibility
    for rank in range(1, totalSize + 1):
        probability_list.append(1/(rank*H_n))

    return probability_list


    

#--------------------------------------------------------------
def logLogPlot(words_dict):

    probability_list = calZipf(len(words_dict))

    pylab.loglog(range(len(words_dict)), list(words_dict.values()), label="data")
    pylab.loglog(range(len(words_dict)), probability_list, label="theory (Zipf's law)")
    pylab.title("Log-log plot compared with Zipf's Law and empirical distribution")
    pylab.xlabel("Term frequency ranking (log)")
    pylab.ylabel("Term prob. of occurrence (log)")
    pylab.grid(True)
    pylab.savefig('images/loglog_distribution.png')
    # pylab.show()






#--------------------------------------------------------------
if __name__ == "__main__":
    if not os.path.isdir("output-data"):
        os.mkdir(os.path.join("output-data", "./"))

    if not os.path.isdir("images"):
        os.mkdir(os.path.join("images", "./"))
    
    file_path = "coursework-1-data/passage-collection.txt"
    words_dict = getTextOccurences(file_path)
    words_dict = calProbability(words_dict)
    plotProbability(words_dict)
    print(len(words_dict.items())) 


