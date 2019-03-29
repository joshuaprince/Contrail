from loader.loaders import BaseLoader, register_loader
from loader.warehouse import db


# Uncomment the "@" line below to activate your loader.
#       Be sure to change the `provider` argument to either your own subclass of BaseProvider,
#       or the folder name in S3 whose files should use this loader.
# @register_loader(provider='ExampleProvider')
class ExampleLoader(BaseLoader):
    @classmethod
    def load(cls, filename: str, json: dict):
        # Write your own loading logic here.
        # The parsed file being loaded is located in `json` as a dictionary.
        db.insert([])