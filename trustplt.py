
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


def retrieve_next_page(reviews_html: BeautifulSoup) -> str:
    """
    Given a source_page as an html object, retrieve the url for the next page.
    """
    nav = reviews_html.find_all('nav', attrs={'class': 'pagination-container'})
    nav = nav[0].find_all('a', attrs={'class': 'button button--primary next-page'})
    next_page = re.findall(r'/review.+?(?=")', str(nav[0]))[0]
    if not next_page:
        raise NoDataRetrievedError
    else:
        return next_page


def extract_total_num_of_reviews(reviews_html: BeautifulSoup,
                                rvw_num_att='headline__review-count') -> int:
    
    rev_num_atr = reviews_html.find_all('span', attrs={'class': rvw_num_att})
    rev_num_atr = [span.get_text() for span in rev_num_atr][0].replace(',', '')
    
    return int(rev_num_atr)


def retrieve_reviews(reviews_html: BeautifulSoup,
                     rvw_section_att='review-card') -> element.ResultSet:
    """
    The function returns an element.ResultSet, where each element is a tag
    that contain all the information of the reviews. The ResultSet has a length
    of 20. A 'review-card' element corresponds to a separate review.
    """
    return reviews_html.find_all('div', attrs={'class': rvw_section_att})


def get_review_title(review: element.Tag,
                   rvw_title_att='review-content__title') -> str:
    title_obj = review.find_all('h2', attrs={'class': rvw_title_att})
    title = [obj.get_text() for obj in title_obj]
    if title:
        return title[0].strip()
    else:
        raise NoDataRetrievedError


def get_review_id(review: element.Tag,
                  rvw_userid_att='consumer-information') -> str:
    reviewer_id_obj = review.find_all('a', attrs={'class': rvw_userid_att})
    
    return reviewer_id_obj[0].get('href').replace('/users/', '')


def get_review_unique_id(review: element.Tag) -> str:
    review_id_obj = review.find_all('article', attrs={'class': 'review'})
    
    return review_id_obj[0].get('id')


def get_review_text(review: element.Tag,
                  rvw_text_att='review-content__text') -> str:
    text_obj = review.find_all('p', attrs={'class': rvw_text_att})
    text = [obj.get_text() for obj in text_obj]
    if text:
        return text[0].strip()
    else:
        pass


def get_review_rating(review: element.Tag,
                    ratings_dict: Mapping[int, str],
                    rvw_rating_att='star-rating star-rating--medium') -> dict:
    rating_obj = review.find_all('div', attrs={'class': rvw_rating_att})
    for div in rating_obj:
        img = div.find('img', alt=True)
        rating_str = img['alt']
    rating_str = {int(rating_str[0]):ratings_dict[int(rating_str[0])]}
    
    return rating_str


def get_review_datetime(review: element.Tag):
    """
    The function currently is extracting only the date not the time.
    """
    for parent in review.find_all('script'): 
        for child in parent.children:
            if 'publishedDate' in str(child):
                published_date = child.strip().split(',')[0][18:43]
                try:
                    published_date= isoparse(published_date)
                except ValueError:
                    return
    
    return published_date.strftime("%Y-%m-%d %H:%M")


def reviews_page_to_df(reviews: element.ResultSet,
                        ratings_dict: Mapping[int, str],
                        col_names: List['str'],
                        company_name: 'str') -> pd.core.frame.DataFrame:
    """
    Transform a single page of reviews into a pandas DataFrame. Columns are 
    following the order as defined in col_names.
    """
    company_name_ls = [company_name] * len(reviews)
    review_id_ls = []
    reviewer_id_ls = []
    title_ls = []
    text_ls = []
    datetime_ls = []
    ratings_ls = []
    
    for i in range(0, len(reviews)):
        review_id_ls.append(get_review_unique_id(reviews[i]))
        reviewer_id_ls.append(get_review_id(reviews[i]))
        title_ls.append(get_review_title(reviews[i]))
        text_ls.append(get_review_text(reviews[i]))
        datetime_ls.append(get_review_datetime(reviews[i]))
        ratings_ls.append(get_review_rating(reviews[i],
                                          ratings_dict=ratings_dict))

    reviews_df = pd.DataFrame(list(zip(company_name_ls,
                                       review_id_ls,
                                       reviewer_id_ls,
                                       title_ls,
                                       text_ls,
                                       datetime_ls,
                                       ratings_ls)), columns = col_names)
    return reviews_df


def trustplt_sniffer(base_domain: str,
                    starting_page: str,
                    steps: int,
                    processed_urls_f: str,
                    ratings_dict: Mapping[int, str],
                    col_names: List['str'],
                    company_name: 'str') -> pd.core.frame.DataFrame:
    """
    Generate a dataframe with the data retrieved from TrustPilot for a
    specified target 

    Parameters
    ----------
    base_domain: 
        Base domain path for the Trustpilot landing page
    starting_page: 
        Sub-domain path
    steps: 
        Number of pages to iterate with "starting_page" as starting point
    processed_urls: 
        Path to the .txt file that contains the already parsed URLs

    Returns
    --------
         A pandas dataframe object that contains the merged data retrieved by
         looping through different url pages.
    
    Notes
    -----
        The function checks processed_urls_f for subdomains that are already
        processed and it skips them if they are present in the .txt file. If
        not, then a new line is written in the .txt file to avoid re-processing
        in future iterations.
    """
    pages_ls = []
    landing_page = base_domain + starting_page
    processed_pages = retrieve_processed_pages(processed_urls_f)
    with open(processed_urls_f, 'a') as file:
        while steps != 0:
            reviews_page_html = reviews_page_to_html(landing_page)
            try:
                page = retrieve_next_page(reviews_page_html)
                print('processing: {0}'.format(page))
                reviews = retrieve_reviews(reviews_page_html)
                df = reviews_page_to_df(reviews,
                                            ratings_dict=ratings_dict,
                                            col_names=col_names,
                                            company_name=company_name)
                if page not in processed_pages:
                    print(page)
                    file.write(page +'\t' +
                            company_name +'\t' +  str(datetime.now()) + '\n')
                    pages_ls.append(df)
                landing_page = base_domain + page
                steps -= 1
                time.sleep(1)
            except IndexError as e:
                print(e)
                pass
    file.close()

    return pd.concat(pages_ls)

