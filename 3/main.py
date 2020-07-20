# py main.py

from config import PORT, HOST, WORKERS
import uvicorn
from fastapi import FastAPI, WebSocket, Request, Response, File, UploadFile, Form, status
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
import os
import shutil
import datetime
import uuid

# multi threading
import logging
import subprocess
from concurrent.futures import ThreadPoolExecutor as Pool
import functools
# from functools import partial


# websocket
import socketio


# Init
app = FastAPI()

# Public ( mount a Static folders)
app.mount("/public", StaticFiles(directory="./public"), name="static")
app.mount("/export", StaticFiles(directory="./export"), name="output")
app.mount("/upload", StaticFiles(directory="./upload"), name="upload")
templates = Jinja2Templates(directory="./templates")

# # websocket (socket.io)
# sio = socketio.AsyncServer(async_mode='asgi')
# socket_app = socketio.ASGIApp(sio, static_files={'/': 'app.html'})
# background_task_started = False


# Websocket (by FastAPI)
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message text was: {data}")

if __name__ == "__main__":
    uvicorn.run("main:app", host=HOST, port=int(PORT), reload=True,
                debug=True, workers=int(WORKERS))
    # uvicorn.run(app, host='127.0.0.1', port=3000, reload=True,
    #             debug=True, workers=1)


@app.get('/')
def index(request: Request):
    return templates.TemplateResponse('index.html', {"request": request})


@app.get("/hello")
async def root():
    return {"message": "Hello World"}


# CORS
origins = [
    "http://localhost",
    # "http://127.0.0.1:3000",
    # "http://localhost:8080",
    # "http://localhost:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# allowed extenstions
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# logger
info = logging.getLogger(__name__).info


# Callback
def notify_client(_id, future):
    info(_id)
    if future.exception() is not None:
        info("got exception: %s" % future.exception())
    else:
        info("process returned %d" % future.result())
        # emit to client
        # sio.emit('done_processing', {'data': data}, broadcast=True, include_self=False)


# logging
logging.basicConfig(
    level=logging.INFO,
    format=("%(relativeCreated)04d %(process)05d %(threadName)-10s "
            "%(levelname)-5s %(msg)s"))


@app.post("/uploadfile/")
async def create_upload_file(request: Request, response: Response, file: UploadFile = File(...), style: str = Form(...)):
    # if user does not select file, browser also
    # submit an empty part without filename
    print(style)
    if file.filename == '':
        return {'error': 'please choose an image'}
    if file and allowed_file(file.filename):
        # create empty file to copy the file_object to
        global upload_folder
        # generate random id :
        _id = uuid.uuid1()
        file_object = file.file
        # upload_folder = open(os.path.join('upload', file.filename), 'wb+')
        new_name = str(_id) + '.' + file.filename.split(".")[-1].lower()
        # new_name = datetime.datetime.now().strftime(
        #     "%d%m%y%H") + '.' + file.filename.split(".")[-1]
        upload_folder = open(os.path.join('upload', new_name), 'wb+')
        shutil.copyfileobj(file_object, upload_folder)
        upload_folder.close()
        # call for style-transfer bash command

        command = "conda.bat activate style-transfer && python evaluate.py --checkpoint ./checkpoints/%s.ckpt --in-path ./upload/%s --out-path ./export/%s.jpg" % (
            style, new_name, _id)
        # command = "conda.bat activate style-transfer && python evaluate.py --checkpoint ./checkpoints/rain_princess.ckpt --in-path ./upload/12072022-Capture.png --out-path ./export/output_image.jpg"
        # subprocess.Popen(command, shell=True)

        # wait for the process completion asynchronously
        info("begin waiting")
        pool = Pool(max_workers=1)
        f = pool.submit(subprocess.call, command + "&& echo done", shell=True)
        # f.add_done_callback(callback)
        f.add_done_callback(functools.partial(notify_client, str(_id)))
        pool.shutdown(wait=False)  # no .submit() calls after that point
        info("continue waiting asynchronously")
        info("processing %s" % str(_id))
        print(f)
        # return templates.TemplateResponse('index.html', {'name': new_name, 'request': request})
        response = RedirectResponse(
            url='/', status_code=status.HTTP_303_SEE_OTHER)

        response.set_cookie(key="APP_original_image", value=new_name)
        response.set_cookie(key="APP_process", value=str(_id))
        response.set_cookie(key="APP_style", value=style)
        return response


# async def background_task():
#     """Example of how to send server generated events to clients."""
#     count = 0
#     while True:
#         await sio.sleep(10)
#         count += 1
#         await sio.emit('my_response', {'data': 'Server generated event'})


# @sio.on('connect')
# async def test_connect(sid, environ):
#     global background_task_started
#     if not background_task_started:
#         sio.start_background_task(background_task)
#         background_task_started = True
#     await sio.emit('my_response', {'data': 'Connected', 'count': 0}, process=sid)


# @sio.on('disconnect')
# def test_disconnect(sid):
#     print('Client disconnected')


# @sio.on('my_event')
# async def test_message(sid, message):
#     print(sid, message)
#     await sio.emit('my_response', {'data': message['data']}, process=sid)


# app.mount('/', socket_app)
