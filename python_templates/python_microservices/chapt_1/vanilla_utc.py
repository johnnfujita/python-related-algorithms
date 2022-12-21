import json
import time


# environ, the response with status and readers as a list of tuples, bytes of some text
def application(environ, start_response):
    headers = [("Content-type", "application/json")]
    start_response("200 OK", headers)
    return [bytes(json.dumps({"time": time.time()}), "utf8")]

## Can be runned with gunicorn
