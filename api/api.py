# -*- coding: utf-8 -*-
"""
api.ipynb
"""

#pip install flask-restx

from flask import Flask, jsonify, request
from sqlalchemy import create_engine
from datetime import datetime
from flask_restx import Api, Namespace, Resource, \
    reqparse, inputs, fields


user = ""
passw = ""
host = ""
database = "main"

app = Flask(__name__)
app.config['API_KEYS'] = {
    'api_key_1': 'user_1',
    'api_key_2': 'user_2'
}

app.config["SQLALCHEMY_DATABASE_URI"] = host

api = Api(app, version = '1.0',
    title = 'The famous REST API with FLASK!',
    description = """
        This RESTS API is an API to built with FLASK
        and FLASK-RESTX libraries
        """,
    contact = "gustavom@faculty.ie.edu",
    endpoint = "/api/v1"
)

# def api_key_required_no_modify(f):
#     @wraps(f)
#     def decorated_function(*args, **kwargs):
#         api_key = request.headers.get('X-API-KEY')
#         if api_key not in app.config['API_KEYS']:
#             return jsonify({'error': 'Invalid API key'}), 401
#         return f(*args, **kwargs)
#     return decorated_function



def connect():
    db = create_engine(
    'mysql+pymysql://{0}:{1}@{2}/{3}' \
        .format(user, passw, host, database), \
    connect_args = {'connect_timeout': 10})
    conn = db.connect()
    return conn

def disconnect(conn):
    conn.close()

customers = Namespace('customers',
    description = 'All operations related to customers',
    path='/api/v1')
api.add_namespace(customers)

@customers.route("/customers")
class get_all_users(Resource):
    
    #@api_key_required_no_modify
    def get(self):
        conn = connect()
        select = """
            SELECT *
            FROM customers
            LIMIT 5000;
            """
        result = conn.execute(select).fetchall()
        disconnect(conn)
        return jsonify({'result': [dict(row) for row in result]})

@customers.route("/customers/<string:id>")
@customers.doc(params = {'id': 'The ID of the user'})
class select_user(Resource):
    
    #@api_key_required_no_modify
    @api.response(404, "CUSTOMER not found")
    def get(self, id):
        id = str(id)
        conn = connect()
        select = """
            SELECT *
            FROM customers
            WHERE customer_id = '{0}';""".format(id)
        result = conn.execute(select).fetchall()
        disconnect(conn)
        return jsonify({'result': [dict(row) for row in result]})
    
articles = Namespace('articles',
    description = 'All operations related to articles',
    path='/api/v1')
api.add_namespace(articles)

@articles.route("/articles")
class get_all_articles(Resource):
    
    #@api_key_required_no_modify
    def get(self):
        conn = connect()
        select = """
            SELECT *
            FROM articles
            LIMIT 5000;
            """
        result = conn.execute(select).fetchall()
        disconnect(conn)
        return jsonify({'result': [dict(row) for row in result]})
    
@articles.route("/articles/<string:id>")
class get_all_articles(Resource):
    
    #@api_key_required_no_modify
    def get(self):
        conn = connect()
        select = """
            SELECT *
            FROM articles
            WHERE article_id = '{0}';""".format(id)
        result = conn.execute(select).fetchall()
        disconnect(conn)
        return jsonify({'result': [dict(row) for row in result]})
    

transactions = Namespace('transactions',
    description = 'All operations related to transactions',
    path='/api/v1')
api.add_namespace(transactions)

@transactions.route("/transactions")
class get_all_transactions(Resource):
    
    #@api_key_required_no_modify
    def get(self):
        conn = connect()
        select = """
            SELECT *
            FROM transactions
            LIMIT 5000;
            """
        result = conn.execute(select).fetchall()
        disconnect(conn)
        return jsonify({'result': [dict(row) for row in result]})
    
@transactions.route("/transactions/<string:id>")
class get_all_transactions(Resource):
    
    #@api_key_required_no_modify
    def get(self):
        conn = connect()
        select = """
            SELECT *
            FROM transactions
            WHERE transaction_id = '{0}';""".format(id)
        result = conn.execute(select).fetchall()
        disconnect(conn)
        return jsonify({'result': [dict(row) for row in result]})

if __name__ == '__main__':
    app.run(debug = True)