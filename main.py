from datetime import datetime
from flask import Flask, jsonify, request
from elasticsearch import Elasticsearch

# from api.elastic_test import connect_elasticsearch
# from flask_app import app
# from config.config_handling import get_config_value


es = Elasticsearch('https://localhost:9200')

app = Flask(__name__)


##Health endpoint
@app.route('/health', methods=['POST'])
def health_check():
    return "OK", 200


@app.route('/insert_data', methods=['POST'])
def insert_data():
    if request.form['operation'] == 'insert':
        city_id = request.form['city_id']
        city = request.form['city']
        population = request.form['population']
        city_obj = {
            'city_id': city_id,
            'city': city,
            'occupation': population
        }

        result = es.index(index='city', id=city_id, body=city_obj, request_timeout=30)
        return jsonify(result)
    elif request.form['operation'] == 'update':
        city_id = request.form['city_id']
        param = request.form['param']
        new_val = request.form['new_value']

        update_dict = {
            'doc': {
                param: new_val
            }
        }

        response = es.update(index='city', id=city_id, body=update_dict)
        return jsonify(response)
    else:
        return "Internal Server Error", 500


@app.route('/get-population', methods=['GET'])
def search_user():
    city = request.form['city']

    query_body = {
        "query": {
            "match": {
                "name": city
            }
        }
    }

    res = es.search(index="city", body=query_body)

    return jsonify(res['city']['population'])

