import itertools as it
from axioms import test_axioms
from copy import deepcopy


def init_model():
    model = dict()
    model["DOMAIN"] = list()
    model["V"] = list()
    model["T"] = list()
    model["B"] = list()
    return model


def search_model():
    dict_b_set = dict()
    for i in range(3,7):
        dict_b_set[i] = generate_b(i)

    models = []
    for no_v in [2, 3]:
        for no_t in range(1, no_v + 1):
            model = init_model()
            no_d = no_v + no_t
            model["DOMAIN"] = list(range(1, (no_d + 1)))
            model["V"] = list(range(1, no_v + 1))
            model["T"] = list(range(no_v+1, no_d + 1))

            number_of_domain = len(model["DOMAIN"])
            for i in range(0, len(dict_b_set[number_of_domain])):
                current_model = deepcopy(model)
                current_model["B"] = list(dict_b_set[number_of_domain][i])
                if test_axioms(current_model):
                    models.append(current_model)
    return models


def generate_b(n):
    r = range(1, n+1)
    full_b = list(it.permutations(r, 2))
    filter_b = [i for i in full_b if i[0] != 1]

    combinations_of_b = list(it.combinations(filter_b, (n-1)))
    return combinations_of_b