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
def get_books() -> list[dict]:
    return [{'title': 'NINE', 'pages': 100}]


@router.get('/')
def get_books_by_name() -> list[dict]:
    return [{'title': 'NINE', 'pages': 100}]


@router.put('/update/{book_id}')
def update_book():
    pass


@router.delete('/delete/{book_id}')
def delete_book():
    pass
