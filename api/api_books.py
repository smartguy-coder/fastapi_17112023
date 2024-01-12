from fastapi import APIRouter, status, Response

from storage import storage
from schemas import NewBookData, SavedBook

router = APIRouter(
    prefix='/api/books',
    tags=['API', 'Books'],
)


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
def update_book(response: Response, book_id: str, price: float = 100.00):
    storage.update_book(book_id, price)
    response.set_cookie(key='ddd', value='dfgdgdgfdgfdgdgddfdgdg')
    return {'result': 'OK'}


@router.delete('/delete/{book_id}')
def delete_book(book_id: str):
    storage.delete_book(book_id)
    return {'deleted': True}











# from enum import Enum
#
#
# class Genres(str, Enum):
#     SIFY = 'since fiction'
#     DRAMA = 'drama'
#     FANTASY = 'fantasy'
#
#
#
#
# class Creator(BaseModel):
#     person: list[str] = Field(examples=[['Spielberg', 'Gates']])
#
#
# class CreatedBy(BaseModel):
#     director: list[Creator] = Field(examples=[['Spielberg', 'Gates']])
#     producer: list[Creator] = Field(examples=[['Spielberg', 'Gates']])
#     scriptwriter: list[Creator] = Field(examples=[['Spielberg', 'Gates']])
#
#
# class FilmData(BaseModel):
#
#     title: str = Field(examples=['Good Movie'])
#     genres: list[Genres] = Field(default=[])
#     created_by: CreatedBy # = Field(default={})
#     cast: list[str]
#     duration: int = Field(gt=1, default=1)
#     description: str = None
#     tags: list = Field(default=[], max_items=5)
#
#
#
#
#
#
#
# @router.post('/fake')
# def ffffffffffffff(film: FilmData):
#     return {}

# {
#   "title": "Good Movie",
#   "genres": [],
#   "created_by": {
#     "director": [
#       "Spielberg",
#       "Gates"
#     ],
#     "producer": [
#       "Spielberg",
#       "Gates"
#     ],
#     "scriptwriter": [
#       "Spielberg",
#       "Gates"
#     ]
#   },
#   "cast": [
#     "string"
#   ],
#   "duration": 1,
#   "description": "string",
#   "tags": []
# }