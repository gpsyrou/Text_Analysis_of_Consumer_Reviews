
import os
import numpy as np
import pandas as pd

project_dir = r'D:\GitHub\Projects\Analysis_of_Delivery_Companies_Reviews'
os.chdir(project_dir)

from helpers.utilities import splitRatingsColumn
from processing import text_processing as tp

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


test = base_df['Review'].iloc[12]

tp.tokenize_and_clean(text=test)

