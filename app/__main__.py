import uvicorn

if __name__ == '__main__':
    uvicorn.run('app.entrypoints.fastapi_app:app', host='0.0.0.0')
