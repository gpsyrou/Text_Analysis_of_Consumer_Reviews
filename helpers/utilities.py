from typing import List

class NoDataRetrievedError(Exception):
    def __init__(self):
        self.msg = 'No data could be retrieved or field was empty'


def retrieveProcessedPages(input_file: str) -> List['str']:
    """
    Returns a list of all the links that are already processed.
    """
    with open(input_file, 'r') as file: 
        processed_pages = [line.split('\t')[0].strip() for line in file.readlines()]
        file.close()
    return processed_pages
