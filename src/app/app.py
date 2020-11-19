#!/usr/bin/env python3
from flask import Flask, request, jsonify
from flask_cors import CORS

from query import Query

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

query_obj = Query("../../crawlers/stack/data/data.jsonl")


@app.route('/search')
def search():
    global query_obj
    params = request.json
    if params is None:
        params = request.args

    inp_query = params['query']
    num_results = int(params['num_results'])

    result = query_obj.search(inp_query, num_results)
    tags = list(query_obj.predict_tags(inp_query))
    print(f"Query:{inp_query}")
    print(f"Tags are {tags} and result=>\n{result}")
    return jsonify({'tags': tags, 'results': result})


@app.route('/')
def home():
    return jsonify({
        "msg": "Nothing here",
        "goto": "/search"
    })


if __name__ == '__main__':
    app.run(debug=False)
