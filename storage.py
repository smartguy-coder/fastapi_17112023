from abc import ABC, abstractmethod
import config
import pymongo
from uuid import uuid4


class BaseStorage(ABC):
    @abstractmethod
    def create_book(self, book: dict):
        pass

    @abstractmethod
    def get_books(self):
        pass

    @abstractmethod
    def get_books_by_name(self):
        pass

    @abstractmethod
    def update_book(self):
        pass

    @abstractmethod
    def delete_book(self):
        pass


class MongoStorage(BaseStorage):
    def __init__(self):

        url = 'mongodb+srv://{user}:{password}@cluster0.buyf0ko.mongodb.net/?retryWrites=true&w=majority' \
            .format(
                user=config.USER,
                password=config.PASSWORD,
            )

        client = pymongo.MongoClient(url)
        db = client['books']
        self.collection = db['books']

    def create_book(self, book: dict) -> dict:
        book['uuid'] = str(uuid4())
        self.collection.insert_one(book)
        return book

    def get_books(self):
        raise NotImplemented

    def get_books_by_name(self):
        raise NotImplemented

    def update_book(self):
        raise NotImplemented

    def delete_book(self):
        raise NotImplemented


storage = MongoStorage()
