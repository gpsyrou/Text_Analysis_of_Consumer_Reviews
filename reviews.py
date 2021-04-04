
import os
import pandas as pd
from typing import List
from datetime import datetime

project_dir = r'D:\GitHub\Projects\Analysis_of_Delivery_Companies_Reviews'
os.chdir(project_dir)

from helpers.utilities import NoDataRetrievedError
import trustplt as pilot

col_names = ['Id', 'Title', 'Review', 'Date', 'Rating']
ratings_dict = {1: 'Bad', 2: 'Poor', 3: 'Average', 4: 'Great', 5: 'Excellent'}      
processed_pages_file = os.path.join(project_dir, 'processed_pages.txt')

source_url = 'https://uk.trustpilot.com'
company_url = '/review/www.deliveroo.co.uk'
landing_page = source_url + company_url




def processedPages(input_file: str) -> List['str']:
    """
    Returns a list of all the links that are already processed.
    """
    with open(input_file, 'r') as file: 
        file_content = [line.split('\t')[0].strip() for line in file.readlines()]
        file.close()
    return file_content


def trustPltSniffer(base_domain: str, starting_page: str, steps: int,
                    processed_urls_f: str) -> pd.core.frame.DataFrame:
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
    merged_data_df:
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
    file_content = processedPages(processed_urls_f)
    
    with open(processed_urls_f, 'a') as file:
        for i in range(0, steps):
            reviews_page_html = pilot.reviewsPageToHTMLObject(landing_page)
            page = pilot.retrieveNextPage(reviews_page_html)
            reviews = pilot.retrieveReviews(reviews_page_html)
            df = pilot.reviewsPageToDataFrame(reviews, ratings=ratings_dict,
                                           colnames=col_names)
            if page not in file_content:
                print(page)
                file.write(page +'\t' + str(datetime.now()) + '\n')
                pages_ls.append(df)
            landing_page = source_url + page
    file.close()
    merged_data_df = pd.concat(pages_ls)
        
    return merged_data_df

processedPages(input_file=processed_pages_file)
t = trustPltSniffer(base_domain=source_url, starting_page=company_url, steps=6, processed_urls_f=processed_pages_file)