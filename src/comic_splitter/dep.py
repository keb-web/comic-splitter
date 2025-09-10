from typing import Annotated

from fastapi import Depends
from sqlmodel import Session

import comic_splitter.db.database as db

SessionDep = Annotated[Session, Depends(db.get_session)]
