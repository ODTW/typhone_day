import uvicorn
from fastapi import FastAPI

app = FastAPI()


@app.get("/hi")
def Hello():
    return {"msg": "Hello"}


if __name__ == "__main__":
    uvicorn.run(app="main:app", reload=True)
