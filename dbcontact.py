from flask import Flask
import os

app = Flask(__name__);


if __name__ == '__main__':
    app.debug = True
    # https://docs.c9.io/docs/run-an-application
    # echo $PORT
    port = int(os.getenv('PORT', 8080))
    # echo $IP
    # host = os.getenv('IP', '0.0.0.0')
    app.run(port=8080, host= '0.0.0.0')
    # app.run()