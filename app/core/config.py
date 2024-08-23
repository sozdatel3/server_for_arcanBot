import logging
import time
from functools import wraps

# from re import DEBUG
from typing import Callable

from fastapi import Request, Response
from fastapi.routing import APIRoute
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DEBUG: bool = False

    ROBOKASSA_LOGIN: str
    ROBOKASSA_PASSWORD1: str
    ROBOKASSA_PASSWORD2: str
    ROBOKASSA_TEST_PASSWORD1: str
    ROBOKASSA_TEST_PASSWORD2: str

    model_config = SettingsConfigDict(env_file=".env", extra="allow")

    @property
    def ACTIVE_ROBOKASSA_PASSWORD1(self) -> str:
        return (
            self.ROBOKASSA_TEST_PASSWORD1
            if self.DEBUG
            else self.ROBOKASSA_PASSWORD1
        )

    @property
    def ACTIVE_ROBOKASSA_PASSWORD2(self) -> str:
        return (
            self.ROBOKASSA_TEST_PASSWORD2
            if self.DEBUG
            else self.ROBOKASSA_PASSWORD2
        )


settings = Settings()
DEBUG = settings.DEBUG
from colorlog import ColoredFormatter


class CustomLogger:
    def __init__(self):
        self.logger = logging.getLogger("custom_logger")
        self.logger.setLevel(logging.DEBUG)

        # Форматтер для файлового хендлера (без цветов)
        file_formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )

        file_handler = logging.FileHandler("app.log")
        file_handler.setFormatter(file_formatter)
        self.logger.addHandler(file_handler)

        # Цветной форматтер для консольного вывода
        console_formatter = ColoredFormatter(
            "%(log_color)s%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            log_colors={
                "DEBUG": "cyan",
                "INFO": "green",
                "WARNING": "yellow",
                "ERROR": "red",
                "CRITICAL": "red,bg_white",
            },
            secondary_log_colors={},
            style="%",
        )

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)

    def log_db_operation(self, func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            if not DEBUG:
                self.logger.info(f"Starting DB operation: {func.__name__}")
            try:
                result = func(*args, **kwargs)
                if not DEBUG:
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
                if not DEBUG:
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


# class CustomLogger:
#     def __init__(self):
#         self.logger = logging.getLogger("custom_logger")
#         self.logger.setLevel(logging.DEBUG)

#         formatter = logging.Formatter(
#             "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
#         )

#         file_handler = logging.FileHandler("app.log")
#         file_handler.setFormatter(formatter)
#         self.logger.addHandler(file_handler)

#         console_handler = logging.StreamHandler()
#         console_handler.setFormatter(formatter)
#         self.logger.addHandler(console_handler)

#     def log_db_operation(self, func: Callable) -> Callable:
#         @wraps(func)
#         def wrapper(*args, **kwargs):
#             start_time = time.time()
#             self.logger.info(f"Starting DB operation: {func.__name__}")
#             try:
#                 result = func(*args, **kwargs)
#                 self.logger.info(
#                     f"DB operation {func.__name__} completed successfully"
#                 )
#                 return result
#             except Exception as e:
#                 self.logger.error(
#                     f"DB operation {func.__name__} failed: {str(e)}"
#                 )
#                 raise
#             finally:
#                 end_time = time.time()
#                 self.logger.info(
#                     f"DB operation {func.__name__} took {end_time - start_time:.2f} seconds"
#                 )

#         return wrapper

#     def log_endpoint(self, func: Callable) -> Callable:
#         @wraps(func)
#         async def wrapper(request: Request, *args, **kwargs):
#             start_time = time.time()
#             self.logger.info(
#                 f"Received {request.method} request for {request.url.path}"
#             )
#             try:
#                 response = await func(request, *args, **kwargs)
#                 self.logger.info(
#                     f"Request to {request.url.path} completed successfully"
#                 )
#                 return response
#             except Exception as e:
#                 self.logger.error(
#                     f"Request to {request.url.path} failed: {str(e)}"
#                 )
#                 raise
#             finally:
#                 end_time = time.time()
#                 self.logger.info(
#                     f"Request to {request.url.path} took {end_time - start_time:.2f} seconds"
#                 )

#         return wrapper


# custom_logger = CustomLogger()


# class LoggingRoute(APIRoute):
#     def get_route_handler(self) -> Callable:
#         original_route_handler = super().get_route_handler()

#         @wraps(original_route_handler)
#         async def custom_route_handler(request: Request) -> Response:
#             return await custom_logger.log_endpoint(original_route_handler)(
#                 request
#             )

#         return custom_route_handler
