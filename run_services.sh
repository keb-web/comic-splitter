#! usr/bin/bash
# echo 'hello world!'
# echo '$VIRTUAL_ENV'

# check if .env exists
# activate venv and install requirements if not
PWD=`pwd`
activate () {
	source $PWD/.venv/bin/activate
}

# fastapi run src/comic_splitter/server.py
# npm run dev on frontend/

# replace with docker when connecting to mongo
