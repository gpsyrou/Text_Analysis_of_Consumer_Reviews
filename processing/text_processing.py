import numpy as np
import pandas as pd
import re
import string
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer 

from nltk.corpus import stopwords
nltk.download('stopwords')
stop = stopwords.words('english')

# project_dir = r'D:\GitHub\Projects\Analysis_of_Delivery_Companies_Reviews'
# os.chdir(project_dir)

def removePunctuation_Num(text, option) :
    """
    Takes string input and option, removes punctuation and returns string output
    Option 1: for removing numbers
    Option 2: for removing punctuation 
    Option 3: for removing both numbers and punctuation
    """
    if option == 1:
        return re.sub('[^\w\s]', '',text)

    elif option == 2:
        return re.sub('\d+', '',text)

    elif option == 3:
        return re.sub('\d+', '',re.sub('[^\w\s]', '',text))
        


def tokenize(text):
    """
    Takes string input returns list of tokens
    """
    return word_tokenize(text)

def removeStopwords(text, stop_words_list):

    """
    Takes string input and list of stop words, removes stop words from input string and returns string output
    """
    word_tokens = word_tokenize(text)
    filtered_words = [word for word in word_tokens if word not in stop_words_list]
    return ' '.join(map(str, filtered_words))

def Lemmatize(text):

    """
    Takes string input and returns lemmatized string output
    """
    lemmatizer = WordNetLemmatizer()
    lemma_words = [lemmatizer.lemmatize(item) for item in text.split()]
    return ' '.join(map(str, lemma_words))

    

  

