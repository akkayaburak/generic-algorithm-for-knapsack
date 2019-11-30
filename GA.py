
import math
import csv
import sys
filepath = sys.argv[-1]
with open(filepath) as f:
    randomList = f.readline()
    populationSize = int(f.readline())
    k = int(f.readline())
    probMutation = f.readline()
    iterationCount = int(f.readline())
    bagSize = int(f.readline())
    elementWeight = f.readline()
    elementValue = f.readline()
    f.close()
randomList = randomList.strip()
randomList = randomList.split(",")
elementWeight = elementWeight.strip()
elementWeight = elementWeight.split(",")
elementValue = elementValue.strip()
elementValue = elementValue.split(",")
allFitness = []
def initialize():
    population = []
    x=0
    for i in range(populationSize):
        element = []
        for j in range (len(elementWeight)):
            if x >= len(randomList):
                x=0
            if float(randomList[x]) < 0.5:
                element += '0'
            else:
                element += '1'
            x= x+1
        element = [int (z) for z in element]
        population.append(element)
    #print(population[i][0])
    return population

def evaluate (population):
    weights = []
    fitness = []
    for i in range(populationSize):
        weights.append(0)
        sumFitness = 0
        for j in range(len(elementWeight)):
            weights[i] += int(elementWeight[j]) * population[i][j]
            sumFitness += int(elementValue[j]) * population[i][j]
        if weights[i] > bagSize:
            fitness.append(0)
        else:
            fitness.append(sumFitness)
    return fitness

def parentSelect(fitness,population):
    x=0
    parents = []
    for i in range(populationSize):
        tmp = [] # index
        tmpFitness = []
        for j in range(k):
            if x >= len(randomList):
                x = 0
            tmp.append((math.ceil(float(randomList[x]) * populationSize)) -1 )
            tmpFitness.append(fitness[tmp[j]])
            x = x+1
        parents.append(population[tmp[tmpFitness.index(max(tmpFitness))]])
    return parents

def recombine(parents):
    x=0
    #print('Applying Crossover ')
    crossedParents = []
    for i in range (0,populationSize,2):
        if populationSize % 2 == 1 and i == populationSize -1:
            crossedParents.append(parents[i])
            break
        #print('Parents :' , parents [i] , parents[i+1] ,'\n')
        if x >= len(randomList):
            x=0
        location = (math.ceil(float(randomList[x]) * populationSize)) - 1
        firstChild = parents [i][0 : location+1 ] + parents [i+1][location+1  :]
        crossedParents.append(firstChild)
        secondChild = parents [i+1] [0 : location+1] + parents [i] [location+1 : ]
        crossedParents.append(secondChild)
        #print('Children : ' , firstChild , secondChild , '\n')
        x = x+1
    #print(len(crossedParents))
    return crossedParents
def mutation(crossedParents):
    #print('Applying mutation to :' , crossedParents , '\n')
    x=0
    for i in range(populationSize):
        for j in range (len(elementValue)):
            if x >= len(randomList):
                x=0
            if randomList[x] < probMutation:
                if crossedParents [i] [j] == 0:
                    crossedParents [i] [j] = 1
                else:
                    crossedParents [i] [j] = 0
            x= x+1
    # print('Mutated offspring : ' , crossedParents , '\n\n')
    return crossedParents
def survivalSelect(crossedParents,fitnessCrossedParents, population , fitnessPopulation ):
    newPopulation = crossedParents + population
    newPopulationFitness = fitnessCrossedParents + fitnessPopulation
    for i in range(len(newPopulation)):
        min_idx = 1
        for j in range(i+1, len(newPopulation)):
            if newPopulationFitness[min_idx] > newPopulationFitness [j]:
                min_idx = j
        newPopulation [i] , newPopulation[min_idx] = newPopulation[min_idx] , newPopulation [i]
        newPopulationFitness [i] , newPopulationFitness [min_idx] = newPopulationFitness[min_idx] , newPopulationFitness [i]
    return (newPopulation[-populationSize:  ] , newPopulationFitness [-populationSize: ])


def main():
    population = initialize()
    fitnessPopulation = evaluate(population)
    for i in range(iterationCount):
        tmp = []
        parents = parentSelect(fitnessPopulation,population)
        # print('Generation ', i+1)
        # print('Population : ')
        # for j in range(populationSize):
        #     print(population[j], fitnessPopulation[j])
        #print('\n')
        crossedParents = recombine(parents)
        crossedParents = mutation(crossedParents)
        fitnessCrossedParents = evaluate(crossedParents)
        population , fitnessPopulation = survivalSelect(crossedParents, fitnessCrossedParents, population, fitnessPopulation)
        tmp.append(i)
        tmp.append(min(fitnessPopulation))
        tmp.append(int(sum(fitnessPopulation) / populationSize))
        tmp.append(max(fitnessPopulation))
        allFitness.append(tmp)
    #print('Final Population : ')
    for z in range(populationSize):
        print(population[z], fitnessPopulation[z])
    #print(allFitness)
    with open ('H2.csv','w') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerows(allFitness)

if __name__ == '__main__':
    main()

