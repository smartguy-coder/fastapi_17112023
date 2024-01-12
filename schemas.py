from pydantic import BaseModel, Field
import constants


class NewBookData(BaseModel):
    title: str = Field(min_length=3, examples=['I, legend'])
    author: str
    price: float = Field(default=0.01, gt=0.0)
    cover: str
    tags: list[constants.Genres] = Field(default=[], max_items=2)
    description: str = None


class SavedBook(NewBookData):
    uuid: str = Field(examples=['28a118b0-0e13-4395-9293-f954a411bc0f'])
