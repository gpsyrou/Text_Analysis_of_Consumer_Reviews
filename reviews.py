import pandas as pd
import numpy as np
import requests

from bs4 import (BeautifulSoup,
                 element)

import urllib

target_url = 'https://uk.trustpilot.com/review/www.deliveroo.co.uk'


def getHTMLObject(target_url: str) -> BeautifulSoup:
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

      
test_html = getHTMLObject(target_url)


def extractTotalNumberOfReviews(reviews_html: BeautifulSoup,
                                review_count_att='headline__review-count') -> int:
    
    rev_count_atr = reviews_html.find_all('span', attrs={'class': review_count_att})
    rev_count_atr = [span.get_text() for span in rev_count_atr][0].replace(',', '')
    return int(rev_count_atr)


def retrieveReviews(reviews_html: BeautifulSoup,
                    review_section_att='review-card') -> element.ResultSet:
    '''
    The function returns an element.ResultSet, where each element is a tag
    that contain all the information of the reviews. The ResultSet has a length
    of 20.
    '''
    return reviews_html.find_all('div', attrs='review-card')


test = retrieveReviews(test_html)

