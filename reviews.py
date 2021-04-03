
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


all_res = []

def parsedPagesList(filename: str) -> List['str']:
    '''
    Returns a list of all the links that are already processed.
    '''
    with open(processed_pages_file, 'r') as file: 
        file_content = [line.strip() for line in file.readlines()]
        file.close()
    return file_content


with open(processed_pages_file, 'w') as file:
    file_content = parsedPagesList(filename=processed_pages_file)
    for i in range(0, 11):
        reviews_page_html = tp.reviewsPageToHTMLObject(landing_page)
        page = tp.retrieveNextPage(reviews_page_html)
        reviews = tp.retrieveReviews(reviews_page_html)
        temp_df = tp.reviewsPageToDataFrame(reviews, ratings=ratings_dict,
                                       colnames=col_names)
        if page not in file_content:
            print(page)
            file.write(page + '\n')
            all_res.append(temp_df)
            
        landing_page = source_url + page
        
    df_merged = pd.concat(all_res)
    file.close()
