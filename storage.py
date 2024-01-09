from abc import ABC, abstractmethod
import config
import pymongo
from uuid import uuid4
from pathlib import Path
import json


class BaseStorage(ABC):
    @abstractmethod
    def create_book(self, book: dict):
        pass

    @abstractmethod
    def get_books(self, skip: int = 0, limit: int = 10, search_param: str = None):
        pass

    @abstractmethod
    def update_book(self, book_uuid: str, new_price: float):
        pass

    @abstractmethod
    def delete_book(self, book_uuid: str):
        pass


class JSONStorage(BaseStorage):

    def __init__(self):
        self.file_name = 'storage.json'

        my_file = Path(self.file_name)
        if not my_file.is_file():
            with open(self.file_name, 'w', encoding='utf-8') as file:
                json.dump([], file, indent=4)

    def create_book(self, book: dict):
        with open(self.file_name, 'r') as file:
            content: list[dict] = json.load(file)

        book['uuid'] = str(uuid4())
        content.append(book)
        with open(self.file_name, 'w', encoding='utf-8') as file:
            json.dump(content, file, indent=4)
        return book

    def get_books(self, skip: int = 0, limit: int = 10, search_param: str = None):
        with open(self.file_name, 'r') as file:
            content: list[dict] = json.load(file)

        if search_param:
            data = []
            for book in content:
                if search_param in book['title']:
                    data.append(book)
            return data[skip:][:limit]

        return content[skip:][:limit]

    def update_book(self, book_uuid: str, new_price: float):
        with open(self.file_name, 'r') as file:
            content: list[dict] = json.load(file)
        for book in content:
            if book['uuid'] == book_uuid:
                book['price'] = new_price
                break
        with open(self.file_name, 'w', encoding='utf-8') as file:
            json.dump(content, file, indent=4)

    def delete_book(self, book_uuid: str):
        with open(self.file_name, 'r') as file:
            content: list[dict] = json.load(file)
        for book in content:
            if book['uuid'] == book_uuid:
                content.remove(book)
                break
        with open(self.file_name, 'w', encoding='utf-8') as file:
            json.dump(content, file, indent=4)


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

    def get_books(self, skip: int = 0, limit: int = 10, search_param: str = None):
        query = {}
        if search_param:
            query = {'title': {'$regex': search_param.strip()}}
        return self.collection.find(query).skip(skip).limit(limit)

    def update_book(self, book_uuid: str, new_price: float):
        filter_data = {'uuid': book_uuid}
        new_data = {'$set': {'price': new_price}}
        processed = self.collection.update_one(filter_data, new_data)
        return processed

    def delete_book(self, book_uuid: str):
        filter_data = {'uuid': book_uuid}
        self.collection.delete_one(filter_data)


storage = JSONStorage()
