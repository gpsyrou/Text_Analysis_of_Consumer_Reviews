import pandas as pd
import urllib.request
import time
import re
from dateutil.parser import isoparse
from datetime import datetime
from typing import List, Mapping
from bs4 import (BeautifulSoup,
                 element)

from helpers.utilities import retrieve_processed_pages, NoDataRetrievedError



def retrieve_reviews(reviews_html: BeautifulSoup,
                     rvw_section_att='typography_typography__QgicV typography_body__9UBeQ typography_color-black__5LYEn typography_weight-regular__TWEnf typography_fontstyle-normal__kHyN3') -> element.ResultSet:
    """
    The function returns an element.ResultSet, where each element is a tag
    that contain all the information of the reviews. The ResultSet has a length
    of 20. A 'review-card' element corresponds to a separate review.
    """
    return reviews_html.find_all('div', attrs={'class': rvw_section_att})

def reviews_page_to_html(target_url: str) -> BeautifulSoup:
    """
    Given a website link (URL), retrieve the corresponding website in an html
    format.

    Parameters
    ----------
    target_url : str
        URL of the webpage that will be transformed to a HTML object.
    """
    #print('Attempting to retrieve HTML object for {0}'.format(target_url))
    request = urllib.request.urlopen(target_url)
    if request.getcode() != 200:
        raise Exception('Can not communicate with the client')        
    else:
        response = request.read()
        response_html = BeautifulSoup(response, 'html.parser')
        return response_html

page = 'https://uk.trustpilot.com/review/www.deliveroo.co.uk'

page_html = reviews_page_to_html(page)
retrieve_reviews(page_html)



nav = page_html.find_all('div', attrs={'class': 'styles_mainContent__nFxAv'})

nav = nav[0].find_all('section', attrs={'class': 'styles_reviewsContainer__3_GQw'})

nav[0].fina_all('div', attrs={'class': "paper_paper__1PY90 paper_square__lJX8a card_card__lQWDv card_noPadding__D8PcU styles_cardWrapper__772_o styles_show__FYIO3 styles_reviewCard__9HxJJ"})