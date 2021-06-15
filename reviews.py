
import os
import pandas as pd
from scipy.sparse.csr import csr_matrix
import numpy as np
from typing import List

project_dir = 'D:\GitHub\Projects\Analysis_of_Delivery_Companies_Reviews'
os.chdir(project_dir)

from helpers.utilities import splitRatingsColumn, getRatingsMapping
from processing import text_processing as tp
from texteda import (most_common_words,
                     plot_most_common_words,
                     plot_wordcloud,
                     compute_bigrams,
                     plot_bigrams)

from nltk.corpus import stopwords

processed_pages_file = os.path.join(project_dir, 'processed_pages.txt')
reviews_base_file = os.path.join(project_dir, 'reviews.csv')

ratings_dict = getRatingsMapping()

base_df = pd.read_csv(reviews_base_file, sep=',')

stopwords_ls = stopwords.words('english')
stpw_charlist = ['\'d', '\'m', '\'s', '\'ve', '\'re', '\'ll', 'n\'t', '’']

common_delivery_words = ['delivery', 'deliver', 'driver', 'order', 'uber',
                         'stuart', 'deliveroo', 'food', 'use', 'get', 'service',
                         'customer', 'refund']

stopwords_ls.extend(stpw_charlist)
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
# base_df = base_df[base_df['Review'].notna()]

# Wherever Review is empty, replace it with Title
base_df.loc[base_df['Review'].isnull(), 'Review'] = base_df['Title']

# Split review in tokens and remove punctuation, stopwords
base_df['Review_Tokens_Clean'] = base_df['Review'].apply(lambda row: tp.tokenize_and_clean(text=row, stopwords_ls=stopwords_ls))

# Lemmatize the tokens
base_df['Review_Tokens_Lemma'] = base_df['Review_Tokens_Clean'].apply(lambda row: tp.lemmatize(text=row, pos_type='n'))
base_df['Review_Tokens_Lemma'] = base_df['Review_Tokens_Lemma'].apply(lambda row: tp.lemmatize(text=row, pos_type='a'))


base_df['Reviews_Clean'] = base_df['Review_Tokens_Lemma'].apply(lambda row: ' '.join([x for x in row]))

base_df['Review_Bigram'] = base_df['Review_Tokens_Lemma'].apply(lambda row: tp.sentenceToNGramTokens(text=row, ngram_size=2))
base_df['Review_Bigram_Sentence'] = base_df['Review_Bigram'].apply(lambda row: ' '.join([x for x in row]))


# Exploratory Data Analysis
most_common_words(base_df, text_col='Review_Bigram_Sentence', n_most_common=10)

plot_most_common_words(base_df,  n_most_common=10, text_col='Review_Bigram_Sentence')

plot_wordcloud(base_df, text_col='Review_Bigram_Sentence')

compute_bigrams(base_df, text_col='Reviews_Clean')

plot_bigrams(input_df=base_df, text_col='Reviews_Clean', top_n=10)

'''
From the bigrams plot we can infer that there are 3 main topics in the data:
    1) Case where order arrived but an item was missing
    2) Case when items received very late
    3) Case when the order never arrived
    
The customer service related queries might be adding noise in the data as in all
cases above, the customer most likely would try to contact the customer service
'''

# Deliveroo
most_common_words(base_df[base_df['Company'] == 'Deliveroo'],
                  text_col='Review_Bigram_Sentence',
                  n_most_common=10)


# LDA
from sklearn.feature_extraction.text import CountVectorizer
vectorizer = CountVectorizer(max_df=0.7,
                             min_df=1,
                             max_features=6000)

'''
This create a sparse matrix where each row is a document and each column
is a word. The values [xi, yi] represent a count of how many times a word
appears in that document.
'''

# apply transformation
cv = vectorizer.fit_transform(base_df['Review_Bigram_Sentence']) #.toarray()
# tf_feature_names tells us what word each column in the matrix represents
cv.shape # (15407, 800)


def countVectorizerToDict(vectorizer: CountVectorizer,
                          matrix: csr_matrix) -> dict:
    feature_names = vectorizer.get_feature_names()
    counts = np.asarray(matrix.sum(axis=0))[0]
    return dict(zip(feature_names, counts))

word_counts = countVectorizerToDict(vectorizer=vectorizer, matrix=cv)


from sklearn.decomposition import LatentDirichletAllocation
number_of_topics = 3
lda_model = LatentDirichletAllocation(n_components=number_of_topics,
                                      max_iter=10,
                                      random_state=45,
                                      n_jobs=-1,
                                      verbose=1) # random state for reproducibility
# Fit data to model
lda_model.fit(cv) # (15349, 17697) i.e. 15349 documents (rows), and 17697 words (columns)


# lda_model.fit_transform(term_freq[1:2])
'''
The output is a NxM matrix where N is number of samples(e.g. a document)
and M is the number of topics.
Gives the probability of the document to belong to each of the topics
'''

lda_model.components_[0]
'''
this gives the weight of each word for a specific document
Its size is number_of_documents x number_of_words
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
  
t = get_word_weights_per_topic(lda_model, feature_names=vectorizer.get_feature_names())
t[0][1][0:5]


def show_top_words_per_topic(model, feature_names: List[str], num_top_words: int):
    for i in range(0, len(model.components_)):
        weights = get_word_weights_per_topic(model, feature_names)[i][1]
        print('Topic {0} : {1}'.format(i, weights[0:num_top_words]))


show_top_words_per_topic(lda_model, feature_names=vectorizer.get_feature_names(), num_top_words=10)



# Gensim
import gensim
import gensim.corpora as corpora
# Create Dictionary
id2word = corpora.Dictionary(base_df['Review_Tokens_Lemma'])

# Create Corpus
texts = base_df['Review_Tokens_Lemma']
# Term Document Frequency
corpus = [id2word.doc2bow(text) for text in texts]
# View
print(corpus[:1][0][:30])

from pprint import pprint
# number of topics
num_topics = 3
# Build LDA model
lda_model = gensim.models.LdaMulticore(corpus=corpus,
                                       id2word=id2word,
                                       num_topics=num_topics)
# Print the Keyword in the 3 topics
pprint(lda_model.print_topics())
doc_lda = lda_model[corpus] # We can view each documents distribution over each topic
len(doc_lda)

import pyLDAvis.gensim
import pickle 
import pyLDAvis
# Visualize the topics
pyLDAvis.enable_notebook()
LDAvis_data_filepath = os.path.join('./results/ldavis_prepared_'+str(num_topics))
# # this is a bit time consuming - make the if statement True
# # if you want to execute visualization prep yourself
if 1 == 1:
    LDAvis_prepared = pyLDAvis.gensim.prepare(lda_model, corpus, id2word)
    with open(LDAvis_data_filepath, 'wb') as f:
        pickle.dump(LDAvis_prepared, f)
# load the pre-prepared pyLDAvis data from disk
with open(LDAvis_data_filepath, 'rb') as f:
    LDAvis_prepared = pickle.load(f)
pyLDAvis.save_html(LDAvis_prepared, './results/ldavis_prepared_'+ str(num_topics) +'.html')
LDAvis_prepared

