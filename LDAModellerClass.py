import pandas as pd
import numpy as np
from typing import List
from sklearn.feature_extraction.text import CountVectorizer


class LDAModeller:


    def __init__(self, input_df: pd.DataFrame, reviews_col: str):
        self.input_df = input_df
        self.reviews_col = reviews_col
        
        
    def setCountVectorizer(self, max_df: float, min_df: float,
                           max_features: int, ngram_range: tuple):

        self.vectorizer = CountVectorizer(max_df=max_df,
                                          min_df=min_df,
                                          max_features=max_features,
                                          ngram_range=ngram_range)


    def computeCVMatrix(self):
        try:
            self.cv_matrix = self.vectorizer.fit_transform(self.input_df[self.reviews_col])
            self.cv_matrix_shape = self.cv_matrix.shape
            self.cv_feature_names = self.vectorizer.get_feature_names() 
            
        except AttributeError:
            raise Exception('CountVectorizer was not set up')


    def identifyNGramsFromCVMatrix(self) -> List[List['str']]:
        """ Given a sparse matrix, get the column names where respective columns of that document
        have non-zero values - indicating that the relative column is a word present in the document. 
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
        counts = np.asarray(self.cv_matrix .sum(axis=0))[0]
        return dict(zip(self.cv_feature_names, counts))


    def assignNGramsAsColumn(self, ngram_colname: 'str') -> None:
        self.input_df[ngram_colname] = self.identifyNGramsFromCVMatrix()

    
    def retrieveTopNgrams(self, top_n: int, n_gram_type='Bigram') -> None:
        self.n_gram_counts = self.countVectorizerToDict()
        if top_n is not None:
            return pd.DataFrame(sorted(self.n_gram_counts.items(),
                                       key=lambda item: item[1],
                                       reverse=True),
            columns=[n_gram_type, 'Count']).head(top_n)        

            
            
            
            
            
            