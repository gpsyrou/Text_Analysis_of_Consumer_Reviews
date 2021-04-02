
class NoDataRetrievedError(Exception):
    def __init__(self):
        self.msg = 'No data could be retrieved or field was empty'
