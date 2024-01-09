from fastapi import FastAPI
from api import api_books
from web import web_books

app = FastAPI()
app.include_router(api_books.router)
app.include_router(web_books.router)


# @app.get('/')
# def root() -> dict:
#     return {'try': 'OK', 'count': 10}


if __name__ == '__main__':
    import uvicorn
    uvicorn.run('main:app', reload=True, host='0.0.0.0', port=8666)
