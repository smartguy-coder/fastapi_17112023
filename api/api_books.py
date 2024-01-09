from fastapi import APIRouter, status
from pydantic import BaseModel, Field
import constants
from storage import storage

router = APIRouter(
    prefix='/api/books',
    tags=['API', 'Books'],
)


class NewBookData(BaseModel):
    title: str = Field(min_length=3, examples=['I, legend'])
    author: str
    price: float = Field(default=0.01, gt=0.0)
    cover: str
    tags: list[constants.Genres] = Field(default=[], max_items=2)
    description: str = None


class SavedBook(NewBookData):
    uuid: str = Field(examples=['28a118b0-0e13-4395-9293-f954a411bc0f'])


@router.post('/create', status_code=status.HTTP_201_CREATED)
def create_book(book: NewBookData) -> SavedBook:
    saved_book = storage.create_book(book.model_dump())
    return saved_book


@router.get('/')
def get_books(search_param: str = None, skip: int = 0, limit: int = 10) -> list[SavedBook]:
    books = storage.get_books(skip, limit, search_param)
    result = []

    for book in books:
        instance = SavedBook(
            **{'title': book['title'], 'author': book['author'], 'price': book['price'], 'cover': book['cover'],
               'tags': book['tags'], 'description': book['description'], 'uuid': book['uuid']})

        result.append(instance)
    return result


@router.patch('/update/{book_id}')
def update_book(book_id: str, price: float = 100.00):
    storage.update_book(book_id, price)
    return {'result': 'OK'}


@router.delete('/delete/{book_id}')
def delete_book(book_id: str):
    storage.delete_book(book_id)
    return {'deleted': True}
