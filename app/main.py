from a2wsgi import ASGIMiddleware
from fastapi import FastAPI, Request
from fastapi.routing import APIRouter

from app.api.endpoint import (
    api_city,
    api_cover,
    api_forecast,
    api_loyalty,
    api_sheduler,
    api_stat,
    api_user,
)
from app.core.config import LoggingRoute
from app.crud.db_city import (
    add_task_city_transaction,
    check_signature,
    del_task_city_transaction,
    get_all_task_city_transaction,
    record_city_transaction,
    set_unlimited_city_compatibility,
)
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
app.include_router(
    api_sheduler.router, prefix="/api/scheduler", tags=["schedulers"]
)
app.include_router(router)


@app.get("/")
async def root():
    return {"message": "Welcome to the Telegram Bot Backend"}


# @app.get("/payment-notification")
# async def payment_notification(request: Request):
#     # Получаем все параметры из запроса
#     params = dict(request.query_params)
#     SignatureValue = params.get("SignatureValue")
#     OutSum = params.get("OutSum")
#     user_id = params.get("Shp_id")
#     inv_id = params.get("InvId")
#     # Выводим полученные данные
#     print("Received payment notification:")
#     if check_signature(inv_id, SignatureValue):
# record_city_transaction(user_id, OutSum, True)
# set_unlimited_city_compatibility(user_id)
# add_task_city_transaction(user_id)
# # inv_id = params.get("InvId", "")
# return f"OK{inv_id}"
@app.get("/payment-notification")
async def payment_notification(request: Request):
    params = dict(request.query_params)
    signature_value = params.get("SignatureValue")
    out_sum = params.get("OutSum")
    shp_id = params.get("Shp_id")
    inv_id = params.get("InvId")

    print("Received payment notification:", params)

    if check_signature(inv_id, signature_value, out_sum, shp_id):
        record_city_transaction(shp_id, out_sum, True)
        set_unlimited_city_compatibility(shp_id)
        add_task_city_transaction(shp_id)
        return f"OK{inv_id}"
    else:
        return "BAD SIGNATURE"


@app.get("/api/payment-task")
async def payment_tasks():
    return get_all_task_city_transaction()


@app.post("/api/payment-task/{user_id}")
async def del_payment_task(user_id: int):
    return del_task_city_transaction(user_id)


application = ASGIMiddleware(app, wait_time=5.0)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)


'''
# import sys

# # Путь к директории вашего проекта
# path = '/home/sozdatel33/server_for_arcanBot/app'
# if path not in sys.path:
#     sys.path.append(path)

# from fastapi import FastAPI
# from fastapi.middleware.wsgi import WSGIMiddleware
# from app.main import app  # Импортируйте ваше FastAPI приложение

# # Оберните FastAPI приложение в WSGIMiddleware
# application = WSGIMiddleware(app)


# import sys

# # Путь к директории вашего проекта
# path = '/home/sozdatel33/server_for_arcanBot'
# if path not in sys.path:
#     sys.path.append(path)

# from app.main import app  # Импортируйте ваше FastAPI приложение
# import uvicorn
# import asyncio

# def application(environ, start_response):
#     """
#     WSGI application для запуска FastAPI с uvicorn.
#     """
#     server = uvicorn.Server(uvicorn.Config(app, host='127.0.0.1', port=8000))
#     server.config.load()
#     server.lifespan = server.config.lifespan_class(server.config)

#     async def run():
#         await server.startup()
#         try:
#             message = await server.main.handle(environ["scope"], start_response)
#             await server.send(message)
#         finally:
#             await server.shutdown()

#     asyncio.run(run())
#     return []



# This file contains the WSGI configuration required to serve up your
# web application at http://serverArcanBot-sozdatel33.pythonanywhere.com/
# It works by setting the variable 'application' to a WSGI handler of some
# description.
#

# +++++++++++ GENERAL DEBUGGING TIPS +++++++++++
# getting imports and sys.path right can be fiddly!
# We've tried to collect some general tips here:
# https://help.pythonanywhere.com/pages/DebuggingImportError


# +++++++++++ HELLO WORLD +++++++++++
# A little pure-wsgi hello world we've cooked up, just
# to prove everything works.  You should delete this
# code to get your own working.


# HELLO_WORLD = """<html>
# <head>
#     <title>PythonAnywhere hosted web application</title>
# </head>
# <body>
# <h1>Hello, World!</h1>
# <p>
#     This is the default welcome page for a
#     <a href="https://www.pythonanywhere.com/">PythonAnywhere</a>
#     hosted web application.
# </p>
# <p>
#     Find out more about how to configure your own web application
#     by visiting the <a href="https://www.pythonanywhere.com/web_app_setup/">web app setup</a> page
# </p>
# </body>
# </html>"""


# def application(environ, start_response):
#     if environ.get('PATH_INFO') == '/':
#         status = '200 OK'
#         content = HELLO_WORLD
#     else:
#         status = '404 NOT FOUND'
#         content = 'Page not found.'
#     response_headers = [('Content-Type', 'text/html'), ('Content-Length', str(len(content)))]
#     start_response(status, response_headers)
#     yield content.encode('utf8')


# Below are templates for Django and Flask.  You should update the file
# appropriately for the web framework you're using, and then
# click the 'Reload /yourdomain.com/' button on the 'Web' tab to make your site
# live.

# +++++++++++ VIRTUALENV +++++++++++
# If you want to use a virtualenv, set its path on the web app setup tab.
# Then come back here and import your application object as per the
# instructions below


# +++++++++++ CUSTOM WSGI +++++++++++
# If you have a WSGI file that you want to serve using PythonAnywhere, perhaps
# in your home directory under version control, then use something like this:
#
#import sys
#
#path = '/home/sozdatel33/path/to/my/app
#if path not in sys.path:
#    sys.path.append(path)
#
#from my_wsgi_file import application  # noqa


# +++++++++++ DJANGO +++++++++++
# To use your own django app use code like this:
#import os
#import sys
#
## assuming your django settings file is at '/home/sozdatel33/mysite/mysite/settings.py'
## and your manage.py is is at '/home/sozdatel33/mysite/manage.py'
#path = '/home/sozdatel33/mysite'
#if path not in sys.path:
#    sys.path.append(path)
#
#os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'
#
## then:
#from django.core.wsgi import get_wsgi_application
#application = get_wsgi_application()



# +++++++++++ FLASK +++++++++++
# Flask works like any other WSGI-compatible framework, we just need
# to import the application.  Often Flask apps are called "app" so we
# may need to rename it during the import:
#
#
#import sys
#
## The "/home/sozdatel33" below specifies your home
## directory -- the rest should be the directory you uploaded your Flask
## code to underneath the home directory.  So if you just ran
## "git clone git@github.com/myusername/myproject.git"
## ...or uploaded files to the directory "myproject", then you should
## specify "/home/sozdatel33/myproject"
#path = '/home/sozdatel33/path/to/flask_app_directory'
#if path not in sys.path:
#    sys.path.append(path)
#
#from main_flask_app_file import app as application  # noqa
#
# NB -- many Flask guides suggest you use a file called run.py; that's
# not necessary on PythonAnywhere.  And you should make sure your code
# does *not* invoke the flask development server with app.run(), as it
# will prevent your wsgi file from working.


import sys
path = '/home/sozdatel33/server_for_arcanBot'
if path not in sys.path:
    sys.path.append(path)

from app.main import application

# import sys
# path = '/home/sozdatel33/server_for_arcanBot'
# if path not in sys.path:
#     sys.path.append(path)

# from app.flask_wrapper import application


'''
