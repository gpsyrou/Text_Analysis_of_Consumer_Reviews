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

df = pd.read_csv('dataframe.csv')

def processing(df: pd.core.frame.DataFrame) :

    """
    Pre-processing of 'Reviews' column of dataframe 
    - conversion to lowercase
    - tokenization and removal of stopwords
    - removal of punctuation and numerical digits

    """
    stop = stopwords.words('english')
     # Removes spaces and converts to lowercase
    df['Review_processed'] = df['Review'].str.lower().str.strip()
    #  Remove numbers
    df['Review_processed'] = df['Review_processed'].str.replace('\d+', '')
    # Removes punctuation
    df['Review_processed'] = df['Review_processed'].str.replace('[^\w\s]','')

    #Lemmatization
    df['Review_processed'] = df['Review_processed'].astype(str)
    lemmatizer = WordNetLemmatizer()
    df['Review_processed'] = df['Review_processed'].apply(lambda x: [lemmatizer.lemmatize(item) for item in x.split()])
     
    # Tokenization and removal of stop words
    
    df['Review_processed']= df['Review_processed'].apply(lambda x: [item for item in x if item not in stop])
    
    return df

