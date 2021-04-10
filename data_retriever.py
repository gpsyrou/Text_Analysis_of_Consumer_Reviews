
import os
import json
import pandas as pd
import argparse

project_dir = r'D:\GitHub\Projects\Analysis_of_Delivery_Companies_Reviews'
os.chdir(project_dir)

import trustplt as pilot

json_loc = 'config.json'

with open(json_loc, 'r') as json_file:
    config = json.load(json_file)
json_file.close()

starting_page = config['starting_page']
steps = config['steps']

source_url = 'https://uk.trustpilot.com'
# starting_page = '/review/www.deliveroo.co.uk'
landing_page = source_url + starting_page

processed_pages_file = os.path.join(project_dir, 'processed_pages.txt')
reviews_base_file = os.path.join(project_dir, 'output.csv')

company = 'Deliveroo'
col_names = ['Company', 'Id', 'Reviewer_Id', 'Title', 'Review', 'Date', 'Rating']
ratings_dict = {1: 'Bad', 2: 'Poor', 3: 'Average', 4: 'Great', 5: 'Excellent'}      

print('Starting retrieving data for {0}... \n'.format(company))
# company_url = '/review/www.deliveroo.co.uk?b=MTYxNDM2ODY0MDAwMHw2MDM5NGY4MGY4NWQ3NTA5ZDhlNWE1N2M'
base_df = pd.read_csv(reviews_base_file, sep=',')
print('Base file has {0} rows and {1} unique Ids \n\n'.format(base_df.shape[0], len(base_df['Id'].unique())))

new_reviews_df = pilot.trustPltSniffer(base_domain=source_url, starting_page=starting_page,
                      steps=steps, processed_urls_f=processed_pages_file,
                      ratings_dict=ratings_dict, col_names=col_names, company_name=company)

base_df_updated = pd.concat([base_df, new_reviews_df], axis=0)
print('Updated base file has {0} rows and {1} unique Ids \n\n'.format(base_df_updated.shape[0], len(base_df_updated['Id'].unique())))

base_df_updated.to_csv(reviews_base_file, sep=',', index=False)

print('Data retrieval for {0} finished...'.format(company))

config['starting_page'] = pilot.flushLastProcessedPage(processed_urls_f=processed_pages_file, company_name=company)

with open(json_loc, "w") as json_file:
    json.dump(config, json_file)
json_file.close()
