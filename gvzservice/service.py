
import asyncio
import os
import sys
from aiohttp import web
from subprocess import PIPE

STATIC_PATH = "./static/"
GRAPHVIZ_EXE = "C:/msys64/usr/bin/cat.exe -n"
APP_PORT=8888

if sys.platform == 'win32':
    loop = asyncio.ProactorEventLoop()
    asyncio.set_event_loop(loop)

async def handle(request):
    ctnt = await request.read()
    try:
        result = await run_graphviz(ctnt)
    except Error as err:
        err
    if not isinstance(result, bytes):
        (out, err) = result
        result = out + err
    return web.Response(body=result, content_type="text/txt")

def redirect_handle(location):
    raise web.HTTPTemporaryRedirect(location)

def start_service():
    app = web.Application()
    app.router.add_post('/exec', handle)
    app.router.add_static('/static', STATIC_PATH)
    app.router.add_get('/', lambda req: redirect_handle("static/index.html"))

    web.run_app(app, port=APP_PORT)

async def run_graphviz(data):
    proc = await asyncio.create_subprocess_shell(
        GRAPHVIZ_EXE, 
        stdin=PIPE,
        stdout=PIPE,
        stderr=PIPE)
    (out, err) = await proc.communicate(data)
    ret = proc.returncode
    if ret == 0:
        return out
    else:
        return (out, err)