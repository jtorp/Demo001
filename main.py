<<<<<<< HEAD
=======
"""from fastapi import FastAPI


#app = FastAPI()


/*@app.get("/")
def root():
    return {"msg": "Hello World!"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
"""

>>>>>>> b5d27bc2d1ed14071a0a7d1b86f0e107f5156fea
from fastapi import FastAPI
from fastapi.responses import JSONResponse
import uvicorn
import datetime

start_time = datetime.datetime.utcnow()  # capture app start time

def format_uptime(td: datetime.timedelta) -> str:
    total_seconds = int(td.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours}h {minutes}m {seconds}s"

def create_app() -> FastAPI:
    app = FastAPI()

    @app.get("/", response_class=JSONResponse)
    async def root():
        return {"msg": "See you later!"}

    @app.get("/healthz", response_class=JSONResponse, tags=["Health"])
    async def health_check():
        return {"status": "Fine"}

    @app.get("/status", response_class=JSONResponse)
    async def get_status():
        uptime = datetime.datetime.utcnow() - start_time
        return {
            "status": "running",
            "uptime": format_uptime(uptime),
        }

    return app

app = create_app()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)

