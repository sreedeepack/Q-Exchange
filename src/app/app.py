#!/usr/bin/env python3
from flask import Flask, request, jsonify
from flask_cors import CORS

from query import Query

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

query_obj = Query()


@app.route('/search')
def search():
    global query_obj
    params = request.json
    if params is None:
        params = request.args

    inp_query = params['query']
    num_results = params['num_results']
    # TODO predict tags?
    tags = ""
    result = query_obj.search(inp_query, num_results)

    return jsonify({'tags': tags, 'results': result})


if __name__ == '__main__':
    app.run(debug=True)
