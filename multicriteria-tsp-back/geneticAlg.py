import random
import numpy as np


def processing(matrix, main_criteri, popsize=10,
               multprod=0.5, elite=0.5, maxiter=100):
    def get_distance(path):
        S = 0.0
        for i in range(len(path) - 1):
            line = matrix[path[i]][path[i + 1]]
            if line is None:
                S += float('inf')
            else:
                S += line[main_criteri]
        line = matrix[path[-1]][0]
        if line is None:
            S += float('inf')
        else:
            S += line[main_criteri]
        return S

    def mutate(gen):
        gen_copy = gen.copy()
        i = random.randint(1, len(gen) - 1)
        j = random.randint(1, len(gen) - 1)
        temp = gen_copy[i]
        gen_copy[i] = gen_copy[j]
        gen_copy[j] = temp
        return gen_copy

    def crossover(gen):
        gen_copy = gen.copy()
        i = random.randint(1, len(gen) - 2)
        j = random.randint(i + 1, len(gen) - 1)
        selected_segment_gen = gen_copy[i:j + 1]
        gen_copy[i:j + 1] = np.flip(selected_segment_gen)
        return gen_copy

    pop = []
    while len(pop) < popsize:
        gen = [0] + random.sample(range(1, len(matrix)), len(matrix)-1)
        pop.append(np.array(gen))

    topelite = int(elite * popsize)

    for i in range(maxiter):
        scores = [(get_distance(gen), gen) for gen in
                  pop]
        scores = sorted(scores, key=lambda tup: tup[0],
                        reverse=False)
        ranked = [gen for (s, gen) in
                  scores]
        pop = ranked[0:topelite]

        while len(pop) < popsize:
            c = random.randint(0, topelite - 1)
            if random.random() < multprod:
                gen_mut = mutate(ranked[c])
                pop.append(gen_mut)
            else:
                gen_cross = crossover(ranked[c])
                pop.append(gen_cross)
    return scores[0][1], scores[0][0]
