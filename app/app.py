"""Challenge: Implement a RESTful API using Python and any web framework of your choice (such as Flask, Django, or FastAPI) to manage a simple note-taking application.

Requirements:
1. The API should be able to perform basic CRUD operations (Create, Read, Update, Delete) on notes.
2. Notes can have a title and content.
3. Use proper HTTP status codes and response formats (e.g., JSON) for different operations.
4. Write appropriate unit tests for the API endpoints.
5. Implement authentication and authorization for the API endpoints, where users can only access and manage their own notes.
6. Implement pagination and sorting for retrieving a list of notes.
7. Provide API documentation specifying the available endpoints and their usage.
"""

from typing import Annotated
from fastapi import (
    Depends,
    FastAPI,
    HTTPException,
    status,
)
from fastapi.security import OAuth2PasswordBearer

from .models import (
    Note,
    NoteResponse,
    NoteSortingKeys,
)
from .data_manager import ListDataManager, NoteDataManager

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

dm = NoteDataManager()


def get_current_user() -> str:
    return 'current_user'


def add_owner_to_note(note: Note) -> dict:
    rnote = note.model_dump()
    rnote['owner'] = get_current_user()
    return rnote


def validate_index(note: dict) -> None:
    if note is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    if note['owner'] != get_current_user():
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized user.")


@app.get('/notes/{note_index}')
async def get_note(token: Annotated[str, Depends(oauth2_scheme)], note_index: int) -> NoteResponse:
    """Get a single note by index."""
    note = dm.get_note(note_index)
    validate_index(note)
    return note


@app.get('/notes/')
async def get_all_notes(token: Annotated[str, Depends(oauth2_scheme)],
                        first: int | None = None,
                        last: int | None = None,
                        sortkey: NoteSortingKeys | None = None,
                        reversesort: bool = False) -> list:
    """Get a list with all user's notes. Can be paginated with first and last. Can be serted by sortkey."""
    response = dm.get_notes_by_user(get_current_user())
    if sortkey is not None:
        response.sort(key=lambda x: x[sortkey], reverse=reversesort)
    return response[first:last]


@app.post('/notes/', status_code=status.HTTP_201_CREATED)
async def add_note(token: Annotated[str, Depends(oauth2_scheme)], note: Note) -> NoteResponse:
    """Create a new note."""
    return dm.add_note(add_owner_to_note(note))


@app.put('/notes/{note_index}')
async def update_note(token: Annotated[str, Depends(oauth2_scheme)], note: Note, note_index: int) -> NoteResponse:
    """Edit an existing note"""
    note = dm.get_note(note_index)
    validate_index(note)
    response = dm.update_note(note_index, add_owner_to_note(note))
    return response


@app.delete('/notes/{note_index}', status_code=status.HTTP_204_NO_CONTENT)
async def remove_note(token: Annotated[str, Depends(oauth2_scheme)], note_index: int):
    """Removes an existing note"""
    note = dm.get_note(note_index)
    validate_index(note)
    dm.delete_note(note_index)
