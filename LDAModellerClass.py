import numpy as np
import pandas as pd
from typing import List

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation

class LDAModeller:
    """ Common class used to perform an end-to-end Latent Dirichlet Allocation
    analysis. The base object of the class is a Pandas Dataframe.
    
    Parameters
    -----------
    input_df: Base dataframe
    reviews_col: String representing the name of the column that contains the reviews
    """

    def __init__(self, input_df: pd.DataFrame, reviews_col: str):
        self.input_df = input_df
        self.reviews_col = reviews_col
 

    def setCountVectorizer(self, max_df: float, min_df: float, max_features: int, ngram_range: tuple):
        """ A project-specific wrapper based on
        https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.CountVectorizer.html
        """
        self.vectorizer = CountVectorizer(max_df=max_df, min_df=min_df,
                                          max_features=max_features, ngram_range=ngram_range)

        
    def computeCountVectorizerMatrix(self):
        try:
            self.cv_matrix = self.vectorizer.fit_transform(self.input_df[self.reviews_col])
            self.cv_matrix_shape = self.cv_matrix.shape
            self.cv_feature_names = self.vectorizer.get_feature_names()           
        except AttributeError:
            raise Exception('CountVectorizer was is not set up..\n')

            
    def identifyNGramsFromCountVectMatrix(self) -> List[List['str']]:
        """ Given a sparse matrix, get the column names where respective 
        columns of that document have non-zero values - indicating that the
        relative column is a word present in the document.
        
        Requires @computeCountVectorizerMatrix() to be fitted beforehand.
        """
        vector_matrix_df = pd.DataFrame(self.cv_matrix.toarray(), columns=self.cv_feature_names)
        
        combined_ngrams_ls = []
        for i in vector_matrix_df.index:
            ngrams_ls = []
            for j in list(np.where(vector_matrix_df.iloc[i] != 0)[0]):
                ngrams_ls.append(vector_matrix_df.columns[j])
            combined_ngrams_ls.append(ngrams_ls)
        return combined_ngrams_ls

    
    def countVectorizerToDict(self) -> dict:
        """ Produces a dictionary of the format dict([column_name, count]),
        where column_name is an n-gram case in the sparse matrix, while count
        describes the number of occurences for that specific n-gram as calculated
        by @computeCountVectorizerMatrix() .
        """
        counts = np.asarray(self.cv_matrix .sum(axis=0))[0]
        return dict(zip(self.cv_feature_names, counts))

    
    def assignNGramsAsColumn(self, ngram_colname: 'str'):
        self.input_df[ngram_colname] = self.identifyNGramsFromCountVectMatrix()
 

    def retrieveTopNgrams(self, top_n: int, n_gram_type='Bigram'):
        self.n_gram_counts = self.countVectorizerToDict()
        if top_n is not None:
            return pd.DataFrame(sorted(self.n_gram_counts.items(),
                                       key=lambda item: item[1],
                                       reverse=True),
            columns=[n_gram_type, 'Count']).head(top_n)        

        
    def setAndFitLDAModel(self, lda_model: LatentDirichletAllocation, topic_num: int, fit_model=True):
        self.lda_model = lda_model
        self.number_of_topics = topic_num
        if fit_model:
            self.fitted_lda_model = self.lda_model.fit(self.cv_matrix)


    def getPerTopicWordWeights(self, sort=True):
        self.word_weights_per_topic = []
        for i, topic in enumerate(self.fitted_lda_model.components_):
            weights = list(zip(self.cv_feature_names, topic))
            if sort:
                weights = sorted(weights, key=lambda x: x[1], reverse=True)
            self.word_weights_per_topic.append([i, weights])

            
    def showTopWordsPerTopic(self, num_top_words: int):
        for i in range(0, len(self.fitted_lda_model.components_)):
            self.getPerTopicWordWeights()
            weights = self.word_weights_per_topic[i][1]
            print('Topic {0} : {1} \n'.format(i+1, weights[0:num_top_words]))
