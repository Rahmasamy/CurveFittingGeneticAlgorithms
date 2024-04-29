import random
import os
import sys
allInputFile=[]
number_Of_Chromsomes = 5
degree = 2
lb = -10
upb = 10
datapoints = [[1, 5], [2, 8], [3, 13], [4, 20], [9, 0]]
parent1 = []
listoflist = []
parent2 = []
p1 = []
p2 = []
Bfactor = 1
Max_generation = 20
flaglower = 1
population = 20
elitecharge = 0.05 * population
round_elite_charge = round(elitecharge) + 1


# helper function
def Sort(sub_list):
    # reverse = None (Sorts in Ascending order)
    # key is set to sort using second element of
    # sublist lambda has been used
    sub_list.sort(key=lambda x: x[-1], reverse=True)
    return sub_list


def readFile():
    listFile = []
    listFile.clear()
    f = open("C:/Users/Owner/Downloads/assig2dataset.txt", "r")
    for i in f:
        string = i.strip("\n")
        listFile.append(string.split())

    f.close()
    return listFile


allInputFile = (readFile())

# step 1
def intializematrix(degree):
    parents = []
    for i in range(0, number_Of_Chromsomes):
        parent = []
        for j in range(0, degree + 1):
            k = random.uniform(lb, upb)
            parent.append(k)
        parents.append(parent)
    return parents


###########################################################################
# step 2
def fitness(inittmatrix):
    datasingle = []
    fitness_list = []
    list2 = []
    sum = 0
    error = 0
    totalerror = 0
    fitness_prob = 0

    for i in range(0, len(inittmatrix)):
        c1 = inittmatrix[i]  # c1 carry list for every chromsome c1,c2,c3,c4
        d = datapoints[i]  # d carry list for every data point
        for j in range(degree + 1):  # loop through one chromsome c1 etc
            if j == 0:  # bias
                sum = c1[j]
            else:
                sum += c1[j] * d[0] ** j
                sum -= d[1]
                error = sum ** 2
        totalerror = error / number_Of_Chromsomes
        fitness_prob = 1 / totalerror
        print(f"the total error for {i + 1} chromsome is  {totalerror}")
        print(f"the total fitness for {i + 1} chromsome is  {fitness_prob}")
        print("==========================================================")
        c1.append([fitness_prob])
        print("the parent with probability is :", c1)
        list2.append(c1)
        print("the total append for probaility and parent", list2)

    return list2


# step 3
# tourment-selection
def tourment_selection(degree=2):
    fit_list = []
    sorted = []
    d1 = intializematrix(degree)
    fit_list = fitness(d1)
    parents = random.choices(fit_list, k=4)
    sorted = Sort(parents)
    return sorted


# step 4
def cross_over(parent1, parent2):
    p_new = []
    p_new_2 = []
    if len(parent1) == 3 and len(parent2) == 3:
        temp = parent2[1:2]
        p_new.extend(parent1[:1])
        p_new.extend(temp)
        p_new.extend(parent1[2:])
        temp2 = parent1[1:2]
        p_new_2.extend(parent2[:1])
        p_new_2.extend(temp2)
        p_new_2.extend(parent2[2:])
        return p_new, p_new_2

    else:
        degree = 3
        dg = degree
        p_new.extend(parent1[:1])  # p new 5.490
        p_new_2.extend(parent2[:1])  # pnew2 5.739
        p_new.extend(parent2[1:dg])  # pnew -5.4 -2.9 -3.27
        p_new_2.extend(parent1[1:dg])  # pnew2 5.7 9.07 -7.51
        p_new.extend(parent1[dg:])  # pnew -5.4 9.7 -7.5
        p_new_2.extend(parent2[dg:])
        return p_new, p_new_2


