import logging
import time
from functools import wraps
from typing import Callable

from fastapi import Request, Response
from fastapi.routing import APIRoute
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DEBUG: bool = False

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()


class CustomLogger:
    def __init__(self):
        self.logger = logging.getLogger("custom_logger")
        self.logger.setLevel(logging.DEBUG)

        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )

        file_handler = logging.FileHandler("app.log")
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

    def log_db_operation(self, func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            self.logger.info(f"Starting DB operation: {func.__name__}")
            try:
                result = func(*args, **kwargs)
                self.logger.info(
                    f"DB operation {func.__name__} completed successfully"
                )
                return result
            except Exception as e:
                self.logger.error(
                    f"DB operation {func.__name__} failed: {str(e)}"
                )
                raise
            finally:
                end_time = time.time()
                self.logger.info(
                    f"DB operation {func.__name__} took {end_time - start_time:.2f} seconds"
                )

        return wrapper

    def log_endpoint(self, func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(request: Request, *args, **kwargs):
            start_time = time.time()
            self.logger.info(
                f"Received {request.method} request for {request.url.path}"
            )
            try:
                response = await func(request, *args, **kwargs)
                self.logger.info(
                    f"Request to {request.url.path} completed successfully"
                )
                return response
            except Exception as e:
                self.logger.error(
                    f"Request to {request.url.path} failed: {str(e)}"
                )
                raise
            finally:
                end_time = time.time()
                self.logger.info(
                    f"Request to {request.url.path} took {end_time - start_time:.2f} seconds"
                )

        return wrapper


custom_logger = CustomLogger()


class LoggingRoute(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        @wraps(original_route_handler)
        async def custom_route_handler(request: Request) -> Response:
            return await custom_logger.log_endpoint(original_route_handler)(
                request
            )

        return custom_route_handler
