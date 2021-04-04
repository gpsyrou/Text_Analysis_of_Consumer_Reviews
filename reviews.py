
import os
import pandas as pd
from typing import List
from datetime import datetime

project_dir = r'D:\GitHub\Projects\Analysis_of_Delivery_Companies_Reviews'
os.chdir(project_dir)

from helpers.utilities import processedPages, NoDataRetrievedError
import trustplt as pilot


col_names = ['Id', 'Title', 'Review', 'Date', 'Rating']
ratings_dict = {1: 'Bad', 2: 'Poor', 3: 'Average', 4: 'Great', 5: 'Excellent'}      
processed_pages_file = os.path.join(project_dir, 'processed_pages.txt')

source_url = 'https://uk.trustpilot.com'
company_url = '/review/www.deliveroo.co.uk'
landing_page = source_url + company_url





processedPages(input_file=processed_pages_file)
t = pilot.trustPltSniffer(base_domain=source_url, starting_page=company_url,
                      steps=7, processed_urls_f=processed_pages_file,
                      ratings_dict=ratings_dict, col_names=col_names)
