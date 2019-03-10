from abc import abstractmethod


class BaseLoader:
    """
    A Loader for one format of JSON file.
    """

    @abstractmethod
    def load(self, json: dict):
        """
        Loads a single JSON file into the database. The JSON file is passed in as a dictionary.
        """
        pass
