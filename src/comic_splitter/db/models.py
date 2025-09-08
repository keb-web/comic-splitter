from sqlmodel import Field, SQLModel


class Author(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)


class Series(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str | None = Field(index=True)
    author_id: int | None = Field(default=None, foreign_key='author.id')


class Book(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    chapter: str = Field(index=True)
    author_id: int | None = Field(default=None, foreign_key='author.id')
    series_id: int | None = Field(default=None, foreign_key='series.id')


class Page(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    number: int = Field(index=True)
    x: int | None = Field(default=None)
    y: int | None = Field(default=None)
    height: int | None = Field(default=None)
    width: int | None = Field(default=None)
    ltr_index: int | None = Field(default=None)
    rtl_index: int | None = Field(default=None)
    book_id: int | None = Field(default=None, foreign_key='book.id')
