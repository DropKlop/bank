from fastapi import FastAPI
import uvicorn

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))


from api.users_api import router as user_router



app = FastAPI()

app.include_router(user_router)


if __name__ == "__main__":
    uvicorn.run(app="main:app", host="localhost", port=8000, reload=True)