# from fastapi import FastAPI
# from app.api.endpoints import user, city, forecast, loyalty, cover

# app = FastAPI()

# app.include_router(user.router, prefix="/users", tags=["users"])
# app.include_router(city.router, prefix="/cities", tags=["cities"])
# app.include_router(forecast.router, prefix="/forecasts", tags=["forecasts"])
# app.include_router(loyalty.router, prefix="/loyalty", tags=["loyalty"])
# app.include_router(cover.router, prefix="/covers", tags=["covers"])

# @app.get("/")
# async def root():
#     return {"message": "Welcome to the Telegram Bot Backend"}

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)
