from fastapi import FastAPI
import json


# Init
app = FastAPI(debug=True)


# index
@app.get('/')
def get_index():
    return {'msg': 'Hello Udacians'}


# Data
with open("data.json") as f:
    data = json.load(f)


# GET all items
@app.get('/api')
def get_data():
    return {"data": data}


# GET single item by id (GET POST PUT PATCH DELETE HEAD... etc)
@app.get('/api/i/{id}')
def get_by_id(id: int):
    '''
    get single item by its ID
    '''
    # print(data)
    item = [item for item in data if item['id'] == id]
    return {"data": item}


# GET single item by title
@app.get('/api/t/{title}')
async def get_by_title(title):
    '''
    get single item by its title
    '''
    print(title)
    item = [item for item in data if item['title'] == title]
    return {"data": item}
