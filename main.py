from fastapi import FastAPI
from routes import health,search
from backround import background_task
app = FastAPI()


app.include_router(health.router)
app.include_router(search.router)

@app.get("/")
async def root():
    background_task()




