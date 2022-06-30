from re import A
from uvicorn import run
from application.main import app

if __name__ == "__main__":
    print('Server running...')
    run(app, host="127.0.0.1", port=8000)