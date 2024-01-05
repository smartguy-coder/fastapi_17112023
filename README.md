# fastapi_17112023

poetry config --local virtualenvs.in-project true
poetry init   
poetry init -n

poetry add fastapi[all]
poetry add "fastapi[all]"
 poetry add pytest --dev 

 uvicorn main:app  
uvicorn main:app --port 9000 --reload 

