import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine, select
from sqlmodel.pool import StaticPool

from comic_splitter.db.database import get_session
from comic_splitter.db.models import Author, Series
from comic_splitter.server import app


class TestDatabaseEndpoints:

    @pytest.fixture(name="session")
    def session_fixture(self):
        engine = create_engine(
            "sqlite://",
            connect_args={"check_same_thread": False},
            poolclass=StaticPool
        )
        SQLModel.metadata.create_all(engine)
        with Session(engine) as session:
            yield session

    # @pytest.mark.paramaterize() #known author, and unknown author
    def test_create_book_with_pages(self, session: Session):
        '''
            book creation after confirmed split
            /split/ endpoint will get a json
            json sent to frontend for confirmation
            /book/ endpoint creeates book after confirmation
        '''
        def get_session_override():
            return session
        app.dependency_overrides[get_session] = get_session_override

        dummy_panels = [
            {'x': 5, 'y': 5, 'width': 20, 'height': 30,
             'rtl_idx': 2, 'ltr_idx': 1, 'id': 1},
            {'x': 25, 'y': 5, 'width': 20, 'height': 30,
             'rtl_idx': 1, 'ltr_idx': 2, 'id': 2}]
        dummy_payload = {
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

        client = TestClient(app)
        response = client.post(
            "/books/", json=dummy_payload)
        app.dependency_overrides.clear()
        data = response.json()

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

        assert len(data["pages"]) == 1
        page_1 = data['pages'][0]
        assert page_1["panels"] == dummy_panels
