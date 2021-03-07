import pandas as pd
import numpy as np
import requests

from bs4 import BeautifulSoup
import time
import json

import lxml.html as html


target_url = 'https://uk.trustpilot.com/review/www.deliveroo.co.uk'
request = requests.get(url=target_url, verify=False)
page_content = request.content

tree = html.fromstring(page_content)

ratingCount = tree.xpath('//span[@class="headline__review-count"]')
ratingCount = int(ratingCount[0].text.replace(',',''))

def getOverallRatingCount():
    
    totalNumberOfReviews =     