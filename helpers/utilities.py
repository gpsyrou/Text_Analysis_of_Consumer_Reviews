from typing import List


class NoDataRetrievedError(Exception):
    def __init__(self):
        self.msg = 'No data could be retrieved or field was empty'


def split_ratings_col(rating_text):
    rating_text = rating_text.replace('\'','').replace('{','').replace('}','')
    return rating_text[0], rating_text[3:]


def retrieve_processed_pages(input_file: str) -> List['str']:
    """
    Returns a list of all the links that are already processed.
    """
    with open(input_file, 'r') as file: 
        processed_pages = [line.split('\t')[0].strip() for
                           line in file.readlines()]
        file.close()
    return processed_pages


def flust_last_processed_page(processed_urls_f: str,
                           company_name: str) -> 'str':
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


def get_ratings_mapping():
    return {1: 'Bad', 2: 'Poor', 3: 'Average', 4: 'Great', 5: 'Excellent'}      

