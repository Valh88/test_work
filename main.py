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
async def websocket_endpoint(websocket: WebSocket, client_id:str, db=db) -> None:
    try:
        user = db.get_user(client_id=client_id)
    except KeyError:
        user = db.append(client_id=client_id)

    await websocket.accept()
    while True:
        print(DataBase.db)
        data = await websocket.receive_json()
        user['num'] += 1
        data['num'] = user['num']
        #data = {'message': str, 'num': int}
        await websocket.send_json(data)
