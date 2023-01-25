from fastapi import FastAPI, WebSocket, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

fake_db = {}

app = FastAPI()

templates = Jinja2Templates(directory='templates')


class DataBase():
    db = {}

    def append(self, client_id):
        client = {'num': 0}
        self.db[client_id] = client  
        return client
    def delete(self, client_id):
        del self.db[client_id]

    def get_user(self, client_id):
        return self.db[client_id]

    @classmethod
    def update(cls, user):
        pass
    
db = DataBase()


@app.get("/")
async def get(request: Request, response_class=HTMLResponse) -> HTMLResponse:

    return templates.TemplateResponse('index.html', context={'request': request})


@app.websocket("/ws/{client_id:str}")
async def websocket_endpoint(websocket: WebSocket, client_id:str) -> None:
    num_message = 0

    await websocket.accept()
    while True:
        data = await websocket.receive_json()
        num_message += 1
        data['num'] = num_message
        #data = {'message': str, 'num': int}
        await websocket.send_json(data)
