from comic_splitter.config import DB_FILE
from sqlmodel import SQLModel, Session, create_engine

sqlite_url = f'sqlite:///{DB_FILE}'
connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)
SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def main():
    create_db_and_tables()


if __name__ == "__main__":
    main()
