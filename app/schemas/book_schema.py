from pydantic import BaseModel

class BookBase(BaseModel):
   title: str
   author: str
   year: int

class BookCreate(BookBase):
    pass

class BookOut(BookBase):
    id: int
