from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine, select

from comic_splitter.db.database import get_session
from comic_splitter.db.models import Author, Series
from comic_splitter.server import app


class TestDatabaseEndpoints:

    # @pytest.mark.paramaterize() #known author, and unknown author
    # def test_create_book

    def test_create_book_with_pages(self):
        '''
            for future me:
            book creation after confirmed split
            /split/ endpoint will get a json
            once split is configured and confirmed it will be saved into db
            as a book in /book/
        '''

        dummy_panels = [
            {'x': 5,
             'y': 5,
             'width': 20,
             'height': 30,
             'rtl_idx': 2,
             'ltr_idx': 1,
             'centroid': (15.0, 20.0)},
            {'x': 25,
             'y': 5,
             'width': 20,
             'height': 30,
             'rtl_idx': 1,
             'ltr_idx': 2,
             'centroid': (35.0, 20.0)}]

        payload = {
                'title': 'dummy-comic',
                'series_title': 'dummy-series',
                'author_name': 'dummy-author',
                'entry_number': '1',
                'pages': [
                    {
                        'page_number': 1,
                        'panels': dummy_panels
                    },
                ],
            }
        engine = create_engine(
            "sqlite:///testing.db",
            connect_args={"check_same_thread": False})
        SQLModel.metadata.create_all(engine)
        with Session(engine) as session:
            def get_session_override():
                return session
            app.dependency_overrides[get_session] = get_session_override
            client = TestClient(app)
            response = client.post(
                "/books/", json=payload)
            app.dependency_overrides.clear()
            data = response.json()
            print(data)
            assert data["title"] == "dummy-comic"
            assert data["entry_number"] == 1

            find_author_query = select(
                Author).where(Author.name == "dummy-author")
            author_is_found = session.exec(find_author_query).first()
            assert author_is_found

            find_series_query = select(
                Series).where(Series.title == "dummy-series")
            series_is_found = session.exec(find_series_query).first()
            assert series_is_found

            # assert len(data["pages"]) == 1
            # assert len(data["pages"]["panels"]) == dummy_panels
