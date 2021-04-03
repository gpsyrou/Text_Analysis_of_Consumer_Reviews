
import os
import pandas as pd
from typing import List

project_dir = r'D:\GitHub\Projects\Analysis_of_Delivery_Companies_Reviews'
os.chdir(project_dir)

from helpers.utilities import NoDataRetrievedError
import trustplt as tp

col_names = ['Id', 'Title', 'Review', 'Date', 'Rating']
ratings_dict = {1: 'Bad', 2: 'Poor', 3: 'Average', 4: 'Great', 5: 'Excellent'}      
processed_pages_file = os.path.join(project_dir, 'processed_pages.txt')

source_url = 'https://uk.trustpilot.com'
company_url = '/review/www.deliveroo.co.uk'
landing_page = source_url + company_url




def processedPagesList(input_file: str) -> List['str']:
    '''
    Returns a list of all the links that are already processed.
    '''
    with open(input_file, 'r') as file: 
        file_content = [line.strip() for line in file.readlines()]
        file.close()
    return file_content


def retrieveDataFromSource(input_file: str, source: str, starting_page: str,
                           steps: int) -> pd.core.frame.DataFrame:
    '''
    '''
    all_res = []
    landing_page = source + starting_page
    file_content = processedPagesList(input_file)
    
    with open(input_file, 'a') as file:
        for i in range(0, steps):
            reviews_page_html = tp.reviewsPageToHTMLObject(landing_page)
            page = tp.retrieveNextPage(reviews_page_html)
            reviews = tp.retrieveReviews(reviews_page_html)
            df = tp.reviewsPageToDataFrame(reviews, ratings=ratings_dict,
                                           colnames=col_names)
            if page not in file_content:
                print(page)
                file.write(page + '\n')
                all_res.append(df)
            landing_page = source_url + page
    file.close()
    data = pd.concat(all_res)
        
    return data

test_url = '/review/www.deliveroo.co.uk?b=MTYxNjc3MjYzNzAwMHw2MDVkZmUxZGY4NWQ3NTA4NzAzNmRhN2Q'

processedPagesList(input_file=processed_pages_file)
t = retrieveDataFromSource(input_file=processed_pages_file, source=source_url,
                       starting_page=company_url, steps=6)