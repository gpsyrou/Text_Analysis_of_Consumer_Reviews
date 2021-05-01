"""
Package that contains a collection of function that can be used for generic
exploratory data analysis on text.
"""

import matplotlib.pyplot as plt
from pandas import DataFrame
from seaborn import barplot
from wordcloud import WordCloud
from collections import Counter
from nltk.collocations import BigramCollocationFinder
from nltk import word_tokenize


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
    barplot(x='count',
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
    combined_text = ' '.join([x for x in input_df[text_col] if x is not None])
    wordcloud = WordCloud().generate(combined_text)
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()


def compute_bigrams(input_df:DataFrame,
                    text_col: str) -> dict:
    """
    Calculate the number of occurences that a pair of words appear next to
    each other, and return a dictionary of pair of words - count.
    """
    combined_text = ' '.join([x for x in input_df[text_col]])

    finder = BigramCollocationFinder.from_words(word_tokenize(combined_text))

    bigrams_dict = {}
    for k, v in finder.ngram_fd.items():
        # Condition to avoid characters like '@' and '#'
        if len(k[0]) > 1 and len(k[1]) > 1 and "'s" not in k:
            bigrams_dict[k] = v
        else:
            continue
    return bigrams_dict


def plot_bigrams(input_df:DataFrame,
                 text_col: str,
                 top_n: int,
                 figsize=(10, 8)) -> None:

    bigrams_dict = compute_bigrams(input_df=input_df, text_col=text_col)
    bigrams_sorted = sorted(bigrams_dict.items(),
                            key=lambda x: x[1],
                            reverse=True)[0:top_n]

    bgram, counts = list(zip(*bigrams_sorted))
    bgstring = list(map(lambda txt: '-'.join(txt), bgram))

    plt.figure(figsize=figsize)
    g = barplot(bgstring, counts, palette='muted')
    g.set_xticklabels(g.get_xticklabels(), rotation=80)
    plt.title(f'Top-{top_n} pairs of words that appear next to each other',
              fontweight='bold')
    plt.ylabel('Count')
    plt.grid(True, alpha=0.1, color='black')
    plt.show()  

