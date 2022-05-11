import copy

from flask import Flask, request, jsonify
from flask_cors import CORS
from numpy import sqrt

import optimization
import geneticAlg

app = Flask(__name__)
app.config.from_object(__name__)
CORS(app)
properties = ['path', 'cost', 'time', 'class']


@app.route('/process', methods=['POST'])
def process():
    if request.method == 'POST':
        data = request.get_json()
        points = data['points']
        request_properties = data['properties']
        request_limits = convert_limits(data['limits'])
        result = convert_data(points)
        optimization.build_multiple_criteria_matrix(result)
        optimization.optimization(result, request_properties, request_limits)
        a, b = geneticAlg.processing(result, request_properties[0])
        response = build_response(a, result)
        return jsonify(result=response)


@app.route("/properties", methods=['GET'])
def get_properties():
    return jsonify(properties=properties)


def convert_data(points):
    points_number = len(points)
    adjacency_matrix = [[0] * points_number for i in range(points_number)]
    for i in range(points_number):
        for j in range(points_number):
            adjacency_matrix[i][j] = get_path(points[i], points[j])
    return adjacency_matrix


def convert_limits(limits):
    request_limits = {}
    for i in limits:
        request_limits[i['name']] = i['value']
    return request_limits


def get_path(point_one, point_two):
    first_part = point_one['coordinate'][0] - point_two['coordinate'][0]
    second_part = point_one['coordinate'][1] - point_two['coordinate'][1]
    return sqrt(pow(first_part, 2) + pow(second_part, 2))


def build_response(queue, result):
    response = []
    for i in range(len(queue)):
        if i+1 == len(queue):
            line = result[queue[i]][queue[0]]
            line['pointA'] = int(queue[i])
            line['pointB'] = int(queue[0])
            response.append(line)

        else:
            line = result[queue[i]][queue[i+1]]
            line['pointA'] = int(queue[i])
            line['pointB'] = int(queue[i+1])
            response.append(line)
    return response


if __name__ == "__main__":
    app.run(debug=True)
