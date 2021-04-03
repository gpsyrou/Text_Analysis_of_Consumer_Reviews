import pandas as pd
import urllib
import re
import dateutil.parser

from typing import List, Mapping

from bs4 import (BeautifulSoup,
                 element)
from helpers.utilities import NoDataRetrievedError


def reviewsPageToHTMLObject(target_url: str) -> BeautifulSoup:
    '''
    Given a website link (URL), retrieve the corresponding website in an html
    format.

    Parameters
    ----------
    target_url : str
        URL of the webpage that will be transformed to a HTML object.
    '''
    print('Attempting to retrieve HTML object for {0}'.format(target_url))
    request = urllib.request.urlopen(target_url)
    if request.getcode() != 200:
        raise Exception('Can not communicate with the client')        
    else:
        response = request.read()
        response_html = BeautifulSoup(response, 'html.parser')
        return response_html


def retrieveNextPage(reviews_html: BeautifulSoup) -> str:
    '''
    Given a source_page as an html object, retrieve the url for the next page.
    '''
    nav = reviews_html.find_all('nav', attrs={'class': 'pagination-container'})
    nav = nav[0].find_all('a', attrs={'class': 'button button--primary next-page'})
    next_page = re.findall(r'/review.+?(?=")', str(nav[0]))[0]
    if not next_page:
        raise NoDataRetrievedError
    else:
        return next_page


def extractTotalNumberOfReviews(reviews_html: BeautifulSoup,
                                review_count_att='headline__review-count') -> int:
    
    rev_count_atr = reviews_html.find_all('span',
                                          attrs={'class': review_count_att})
    rev_count_atr = [span.get_text() for span in rev_count_atr][0].replace(',', '')
    return int(rev_count_atr)


def retrieveReviews(reviews_html: BeautifulSoup,
                    review_section_att='review-card') -> element.ResultSet:
    '''
    The function returns an element.ResultSet, where each element is a tag
    that contain all the information of the reviews. The ResultSet has a length
    of 20. A 'review-card' element corresponds to a separate review.
    '''
    return reviews_html.find_all('div', attrs={'class': review_section_att})




def getReviewTitle(review: element.Tag,
                   title_att='review-content__title') -> str:
    title_obj = review.find_all('h2', attrs={'class': title_att})
    title = [obj.get_text() for obj in title_obj]
    if title:
        return title[0].strip()
    else:
        raise NoDataRetrievedError


def getReviewUniqueId(review: element.Tag) -> 'str':
    review = review.find_all('article', attrs={'class': 'review'})
    return review[0].get('id')



def getReviewText(review: element.Tag, text_att='review-content__text') -> str:
    text_obj = review.find_all('p', attrs={'class': text_att})
    text = [obj.get_text() for obj in text_obj]
    if text:
        return text[0].strip()
    else:
        pass


def getReviewRating(review: element.Tag,
                    ratings: Mapping[int, str],
                    rating_att='star-rating star-rating--medium'
                    ) -> dict:
    rating_obj = review.find_all('div', attrs={'class': rating_att})
    for div in rating_obj:
        img = div.find('img', alt=True)
        rating_str = img['alt']
    rating_str = {int(rating_str[0]):ratings[int(rating_str[0])]}
    return rating_str


def getReviewDateTime(review: element.Tag):
    '''
    The function currently is extracting only the date not the time.
    '''
    for parent in review.find_all('script'): 
        for child in parent.children:
            if 'publishedDate' in str(child):
                published_date = child.strip().split(',')[0][18:43]
                published_date= dateutil.parser.isoparse(published_date)
    return published_date.strftime("%Y-%m-%d %H:%M")


def reviewsPageToDataFrame(reviews: element.ResultSet,
                           ratings: Mapping[int, str],
                           colnames: List['str']) -> pd.core.frame.DataFrame:
    '''
    Transform a single page of reviews into a pandas DataFrame. Columns are 
    following the order as defined in col_names.
    '''
    id_ls = []
    title_ls = []
    text_ls = []
    datetime_ls = []
    ratings_ls = []
    
    for i in range(0, len(reviews)):
        id_ls.append(getReviewUniqueId(reviews[i]))
        title_ls.append(getReviewTitle(reviews[i]))
        text_ls.append(getReviewText(reviews[i]))
        datetime_ls.append(getReviewDateTime(reviews[i]))
        ratings_ls.append(getReviewRating(reviews[i], ratings=ratings))

    reviews_df = pd.DataFrame(list(zip(id_ls, title_ls, text_ls, datetime_ls,
                                   ratings_ls)), columns = colnames)

    return reviews_df
