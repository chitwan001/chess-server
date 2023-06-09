import server.chessengine as chessengine
import os

from flask_cors import CORS
from flask import Flask,jsonify,request
def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    # app.config.from_mapping(
    #     SECRET_KEY='dev',
    #     DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    # )
    CORS(app)
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/')
    def hello():
        data ={
            "response": "true"
        }
        return jsonify(data)

    @app.route('/calculate',methods=['POST'])
    def calculateMove():
        data = request.json
        boardData:list[list[str]] = data.get('boardData')
        check = data.get('check')
        # print(boardData)
        head = chessengine.__init__(boardData,check)
        newBoard = head.alphabeta()
        # print(head.board.movePlayed)
        data = {
            "movePlayedByAI": newBoard.movePlayed
        }
        return jsonify(data)

    return app
