
import os
import pandas as pd
from typing import List
from datetime import datetime 

project_dir = r'D:\GitHub\Projects\Analysis_of_Delivery_Companies_Reviews'
os.chdir(project_dir)

from helpers.utilities import retrieveProcessedPages, NoDataRetrievedError
import trustplt as pilot


col_names = ['Company', 'Id', 'Reviewer_Id', 'Title', 'Review', 'Date', 'Rating']
ratings_dict = {1: 'Bad', 2: 'Poor', 3: 'Average', 4: 'Great', 5: 'Excellent'}      
processed_pages_file = os.path.join(project_dir, 'processed_pages.txt')
reviews_base_file = os.path.join(project_dir, 'output.csv')

source_url = 'https://uk.trustpilot.com'
company_url = '/review/www.deliveroo.co.uk'
landing_page = source_url + company_url
company = 'Deliveroo'

base_df = pd.read_csv(reviews_base_file, sep=',')
print('Base file has {0} rows and {1} unique Ids'.format(base_df.shape[0], len(base_df['Id'].unique())))

new_reviews_df = pilot.trustPltSniffer(base_domain=source_url, starting_page=company_url,
                      steps=20, processed_urls_f=processed_pages_file,
                      ratings_dict=ratings_dict, col_names=col_names, company_name=company)

base_df_updated = pd.concat([base_df, new_reviews_df], axis=0)
print('Updated base file has {0} rows and {1} unique Ids'.format(base_df_updated.shape[0], len(base_df_updated['Id'].unique())))

base_df_updated.to_csv(reviews_base_file, sep=',', index=False)
