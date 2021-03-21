import pandas as pd
import numpy as np
import requests

from bs4 import BeautifulSoup

import urllib

target_url = 'https://uk.trustpilot.com/review/www.deliveroo.co.uk/fufu'


reponse_html.find_all("div", {"class": "headline__review-count"})



def getHTMLObject(target_url: str):
    '''
    Given a website link (URL), retrieve the corresponding website in an html
    format.

    Parameters
    ----------
    target_url : str
        URL of the webpage that will be transformed to a HTML object.
    '''
    print('Attempting to retrieve HTML object for {0}'.format(target_url))
    request = urllib.request.urlopen(target_url)
    if request.getcode() != 200:
        raise Exception('Can not communicate with the client')        
    else:
        response = request.read()
        response_html = BeautifulSoup(response, 'html.parser')
        return response_html
        

test_html = getHTMLObject(target_url)
print(test_html.prettify())


