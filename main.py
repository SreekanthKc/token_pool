import json
import app.models.tokens as model
from flask import Flask, request, jsonify
from app.utils.db_initializer import db
from app.utils.sql_connection import ConnectSqlClient
from app.models.tokens import Tokens, TokenListSchema
from flask import Response
from functools import lru_cache

app = Flask(__name__, static_folder='public')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = ConnectSqlClient.connection_string()
db.init_app(app)

with app.app_context():
    db.create_all()
    print("DB created")


@app.route('/post_token', methods=['POST'])
def post_token():
    token_name = request.args.get('token_name')
    token = db.session.query(Tokens).filter(Tokens.token_name == token_name).first()
    if token:
        response = Response(json.dumps({"Response": "Token name already used"}), status=409,
                            mimetype='application/json')
        return response
    else:
        tokens = Tokens(
            token_name=token_name
        )
        tokens.save()
        response = Response(json.dumps({"Response": "Created Token"}), status=201, mimetype='application/json')
        return response


@app.route('/get_token', methods=['GET'])
def get_token():
    pass


@app.route('/token_status', methods=['GET'])
def get_token_status():
    tokens = db.session.query(Tokens).filter(Tokens.id >= 0)
    token_schema = model.TokenListSchema(many=True)
    print(token_schema)
    result = token_schema.dump(tokens)
    response = Response(json.dumps({"token_status": result}), status=200, mimetype='application/json')
    return response


@app.route('/')
# @app.route('/<path:path>')
def root():
    store_to_cache()
    return jsonify({'message': 'Stored'})
    # return json.dumps({'sb_token': "Token"})


@lru_cache(maxsize=10)
def store_to_cache():
    return {'this_goes_to_cache': 'and_this_too', '123': 'and_this_too', 'sdfsdf': 'and_this_too'}


@app.route('/get_cache_info')
def get_cache_info():
  cache_info = store_to_cache.cache_info()

  return jsonify({
      'Hits': cache_info.hits,
      'Misses': cache_info.misses,
      'Maxsize': cache_info.maxsize,
      'Currsize': cache_info.currsize
  })



if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8082, debug=True)
