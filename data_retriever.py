
import os
import json
import pandas as pd

project_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(project_dir)

import trustplt as pilot
from helpers.utilities import flust_last_processed_page

json_loc = 'config.json'

with open(json_loc, 'r') as json_file:
    config = json.load(json_file)
json_file.close()

company = config['company']
starting_page = config['starting_page']
steps = config['steps']

source_url = config['source_url']
landing_page = source_url + starting_page

processed_pages_fp = os.path.join(project_dir, 'processed_pages.txt')
reviews_base_fp = os.path.join(project_dir, 'reviews.csv')

col_n = ['Company', 'Id', 'Reviewer_Id', 'Title', 'Review', 'Date', 'Rating']
ratings_dict = {1: 'Bad', 2: 'Poor', 3: 'Average', 4: 'Great', 5: 'Excellent'}      

print('Starting retrieving data for {0}... \n'.format(company))

base_df = pd.read_csv(reviews_base_fp, sep=',')
print('Base file has {0} rows and {1} unique Ids \n\n'.format(base_df.shape[0],
      len(base_df['Id'].unique())))

new_reviews_df = pilot.trustplt_sniffer(base_domain=source_url,
                                       starting_page=starting_page,
                                       steps=steps,
                                       processed_urls_f=processed_pages_fp,
                                       ratings_dict=ratings_dict,
                                       col_names=col_n,
                                       company_name=company)

base_df_updated = pd.concat([base_df, new_reviews_df], axis=0)

print('Updated base file has {0} rows and {1} unique Ids \n\n'.format(base_df_updated.shape[0],
      len(base_df_updated['Id'].unique())))

base_df_updated.to_csv(reviews_base_fp, sep=',', index=False)

print('Data retrieval for {0} finished...'.format(company))

config['starting_page'] = flust_last_processed_page(processed_urls_f=processed_pages_fp, company_name=company)

with open(json_loc, 'w') as json_file:
    json.dump(config, json_file)
json_file.close()
