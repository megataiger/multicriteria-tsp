import random


def optimization(data, properties, limits_map):
    for i in range(len(data)):
        for j in range(len(data)):
            find_min(data, i, j, properties, limits_map)


def find_min(data, i, j, properties, limits_map):
    travel_ways = data[i][j]
    optim_travel_way = None
    for temp in travel_ways:
        if comparison(temp, properties, limits_map):
            if optim_travel_way is None or \
                    temp[properties[0]] < optim_travel_way[properties[0]]:
                optim_travel_way = temp
    data[i][j] = optim_travel_way


def comparison(param_map, properties, limits_map):
    result = True
    for i in properties:
        if limits_map.get(i) is not None and limits_map.get(i) > 0:
            result = result and param_map[i] <= limits_map[i]
    return result


def get_random_parameters(transport_name, path):
    return {'kind': transport_name,
            'path': path,
            'cost': random.randrange(0, 2000, 1),
            'time': random.randrange(1, 360, 1),
            'class': random.randrange(1, 3, 1)}


def build_multiple_criteria_matrix(matrix):
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            matrix[i][j] = [
                get_random_parameters('plane', matrix[i][j]),
                get_random_parameters('car', matrix[i][j]),
                get_random_parameters('train', matrix[i][j])
            ]
