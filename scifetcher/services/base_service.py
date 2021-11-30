class BaseService:
    def fetch_data(self, query):
        """
        This method will save query and execute fetch data
        then it will return a list of Species
        """
        raise NotImplementedError
