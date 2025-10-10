from typing import List, Literal, Optional
from fastapi import Form, UploadFile
from pydantic import BaseModel
from sqlmodel import Field, SQLModel, Relationship


class SplitFilesPublic(BaseModel):
    image_type: str
    images: List[str]


class AuthorBase(SQLModel):
    name: str = Field(index=True)


class Author(AuthorBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    books: List["Book"] = Relationship(back_populates="author")
    series: Optional[List["Series"]] = Relationship(back_populates="author")


class AuthorCreate(AuthorBase):
    name: str


class AuthorPublic(AuthorBase):
    id: int


class SeriesBase(SQLModel):
    title: str | None = Field(index=True)


class Series(SeriesBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    books: List["Book"] = Relationship(back_populates="series")
    author: Author = Relationship(back_populates="series")
    author_id: int | None = Field(default=None, foreign_key='author.id')


class SeriesCreate(SeriesBase):
    pass


class SeriesPublic(SeriesBase):
    id: int


class BookBase(SQLModel):
    title: str = Field(index=True)
    entry_number: Optional[int] = None
    # pages: Optional[Pages] = Relationship(back_populates='books')


class Book(BookBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    author: Optional[Author] = Relationship(back_populates="books")
    series: Optional[Series] = Relationship(back_populates="books")
    author_id: int | None = Field(default=None, foreign_key='author.id')
    series_id: int | None = Field(default=None, foreign_key='series.id')


class BookCreate(BookBase):
    author_name: str
    series_title: Optional[str]


class BookPublic(BookBase):
    id: int


class PageBase(SQLModel):
    page_number: int = Field(index=True)


class Page(PageBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    book_id: int | None = Field(default=None, foreign_key='book.id')


class PageCreate(PageBase):
    pass


class PagePublic(PageBase):
    id: int


class PanelBase(SQLModel):
    x: int | None = Field(default=None)
    y: int | None = Field(default=None)
    height: int | None = Field(default=None)
    width: int | None = Field(default=None)
    ltr_index: int | None = Field(default=None)
    rtl_index: int | None = Field(default=None)


class Panel(PanelBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    page_id: int | None = Field(default=None, foreign_key='page.id')


class PanelCreate(PanelBase):
    pass


class PanelPublic(PanelBase):
    id: int
