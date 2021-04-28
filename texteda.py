"""
Package that contains a collection of function that can be used for generic
exploratory data analysis on text.
"""


from pandas import DataFrame
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
from wordcloud import WordCloud

def most_common_words(input_df:DataFrame,
                      text_col: str,
                      n_most_common=20):
    """
    Given a collection of documents as text, compute the number of most common
    words as defined by n_most_common.
    Args:
    ------
        input_df: Dataframe that contains the relevant text column
        text_col: Name of the column
        n_most_common: Number of most common words to calculate
    Returns:
    --------
        Pandas dataframe with two columns indicating a word and number
        of times (count) that it appears in the original input_df
    """
    word_list = list([x.split() for x in input_df[text_col] if x is not None])
    word_counter = Counter(x for xs in word_list for x in set(xs))
    word_counter.most_common(n_most_common)

    return DataFrame(word_counter.most_common(n_most_common),
                        columns=['words', 'count'])


def plot_most_common_words(input_df:DataFrame,
                           text_col: str,
                           n_most_common=20,
                           figsize=(10, 10)) -> None:

    fig, ax = plt.subplots(figsize=figsize)
    common_words_df = most_common_words(input_df=input_df,
                                        text_col=text_col,
                                        n_most_common=n_most_common)
    sns.barplot(x='count',
                y='words',
                data=common_words_df).set_title(f'Common Words Found - Overall', fontweight='bold')

    plt.grid(True, alpha=0.3, linestyle='-', color='black')
    plt.show()


def plot_wordcloud(input_df:DataFrame,
                   text_col: str,
                   figsize=(10, 10)) -> None:
    """
    Generate a WordCloud plot based on the number of occurenences of words
    in a set documents
    """
    plt.figure(figsize=figsize)
    gen_text = ' '.join([x for x in input_df[text_col] if x is not None])
    wordcloud = WordCloud().generate(gen_text)
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()
