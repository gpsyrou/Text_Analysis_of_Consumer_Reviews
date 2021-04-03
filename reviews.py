
import os
import pandas as pd

project_dir = r'D:\GitHub\Projects\Analysis_of_Delivery_Companies_Reviews'
os.chdir(project_dir)

from helpers.utilities import NoDataRetrievedError
import trustplt as tp


col_names = ['Id', 'Title', 'Review', 'Date', 'Rating']
ratings_dict = {1: 'Bad', 2: 'Poor', 3: 'Average', 4: 'Great', 5: 'Excellent'}      

source_url = 'https://uk.trustpilot.com'
company_url = '/review/www.deliveroo.co.uk'
landing_page = source_url + company_url

all_res = []

for i in range(0, 5):
    reviews_page_html = tp.reviewsPageToHTMLObject(landing_page)
    page = tp.retrieveNextPage(reviews_page_html)
    reviews = tp.retrieveReviews(reviews_page_html)
    df = tp.reviewsPageToDataFrame(reviews, ratings=ratings_dict,
                                   colnames=col_names)
    print(page)
    landing_page = source_url + page
    all_res.append(df)

df_res = pd.concat(all_res)


