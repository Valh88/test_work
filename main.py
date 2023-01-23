from fastapi import FastAPI, WebSocket, Request
from fastapi.templating import Jinja2Templates

app = FastAPI()

templates = Jinja2Templates(directory='templates')

num_message = 0

@app.get("/")
async def get(request: Request):
    global num_message
    num_message = 0
    return templates.TemplateResponse('index.html', context={'request': request})


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_json()
        global num_message
        num_message += 1
        data['num'] = num_message
        #data = {'message': str, 'num': int}
        await websocket.send_json(data)
