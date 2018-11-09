#import cv2
import numpy as np
import matplotlib.pyplot as plt
import random

from PIL import Image
class DNA:

    dnaBits=30
    def __init__(self):
        self.p1 = []
        self.p2 = []
        self.p3 = []
        self.fitnessScore = 999
        for i in range(self.dnaBits):
            self.p1.append(self.coin())
            self.p2.append(self.coin())
            self.p3.append(self.coin())


    def coin(self):
        x = random.random()
        if x < 0.5:
            return 1
        else:
            return 0
    def gene2val(self,dna,*limit):
        (a,b) = limit
        n = self.dnaBits
        m = 2**n-1
        r = int(''.join(str(i) for i in dna ),2)
        x = a +r/m *(b-a)
        return x

    def calculateFitness(self,imo,imc):

        print("-----------------------------")

        p1 = self.gene2val(self.p1, 0, 30)
        p2 = self.gene2val(self.p2, 0, 0.01)
        p3 = self.gene2val(self.p3, 0, 0.01)
        noise_params = (p1, p2, p3)
        GAnoise = make_noise(imo.shape, noise_params)
        Cim = corrupt_image(imo, GAnoise)
        d = im_diff(Cim, imc)
        print("get dna  p1:%f,p2:%f,p3:%f" % ( p1, p2, p3))
        return d

    def corrupt_image(self,im, noise):  # add noise to every pixel
        im_noisy = im + noise
        return im_noisy

    def im_diff(self,a, b):  # return difference make it between 0 and 1
        d = np.abs(a - b)
        d = np.sum(d)
        n, m = a.shape
        M = n * m * 255
        d = d / M  # [0,1]
        return d

    def make_noise(self,im_size, noise_params):
        # print("make_noise called")
        rows, cols = im_size
        N = np.zeros(im_size)
        NoiseAmp, NoiseFreqRow, NoiseFreqCol = noise_params
        # boardcasting
        row, col = np.arange(rows), np.arange(cols).reshape(rows, 1)
        # print("row shape:"+str(row.shape)+"col shape:"+str(col.shape))
        N = 2 * np.pi * NoiseFreqRow * row + 2 * np.pi * NoiseFreqCol * col
        #  print("N shape:"+str(N.shape)+"type:"+str(type(N)))
        N = NoiseAmp * np.sin(2 * np.pi * NoiseFreqRow * row + 2 * np.pi * NoiseFreqCol * col)

        return N
prob_crossover = 0.80
prob_mutation = 0.05
iterations_limit = 10


def randomIdx(N):
    x = random.random()
    idx = int(x * N)
    return idx


def imread(fn):return np.array(Image.open(fn).convert("L"),dtype=np.float)

def tournament(fitness_population) :


    n = len(fitness_population)
    # add fit guys
    strong  =None
    strong_fitness = 999
    for i in range(n) :
        # 1. select 2 guys
        d1 = random.choice(fitness_population)
        d2 = random.choice(fitness_population)
        (f1, c1),(f2,c2) = (d1.fitnessScore, d1),(d2.fitnessScore,d2)
        # 2. pick the stranger
        temp = c1
        temp_fitness = f1
        if f1 > f2 :
            temp = c2
            temp_fitness = f2
        if temp_fitness< strong_fitness :
            strong = temp
            strong_fitness = temp_fitness
        # 3. add to "selected_population"

    return strong
def selection(population) :
    npopulation = []
    N = len(population)
    for i in range(N):
        p1 = random.choices(population,k=int(randomIdx(N))+1) #make sore not zaro
        p2 = random.choices(population,k=int(randomIdx(N))+1)

        c1 = tournament(p1)
        c2 = tournament(p2)

        npopulation.append((c1,c2))
    return npopulation
def crossover(c1, c2):
    n = len(c1)
    i = randomIdx(n)
    nc1 = c1[ :i] + c2[i: ]
    nc2 = c2[ :i] + c1[i: ]
    return nc1, nc2

def mutation(c) :
    n = len(c)
    i = randomIdx(n)
    mc = c[:] #COPY THE WHOLE THINGS
    mc[i] = 1 - mc[i]
    return mc
def breed_population(parent_pairs):
    size = len(parent_pairs)
    next_population = []
    for k in range(size):
        (d1,d2) = parent_pairs[k]
        cross = random.random() < prob_crossover

        if cross:

            d1p1 = d1.p1
            d2p1 = d2.p1
            (nd1p1, nd2p1) = crossover(d1p1, d2p1)

            # -----
            d1p2 = d1.p2
            d2p2 = d2.p2
            (nd1p2, nd2p2) = crossover(d1p2, d2p2)

            # ------
            d1p3 = d1.p3
            d2p3 = d2.p3
            (nd1p3, nd2p3) = crossover(d1p3, d2p3)

            d1.fitnessScore = 999
            d2.fitnessScore = 999
            mutate = random.random() < prob_mutation
            if mutate:
               nd1p1= mutation(nd1p1)
               nd1p2 = mutation(nd1p2)
               nd1p3 = mutation(nd1p3)
               nd2p1 = mutation(nd2p1)
               nd2p1 = mutation(nd2p1)
               nd2p1 = mutation(nd2p1)
               d1.p1 = nd1p1
               d1.p2 = nd1p2
               d1.p3 = nd1p3
               d2.p1 = nd2p1
               d2.p2 = nd2p2
               d2.p3 = nd2p3
        next_population.append(d1)
        next_population.append(d2)
    return next_population

fn = '/Users/RyanTsai/PycharmProjects/GA/lena.png'
imo = imread(fn)
fn2 = '/Users/RyanTsai/PycharmProjects/GA/lenaN.png'
imc = imread(fn2)
# print('im type:'+str(type(im))+'im shape:'+str(im.shape))




# imA = Image.fromarray(Cim)
# imA.show()
populationSize = 20
population = []
bestpopu = []
#ini polulation
for i in range(populationSize):
    population.append(DNA())
print("-----------------------------")
print("gene new popu")
for j in range(iterations_limit):
    #calculate fitness

    # population.sort(reverse=False, key=lambda dna: dna.fitnessScore)
    print("-----------------------------")
    print("iteration count: %d" % j)
    print("-----------------------------")
    print("the best in this iteation fitness score: %f" % population[0].fitnessScore)
    # bestpopu.append(population[0])
    parents = selection(population)
    population = breed_population(parents)
population.sort(reverse=False, key=lambda dna: dna.fitnessScore)
bestdna = population[0]
p1 = bestdna.gene2val(bestdna.p1,0,30)
p2 = bestdna.gene2val(bestdna.p2,0,0.01)
p3 = bestdna.gene2val(bestdna.p3,0,0.01)
noise_params = (p1,p2,p3)
GAnoise = make_noise(imo.shape,noise_params)
Cim = corrupt_image(imo,GAnoise)
imA = Image.fromarray(Cim)
imA.show()
# print(bestpopu)