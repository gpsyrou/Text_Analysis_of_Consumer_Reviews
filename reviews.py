
import os
import numpy as np
import pandas as pd

project_dir = r'D:\GitHub\Projects\Analysis_of_Delivery_Companies_Reviews'
os.chdir(project_dir)

import trustplt as pilot
from helpers.utilities import splitRatingsColumn

processed_pages_file = os.path.join(project_dir, 'processed_pages.txt')
reviews_base_file = os.path.join(project_dir, 'reviews.csv')

col_names = ['Company', 'Id', 'Reviewer_Id', 'Title', 'Review', 'Date', 'Rating']
ratings_dict = {1: 'Bad', 2: 'Poor', 3: 'Average', 4: 'Great', 5: 'Excellent'}      

base_df = pd.read_csv(reviews_base_file, sep=',')



# See a distribution of number of reviews among all companies
base_df['Company'].value_counts()

# Check for duplicates
base_df.drop_duplicates(inplace=True)

# Cast columns specific data format
base_df['Date'] = pd.to_datetime(base_df['Date'], format="%Y-%m-%d %H:%M", errors='coerce')
base_df['Rating'] = base_df['Rating'].apply(lambda row: splitRatingsColumn(row)[0]).astype(int)
base_df['Rating_Text'] = base_df['Rating'].apply(lambda row: ratings_dict[row])

# Are there reviewers that have submitted to more than one reviews ?
reviewers_multiple =  base_df['Reviewer_Id'].value_counts()
f = base_df[base_df['Reviewer_Id']==reviewers_multiple.index[0]]




import nltk
from typing import List
from nltk.corpus import stopwords

stopwords_ls = stopwords.words('english')

test = base_df['Review'].iloc[0]

nltk.word_tokenize(test,language='english')


def tokenize_and_clean(text, punct=True, numerics=True) -> List[str]:
    """
    Performs tokenizations and cleaning processes given a document/text.
    The function will always tokenize the given text but the cleaning tasks
    are optional.
    
    Parameters
    ----------
    text: 
        A document, which can be a word or sentence of arbitrary length.

    punct: 
        Indicator of removing tokens that are punctuation marks.
    numerics: 
        Indicator of removing tokens that correspond to numbers.

    Returns
    --------
         A tokenized version of 'text' with the necessary updates depending on
         the cleanup steps performed.
    """
    tokenized = nltk.word_tokenize(text, language='english')
    
    
    
    return tokenized



def remove_stopwords(text: List['str'], stopwords_ls: List['str']) -> List['str']:
    return [token for token in text if token not in stopwords_ls]

