from fastapi import APIRouter, Request, Form, Response
from fastapi.templating import Jinja2Templates
from schemas import NewBookData, SavedBook


from storage import storage

templates = Jinja2Templates(directory='templates')

router = APIRouter(
    prefix='',
    tags=['WEB', 'Books'],
)


@router.get('/')
@router.post('/')
def main_books(request: Request, search_param: str = Form(None)):
    book_uuid = request.cookies.get('book')
    previous = storage.get_book_info(book_uuid=book_uuid) if book_uuid else None

    if search_param:
        books = storage.get_books(search_param=search_param)
    else:
        books = storage.get_books(0, limit=10)

    context = {
        'request': request,
        'title': 'Результати пошуку' if search_param else 'Головна сторінка',
        'books': books,
        'previous': previous,
    }
    return templates.TemplateResponse('index.html', context=context)


@router.get('/arriving_schema')
def arriving_schema(request: Request):
    context = {
        'request': request,
        'title': 'Схема проїзду',
    }
    return templates.TemplateResponse('arriving_schema.html', context=context)


@router.get('/add_book')
def add_book_form(request: Request):
    context = {
        'request': request,
        'title': 'Створити нову книгу',
        'text_min_length': 3,
    }
    return templates.TemplateResponse('new_book.html', context=context)


@router.post('/add_book')
def add_book(
        request: Request,
        title: str = Form(),
        author: str = Form(),
        price: float = Form(None),
        cover: str = Form(),
        description: str = Form(),
):
    book = NewBookData(
        title=title,
        author=author,
        price=price,
        cover=cover,
        description=description,
    )
    saved_book = storage.create_book(book.model_dump())
    context = {
        'request': request,
        'title': 'Нова книга',
        'books': [saved_book],

    }
    return templates.TemplateResponse('index.html', context=context)


@router.get('/book/{book_uuid}')
def book_info(request: Request, book_uuid: str):
    saved_book = storage.get_book_info(book_uuid)
    if saved_book:
        context = {
            'request': request,
            'title': f'Інформація про книгу {saved_book["title"]}',
            'book': saved_book,
        }
        response = templates.TemplateResponse('details.html', context=context)
        response.set_cookie(key='book', value=book_uuid)
        return response

    context = {
        'request': request,
        'title': f'Інформація про книгу {book_uuid} не знайдено',
        'book': saved_book,
    }
    return templates.TemplateResponse('http404.html', context=context)

