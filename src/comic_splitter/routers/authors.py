from typing import Annotated, List
from fastapi import APIRouter, HTTPException, Query
from sqlmodel import select

from comic_splitter.db.models import Author, AuthorPublic, AuthorCreate
from comic_splitter.server import SessionDep

router = APIRouter(prefix='/authors', tags=['Authors'])


@router.post("/", response_model=AuthorPublic)
def create_author(author: AuthorCreate, session: SessionDep):
    db_author = Author.model_validate(author)
    session.add(db_author)
    session.commit()
    session.refresh(db_author)
    return db_author


@router.get("/{author_id}", response_model=AuthorPublic)
def get_author(author_id: int, session: SessionDep):
    author = session.get(Author, author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    return author


@router.get('/', response_model=List[AuthorPublic])
def get_authors(
        session: SessionDep, offset: int = 0,
        limit: Annotated[int, Query(le=100)] = 100,):
    get_statement = select(Author).offset(offset).limit(limit)
    authors = session.exec(get_statement).all()
    return authors


@router.delete("/{author_id}")
def delete_author(author_id: int, session: SessionDep):
    author = session.get(Author, author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    session.delete(author)
    session.commit()
    return {"ok": True}
