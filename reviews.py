
import os
import pandas as pd
from typing import List

project_dir = r'D:\GitHub\Projects\Analysis_of_Delivery_Companies_Reviews'
os.chdir(project_dir)

from helpers.utilities import splitRatingsColumn
from processing import text_processing as tp
from texteda import (most_common_words,
                     plot_most_common_words,
                     plot_wordcloud,
                     compute_bigrams,
                     plot_bigrams)

from nltk.corpus import stopwords

processed_pages_file = os.path.join(project_dir, 'processed_pages.txt')
reviews_base_file = os.path.join(project_dir, 'reviews.csv')

col_names = ['Company', 'Id', 'Reviewer_Id', 'Title', 'Review', 'Date', 'Rating']
ratings_dict = {1: 'Bad', 2: 'Poor', 3: 'Average', 4: 'Great', 5: 'Excellent'}      

base_df = pd.read_csv(reviews_base_file, sep=',')

stopwords_ls = stopwords.words('english')
stopwords_ls.extend(['\'d', '\'m', '\'s', '\'ve', '\'re', '\'ll', 'n\'t', '’'])

common_delivery_words = ['delivery', 'deliver', 'driver', 'order', 'uber', 'stuart', 'deliveroo']
stopwords_ls.extend(common_delivery_words)

# See a distribution of number of reviews among all companies
base_df['Company'].value_counts()

# Check for duplicates
base_df.drop_duplicates(inplace=True)

# Cast columns specific data format
base_df['Date'] = pd.to_datetime(base_df['Date'], format="%Y-%m-%d %H:%M", errors='coerce')
base_df['Rating'] = base_df['Rating'].apply(lambda row: splitRatingsColumn(row)[0]).astype(int)
base_df['Rating_Text'] = base_df['Rating'].apply(lambda row: ratings_dict[row])

# Are there reviewers that have submitted to more than one reviews ?
# reviewers_multiple =  base_df['Reviewer_Id'].value_counts()
# f = base_df[base_df['Reviewer_Id']==reviewers_multiple.index[0]]

# Transform dataset

# Delete rows where the review is empty
base_df = base_df[base_df['Review'].notna()]

# Split review in tokens and remove punctuation, stopwords
base_df['Review_Clean'] = base_df['Review'].apply(lambda row: tp.tokenize_and_clean(text=row, stopwords_ls=stopwords_ls))

# Lemmatize the tokens
base_df['Review_Lemma'] = base_df['Review_Clean'].apply(lambda row: tp.lemmatize(text=row, pos_type='n'))


base_df['Review_Merged'] = base_df['Review_Lemma'].apply(lambda row: ' '.join([x for x in row]))





# Exploratory Data Analysis
most_common_words(base_df, text_col='Review_Merged', n_most_common=10)

plot_most_common_words(base_df,  n_most_common=10, text_col='Review_Merged')

plot_wordcloud(base_df, text_col='Review_Merged')

compute_bigrams(base_df, text_col='Review_Merged')

plot_bigrams(input_df=base_df, text_col='Review_Merged', top_n=10)



# LDA
from sklearn.feature_extraction.text import CountVectorizer
vectorizer = CountVectorizer(max_df=1.0, min_df=1, max_features=800)

'''
This create a sparse matrix where each row is a document and each column
is a word. The values [xi, yi] represent a count of how many times a word
appears in that document.
'''

# apply transformation
tf = vectorizer.fit_transform(base_df['Review_Merged']) #.toarray()
# tf_feature_names tells us what word each column in the matrix represents
tf_feature_names = vectorizer.get_feature_names()
tf.shape # (15407, 800)

from sklearn.decomposition import LatentDirichletAllocation
number_of_topics = 5
lda_model = LatentDirichletAllocation(n_components=number_of_topics,
                                      random_state=45,
                                      n_jobs=-1,
                                      verbose=1) # random state for reproducibility
# Fit data to model
lda_model.fit(tf) # (15349, 17697) i.e. 15349 documents (rows), and 17697 words (columns)


lda_model.fit_transform(tf[1:2])
'''
The output is a NxM matrix where N is number of samples(e.g. a document)
and M is the number of topics.
Gives the probability of the document to belong to each of the topics
'''

lda_model.components_
'''
this gives the weight of each word for a specific document
'''

lda_model.exp_dirichlet_component_
lda_model.get_params


def get_word_weights_per_topic(model, feature_names: List[str], sort=True):
    word_weights_per_topic = []
    for i, topic in enumerate(model.components_):
        weights = list(zip(feature_names, topic))
        if sort:
            weights = sorted(weights, key=lambda x: x[1], reverse=True)
        word_weights_per_topic.append([i, weights])
    return word_weights_per_topic
  
t = get_word_weights_per_topic(lda_model, feature_names=tf_feature_names)
t[0][1][0:5]


def show_top_words_per_topic(model, feature_names: List[str], num_top_words: int):
    for i in range(0, len(model.components_)):
        weights = get_word_weights_per_topic(model, feature_names)[i][1]
        print('Topic {0} : {1}'.format(i, weights[0:num_top_words]))


show_top_words_per_topic(lda_model, feature_names=tf_feature_names, num_top_words=5)



# Gensim
import gensim
import gensim.corpora as corpora
# Create Dictionary
id2word = corpora.Dictionary(base_df['Review_Lemma'])

# Create Corpus
texts = base_df['Review_Lemma']
# Term Document Frequency
corpus = [id2word.doc2bow(text) for text in texts]
# View
print(corpus[:1][0][:30])

from pprint import pprint
# number of topics
num_topics = 5
# Build LDA model
lda_model = gensim.models.LdaMulticore(corpus=corpus,
                                       id2word=id2word,
                                       num_topics=num_topics)
# Print the Keyword in the 5 topics
pprint(lda_model.print_topics())
doc_lda = lda_model[corpus]
