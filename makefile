.PHONY: test clean run setup frontend backend
.ONESHELL:

DB_FILE := db/database.db
BACKEND_PORT := 8000

venv: venv/touchfile

venv/touchfile: requirements.txt
	test -d venv || python -m venv venv
	. venv/bin/activate; pip install -Ur requirements.txt
	touch venv/touchfile

setup:
	. venv/bin/activate
	pip install -Ur requirements.txt

	mkdir -p $(dir $(DB_FILE))
	test -f $(DB_FILE) || sqlite3 $(DB_FILE) "VACUUM;"

test: venv
	. venv/bin/activate
	pytest unit_tests/

run: venv
	make backend &
	make frontend
	wait

backend: venv
	lsof -ti :$(BACKEND_PORT) | xargs -r kill -9
	. venv/bin/activate
	fastapi dev src/comic_splitter/server.py

frontend:
	cd frontend && npm install && npm run dev

clean:
	rm -rf venv
	find . -name "*.pyc" -delete
	rm -f $(DB_FILE)
