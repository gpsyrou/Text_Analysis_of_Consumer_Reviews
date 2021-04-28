
import os
import numpy as np
import pandas as pd

project_dir = r'D:\GitHub\Projects\Analysis_of_Delivery_Companies_Reviews'
os.chdir(project_dir)

from helpers.utilities import splitRatingsColumn
from processing import text_processing as tp
from texteda import (most_common_words,
                     plot_most_common_words,
                     plot_wordcloud,
                     compute_bigrams)

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

# Transform dataset

# Delete rows where the review is empty
base_df = base_df[base_df['Review'].notna()]

# Split review in tokens and remove punctuation, stopwords
base_df['Review_Clean'] = base_df['Review'].apply(lambda row: tp.tokenize_and_clean(text=row))

# Lemmatize the tokens
base_df['Review_Lemma'] = base_df['Review_Clean'].apply(lambda row: tp.lemmatize(text=row, pos_type='n'))


base_df['Review_Merged'] = base_df['Review_Lemma'].apply(lambda row: ' '.join([x for x in row]))





# Exploratory Data Analysis
most_common_words(base_df, text_col='Review_Merged', n_most_common=10)

plot_most_common_words(base_df,  n_most_common=10, text_col='Review_Merged')

plot_wordcloud(base_df, text_col='Review_Merged')

compute_bigrams(base_df, text_col='Review_Merged')


# LDA
from sklearn.feature_extraction.text import CountVectorizer
vectorizer = CountVectorizer()
# apply transformation
tf = vectorizer.fit_transform(base_df['Review']) #.toarray()
# tf_feature_names tells us what word each column in the matric represents
tf_feature_names = vectorizer.get_feature_names()
tf.shape

from sklearn.decomposition import LatentDirichletAllocation
number_of_topics = 5
model = LatentDirichletAllocation(n_components=number_of_topics, random_state=45, n_jobs=-1) # random state for reproducibility
# Fit data to model
model.fit(tf) # (15349, 17697) i.e. 15349 documents (rows), and 17697 words (columns)


model.fit_transform(tf[1:5])

model.components_

model.exp_dirichlet_component_
model.get_params

len(model.exp_dirichlet_component_[0])


f = model.exp_dirichlet_component_[0]

k = zip(tf_feature_names, f)
k = [x for x in k]


def display_topics(model, feature_names, no_top_words):
    for topic_idx, topic in enumerate(model.components_):
        print("Topic %d:" % (topic_idx))
        print(" ".join([feature_names[i]
                        for i in topic.argsort()[:-no_top_words - 1:-1]]))

no_top_words = 10

display_topics(model, tf_feature_names, no_top_words)

