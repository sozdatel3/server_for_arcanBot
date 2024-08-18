from a2wsgi import ASGIMiddleware
from fastapi import FastAPI
from fastapi.routing import APIRouter

from app.api.endpoint import (
    api_city,
    api_cover,
    api_forecast,
    api_loyalty,
    api_stat,
    api_user,
)
from app.core.config import LoggingRoute
from app.init import init_db

init_db()
# ook
app = FastAPI()
router = APIRouter(route_class=LoggingRoute)

app.include_router(api_user.router, prefix="/api/users", tags=["users"])
app.include_router(api_city.router, prefix="/api/cities", tags=["cities"])
app.include_router(api_loyalty.router, prefix="/api/loyalty", tags=["loyalty"])
app.include_router(
    api_forecast.router, prefix="/api/forecasts", tags=["forecasts"]
)
app.include_router(
    api_stat.router, prefix="/api/statistics", tags=["statistics"]
)
app.include_router(api_cover.router, prefix="/api/covers", tags=["covers"])
app.include_router(router)


@app.get("/")
async def root():
    return {"message": "Welcome to the Telegram Bot Backend"}


application = ASGIMiddleware(app)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
