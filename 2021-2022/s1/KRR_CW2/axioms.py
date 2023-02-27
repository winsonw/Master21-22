


def test_axioms(model):
    axioms = [axiom_1, axiom_2, axiom_3, axiom_4, axiom_5, axiom_6, axiom_7, axiom_8, axiom_9, axiom_10, axiom_11]
    for i in range(11):
        if not axioms[i](model):
            return False
    return True


def axiom_1(model):
    for i in model["DOMAIN"]:
        if not(i in model["V"] or i in model["T"]):
            return False
    return True


def axiom_2(model):
    return len(model["V"]) >= 2 and len(model["T"]) >= 1


def axiom_3(model):
    return len(model["V"]) <= 3


def axiom_4(model):
    for v in model["V"]:
        if v in model["T"]:
            return False
    return True


def axiom_5(model):
    for toy in model["T"]:
        found = False
        for b in model["B"]:
            if toy == b[0] and b[1] in model["V"]:
                found = True
        if not found:
            return False
    return True


def axiom_6(model):
    for x in model["B"]:
        for y in model["B"]:
            if x[1] == y[1] and x[0] != y[0] and x[0] in model["T"] and y[0] in model["T"]:
                return False
    return True


def axiom_7(model):
    for x in model["B"]:
        for y in model["B"]:
            if x[1] == y[0] and x[0] == y[1]:
                return False
    return True


def axiom_8(model):
    for x in model["B"]:
        for y in model["B"]:
            if x[1] == y[0]:
                for z in model["B"]:
                    if x[0] == z[0] and y[1] == z[1]:
                        return False
    return True


def axiom_9(model):
    for x in model["B"]:
        for y in model["B"]:
            if x[1] == y[0]:
                for z in model["B"]:
                    if y[1] == z[0]:
                        return False
    return True


def axiom_10(model):
    for x in model["B"]:
        for y in model["B"]:
            if x[1] != y[1] and x[0] == y[0]:
                return False
    return True


def axiom_11(model):
    f_s = []
    for d in model["DOMAIN"]:
        not_on = True
        for b in model["B"]:
            if d == b[0]:
                not_on = False
        if not_on:
            f_s.append(d)
    return len(f_s) == 1