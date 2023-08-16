from enum import Enum
from pydantic import BaseModel


class User(BaseModel):
    name: str


class Note(BaseModel):
    title: str
    content: str


class NoteResponse(Note):
    index: int | None = None
    owner: str | None = None


class NoteSortingKeys(str, Enum):
    TITLE = 'title'
    CONTENT = 'content'




