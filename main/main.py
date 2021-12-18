import os

from app import app
from config.config import Configuration

if __name__ == '__main__':
    app.run(host=Configuration.HOST, debug=True, port=int(Configuration.PORT))
