from fastapi.testclient import TestClient
from flask import Flask, Response, request

from app.main import app as fastapi_app

flask_app = Flask(__name__)
test_client = TestClient(fastapi_app)


@flask_app.route("/", defaults={"path": ""})
@flask_app.route(
    "/<path:path>",
    methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
)
def catch_all(path):
    url = request.url
    method = request.method
    headers = dict(request.headers)
    data = request.get_data()

    fastapi_response = test_client.request(
        method=method, url=url, headers=headers, data=data
    )

    return Response(
        fastapi_response.content,
        status=fastapi_response.status_code,
        headers=dict(fastapi_response.headers),
    )


# This is the WSGI entry point
application = flask_app

# from flask import Flask, Response, request

# from app.main import app as fastapi_app

# flask_app = Flask(__name__)


# @flask_app.route("/", defaults={"path": ""})
# @flask_app.route("/<path:path>")
# def catch_all(path):
#     async def _catch_all():
#         scope = {
#             "type": "http",
#             "http_version": "1.1",
#             "method": request.method,
#             "headers": [
#                 (k.lower().encode(), v.encode())
#                 for k, v in request.headers.items()
#             ],
#             "path": request.path,
#             "raw_path": request.path.encode(),
#             "query_string": request.query_string,
#             "scheme": request.scheme,
#             "server": (
#                 request.host.split(":")[0],
#                 request.host.split(":")[1] if ":" in request.host else None,
#             ),
#             "client": (request.remote_addr, None),
#         }

#         async def receive():
#             return {"type": "http.request", "body": request.get_data()}

#         async def send(event):
#             if event["type"] == "http.response.start":
#                 status_code = event["status"]
#                 headers = [
#                     (name.decode(), value.decode())
#                     for name, value in event.get("headers", [])
#                 ]
#             elif event["type"] == "http.response.body":
#                 body = event.get("body", b"")
#                 return Response(body, status=status_code, headers=headers)

#         await fastapi_app(scope, receive, send)

#     return flask_app.ensure_sync(_catch_all)()


# # This is the WSGI entry point
# application = flask_app
