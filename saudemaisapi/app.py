from fastapi import FastAPI

app = FastAPI(title='Saude+API')


@app.get('/')
def root():
    return {'hello': 'world'}


# @app.post('/eventos', status_code=HTTPStatus.CREATED, response_model=**)
# def creat_eventos():
