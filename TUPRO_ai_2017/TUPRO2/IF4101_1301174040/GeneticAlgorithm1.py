import numpy as np
import matplotlib.pyplot as plt
from pylab import meshgrid

function = lambda x1, x2: ((4-(2.1*x1**2)+(x1**4)/3)*x1**2 + x1*x2 + (-4 + (4*x2**2))*x2**2)
a = lambda x1, x2: function(x1,x2)**(-1)
b = lambda f, i: (f[i] / sum(f))

def roulette(fit):
    rndm = np.random.uniform(0,1)
    indv = 0
    
    while rndm > 0:
        rndm -= b(fit,indv)
        
        indv += 1
    print("random:",rndm)
    return indv-1

#crossover
def crossover(parents, offspring_size):
    offspring = np.empty(offspring_size)
    crossover_point = np.uint8(offspring_size[1]/2)

    for k in range(offspring_size[0]):
        parent1_idx = k%parents.shape[0]
        parent2_idx = (k+1)%parents.shape[0]
        offspring[k, 0:crossover_point] = parents[parent1_idx, 0:crossover_point]
        offspring[k, crossover_point:] = parents[parent2_idx, crossover_point:]
    return offspring

#mutation
def mutation(offspring_crossover): 
    for idx in range(offspring_crossover.shape[0]):
        random_value = np.random.uniform(-1.0, 1.0, 1)
        offspring_crossover[idx, 1] = offspring_crossover[idx, 1] + random_value     
    return offspring_crossover

#initial
num_weights = 2
num_parents_mating = 4
population = 10
pop_size = (population, num_weights)
individu = [[np.random.uniform(-3, 3), np.random.uniform(-2, 2)] for i in range(population)]
individu = np.array(individu)
generasi = 10
num_of_parents = 4


best = []
for gen in range(generasi):
    fitness = [a(i[0], i[1]) for i in individu]
    
    print()
    print("generasi",gen+1)
    parents = []
    for i in range(num_of_parents):
        par1 = roulette(fitness)
        parents.append(individu[par1])
    
    parents = np.array(parents)
    
    offspring_crossover = crossover(parents,
    offspring_size=(pop_size[0]-parents.shape[0], num_weights))

    offspring_mutation = mutation(offspring_crossover)
    print("keturunan",offspring_mutation)

    individu[0:parents.shape[0], :] = parents
    individu[parents.shape[0]:, :] = offspring_mutation
    bsf = np.min([function(i[0], i[1]) for i in individu])
    idx = np.argmin([function(i[0], i[1]) for i in individu],axis=0)
    best.append(bsf)
    print("Hasil terbaik : ", bsf, idx)
