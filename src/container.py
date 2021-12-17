import os

from src.data_access_layer.data_manager import DataManager
from src.data_access_layer.image_repository import S3ImageRepository
from src.interfaces.image_repository_interface import ImageRepositoryInterface


class Container:
    image_repository: ImageRepositoryInterface

    def __init__(self):
        if 'IN_MEMORY' in os.environ:
            from tests.unit import InMemorySqliteDataManager
            print('Creating an in memory mysql database')
            self.data_manager = InMemorySqliteDataManager()
        else:
            self.data_manager = DataManager()
        self.image_repository = S3ImageRepository()
