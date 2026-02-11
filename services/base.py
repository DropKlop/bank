from api.depencies import DBDep



class BaseService:
    db: DBDep | None = None

    def __init__(self, db: DBDep | None = None):
        self.db = db
