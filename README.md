# Comic Splitter

Use makefile commands
``` bash
make setup
make test
make run
make frontend
make backend
make clean
```

# Database Setup
create db/database.db
sqlite3 db/database.db

## Server

**fast api server**
testing dev: `fastapi dev main.py`
testing run: `fastapi run main.py`

## Frontend

**frontend**
`npm run dev`

## Setup

pyproject.toml initial setup
`pip install .`

## Run as Module

**in src/**  
_Single Image_
`python -m comic_splitter -i ../unit_tests/assets/test_page_multiple_panels.jpg`
_Directory of Valid Files_
`python -m comic_splitter -d ../unit_tests/assets/`