def mutation(cross_list1, cross_list2):
    delta_l_list = []
    delta_u_list = []
    delta_l_list_2 = []
    delta_u_list_2 = []
    y1 = []
    y2 = []
    mutation_list = []
    mutation_list_2 = []
    x_new_list_p1 = []
    x_new_list_p2 = []
    r = random.uniform(0, 1)
    for i in cross_list1:
        delta_L = i - lb
        delta_U = upb - i
        delta_l_list.append(delta_L)
        delta_u_list.append(delta_U)
    for j in cross_list2:
        delta_L_2 = j - lb
        delta_U_2 = upb - j
        delta_l_list_2.append(delta_L_2)
        delta_u_list_2.append(delta_U_2)
    # generate random number from 0 to 1
    r2 = random.uniform(0, 1)

    if r2 < 0.5:
        y1 = delta_l_list  # carry list of deleta lower
        y2 = delta_l_list_2
        flaglower = 0


    else:
        y1 = delta_u_list  # carry list of delta upper
        y2 = delta_u_list_2
        flaglower = 1

    r22 = random.uniform(0, 1)
    for i in range(0, len(y1)):
        div = (1 - i) / Max_generation
        divb = div ** Bfactor
        r3 = r22 ** divb
        n = 1 - r3
        final = y1[i] * n
        final2 = y2[i] * n
        mutation_list.append(final)
        mutation_list_2.append(final2)
    ele = 0
    for i in cross_list1:
        if flaglower == 0:
            xnew = i - y1[ele]
            xnew2 = i - y2[ele]
            ele += 1
            x_new_list_p1.append(xnew)
            x_new_list_p2.append(xnew2)
        else:
            xnew = y1[ele] - i
            xnew2 = y2[ele] - i
            ele += 1
            x_new_list_p1.append(xnew)
            x_new_list_p2.append(xnew2)
    return x_new_list_p1, x_new_list_p2


def replacement(degree):
    for i in range(0, 20):
        list_fadia = []
        list_fadia_3 = []
        list_fadia_4 = []
        matrix = []
        newElite = []
        total = []
        o = 0
        list_fadia_2 = []  # carry third,fourth,.... for the fitness nad crossover
        x1 = tourment_selection(degree)  # 4 list sorting descending acording fitness
        l3 = []
        new_elite = x1[:round_elite_charge]  # round 2
        for i in range(0, round_elite_charge):  # pick the elites from the x1
            newElite = new_elite[i]
            matrix.append(newElite)
            total.extend(matrix[i][-1])  # total carry fitness probability for eleite
            # take row of it each elite
            list_fadia.append(newElite[:-1])  # append to list and make -1 to remove fitness

        for i in range(round_elite_charge, len(x1)):
            # move on the rest of x1 (take it and perform cross over and mutation )
            newx = x1[i]
            list_fadia_2.append(newx[:-1])
        o = len(list_fadia_2)
        # len=2
        newo = o - 1
        for i in range(0, len(list_fadia_2)):

            if i < newo:
                co = cross_over(list_fadia_2[i], list_fadia_2[i + 1])
                mutate = co[i]
                mutate2 = co[i + 1]
                m1, m2 = mutation(mutate, mutate2)
                list_fadia_3.append(m1)
                list_fadia_3.append(m2)
                l = fitness(list_fadia_3)
                for index in range(0, len(l)):
                    l3.append(l[index][3])



        else:  # i the last index in the matrix

            co2 = cross_over(list_fadia_2[i], list_fadia_2[0])  # co2  []=co2[0]  []=co2[1]
            m3, m4 = mutation(co2[0], co2[1])  # 1,2
            list_fadia_4.append(m3)
            list_fadia_4.append(m4)
            l2 = fitness(list_fadia_4)
            # sort acording to the greatest fitness
            t2 = Sort(l2)
            for index in range(0, len(l2)):
                l3.append(l2[index][3])

            m = max(l3)

        # total =====> fitness probabilty ellite # elite
        # t2========> sort after mutation according to fitness(rest ofthe fitness)
        # l3 ========> fitness for rest of the matrix
        # m=========> maximum fitness in the rest of the matrix

        x = t2[0][:-1]  # parent for max fitness
        if total[0] < m[0]:
            total[0] = m  # new elites but for probability
            # v2=total[0] when we use v1,v2 use * to the value without square brackets
            list_fadia[0] = x

        elif total[1] < m[0]:
            total[1] = m
            list_fadia[1] = x

    return list_fadia[0]


ii = 0
path = "C:/Users/Owner/Downloads/assig2dataset.txt"
f = open(path, "r")
numofdatasets = int(f.readline())

while ii < numofdatasets:
    x = f.readline()
    numofdatapoints = int(float(x[:2]))
    degreee = int(float(x[3:]))
    print("the best coffients are", replacement(degree), "we are in the data set index :", ii, )

    ii += 1
