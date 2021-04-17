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

def trimSpace(text) :
    """
    Takes string input, removes leading and trailing spaces and returns string output
    
    """
    return str.strip(text)


def removeNum(text) :
    """
    Takes string input, removes numbers and returns string output
    
    """
    return re.sub('\d+', '',text)

def removePunctuation(text) :
    """
    Takes string input, removes punctuation and returns string output
    """
    return re.sub('[^\w\s]', '',text)

def tokenize(text):
    """
    Takes string input returns list of tokens
    """
    return word_tokenize(text)

def removeStopwords(text):

    """
    Takes string input, removes stop words and returns string output
    """
    stop_words = set(stopwords.words("english"))
    word_tokens = word_tokenize(text)
    filtered_words = [word for word in word_tokens if word not in stop_words]
    return ' '.join(map(str, filtered_words))

def Lemmatize(text):

    """
    Takes string input and returns lemmatized string output
    """
    lemmatizer = WordNetLemmatizer()
    lemma_words = [lemmatizer.lemmatize(item) for item in text.split()]
    return ' '.join(map(str, lemma_words))

    
  

