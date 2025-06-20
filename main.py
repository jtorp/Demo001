from fastapi import FastAPI


app = FastAPI()


@app.get("/")
def root():
    return {"msg": "Hello World!"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000)