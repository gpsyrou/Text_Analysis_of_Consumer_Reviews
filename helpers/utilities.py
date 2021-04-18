from typing import List

class NoDataRetrievedError(Exception):
    def __init__(self):
        self.msg = 'No data could be retrieved or field was empty'


def splitRatingsColumn(rating_text):
    rating_text = rating_text.replace('\'','').replace('{','').replace('}','')
    return rating_text[0], rating_text[3:]


def retrieveProcessedPages(input_file: str) -> List['str']:
    """
    Returns a list of all the links that are already processed.
    """
    with open(input_file, 'r') as file: 
        processed_pages = [line.split('\t')[0].strip() for line in file.readlines()]
        file.close()
    return processed_pages


def flushLastProcessedPage(processed_urls_f: str, company_name: str) -> 'str':
    """
    Read through 'processed_urls_f' and retrieve the last processed web url for
    a specific company.
    """
    with open(processed_urls_f, 'r') as file:
        lines = file.readlines()
        relevant_urls = []
        for line in lines:
            page_info = line.split('\t') 
            if page_info[1] == company_name:
                relevant_urls.append(page_info[0])
        relevant_urls.sort(key=lambda x: x[2])
        file.close()
    return relevant_urls[-1]
