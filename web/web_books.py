from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

from storage import storage

templates = Jinja2Templates(directory='templates')

router = APIRouter(
    prefix='',
    tags=['WEB', 'Books'],
)


@router.get('/')
def index(request: Request):
    books = storage.get_books(0, limit=10)
    context = {
        'request': request,
        'page': 'page 1',
        'title': 'first page',
        'books': books
    }

    return templates.TemplateResponse('index.html', context=context)

@router.get('/second')
def index(request: Request):
    context = {
        'request': request,
        'page': 'page 2',
        'title': 'first second'
    }

    return templates.TemplateResponse('index.html', context=context)
