from typing import List
from fastapi import APIRouter, HTTPException
from sqlmodel import select

from comic_splitter.db.models import BookPublic, BookCreate, Book, Author, Page, Panel, Series
from comic_splitter.server import SessionDep

router = APIRouter(prefix='/books', tags=['Books'])


@router.post('/', response_model=BookPublic)
def create_book(book: BookCreate, session: SessionDep):
    author = session.exec(
        select(Author).where(Author.name == book.author_name)).first()

    if author is None:
        author = Author(name=book.author_name)
        session.add(author)
        session.flush()

    book_series_id = None
    if book.series_title:
        series = session.exec(
            select(Series).where(Series.title == book.series_title)).first()
        if series is None:
            series = Series(title=book.series_title, author_id=author.id)
            session.add(series)
            session.flush()
        else:
            if series.author_id != author.id:
                raise HTTPException(
                    status_code=400,
                    detail=f"Series '{book.series_title}'"
                           "belongs to different author"
                )
        book_series_id = series.id

    db_book = Book(
        title=book.title,
        entry_number=int(book.entry_number) if book.entry_number else None,
        author_id=author.id,
        series_id=book_series_id,
    )
    session.add(db_book)
    session.flush()

    if book.pages:
        for page_data in book.pages:
            db_page = Page(book_id=db_book.id,
                           page_number=page_data.page_number)
            session.add(db_page)
            session.flush()
            if page_data.panels:
                for panel in page_data.panels:

                    db_panel = Panel(page_id=db_page.id, x=panel.x, y=panel.y,
                                     width=panel.width, height=panel.height,
                                     ltr_idx=panel.ltr_idx,
                                     rtl_idx=panel.rtl_idx)
                    session.add(db_panel)

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
