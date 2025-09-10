from typing import List
from fastapi import APIRouter, HTTPException
from sqlmodel import select

from comic_splitter.db.models import BookPublic, BookCreate, Book
from comic_splitter.server import SessionDep

router = APIRouter(prefix='/books', tags=['Books'])


@router.post('/', response_model=BookPublic)
def create_book(book: BookCreate, session: SessionDep):
    db_book = Book.model_validate(book)
    session.add(db_book)
    session.commit()
    session.refresh(db_book)
    return db_book


@router.get('/{book_id}', response_model=BookPublic)
def get_books(book_id: int, session: SessionDep) -> Book:
    book = session.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@router.get(
    '/author/{author_id}',
    response_model=List[BookPublic],
    summary="Get all books by a specific author"
)
def get_author_books(
        author_id: int, session: SessionDep):

    select_author_books_query = select(Book).where(Book.author_id == author_id)
    author_books = session.exec(select_author_books_query).all()
    if not author_books:
        raise HTTPException(
            status_code=404, detail="No books for this specified author")
    return author_books


@router.get(
    '/series/{series_id}',
    response_model=list[BookPublic],
    summary='Get all books in a series'
)
def get_series_books(series_id: int, session: SessionDep):
    books_in_series_query = select(Book).where(Book.series_id == series_id)
    series_books = session.exec(books_in_series_query).all()
    if not series_books:
        raise HTTPException(
            status_code=404, detail="No books in this specified series")
    return series_books


@router.delete('/{book_id}')
def delete_book(book_id: int, session: SessionDep):
    book = session.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Author not found")
    session.delete(book)
    session.commit()
    return {'ok': True}
