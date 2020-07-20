from fastapi import FastAPI
import uvicorn


# Init
app = FastAPI(debug=True)


# index
@app.get('/')
def get_index():
    return {'msg': 'Hello Udacians'}


# if __name__ == '__main__':
#     uvicorn.run(app, host="127.0.0.1", port="5000")
