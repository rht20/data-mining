import random


def calcPurity(classLabel, clusterID, clusterList, k):
    clusterClass = {}
    for i in range(0, k):
        count = {}
        for item in clusterList[i]:
            if classLabel[item] not in count:
                count[classLabel[item]] = 1
            else:
                count[classLabel[item]] += 1

        mxc = 0
        for item in count:
            if count[item] > mxc:
                clusterClass[i] = item
                mxc = count[item]

    cnt = 0
    for i in range(0, len(classLabel)):
        if classLabel[i] == clusterClass[clusterID[i]]:
            cnt += 1

    purity = float(cnt)/float(len(classLabel))
    print("Purity: " + str(purity))

    return purity


def calcBCubedPrecision(classLabel, clusterID):
    correctness = {}
    for i in range(0, len(classLabel)):
        for j in range(0, len(classLabel)):
            if i != j:
                if classLabel[i] == classLabel[j] and clusterID[i] == clusterID[j]:
                    correctness[(i, j)] = 1
                else:
                    correctness[(i, j)] = 0

    sum = 0
    for i in range(0, len(classLabel)):
        c1 = 0
        c2 = 0
        for j in range(0, len(classLabel)):
            if i != j:
                c1 += correctness[(i, j)]
                if clusterID[i] == clusterID[j]:
                    c2 += 1

        if c2 > 0:
            sum += (float(c1)/float(c2))

    bcp = sum/float(len(classLabel))

    print("BCubed precision: " + str(bcp))


def getEuclideanDistance(point1, point2):
    dist = 0
    for i in range(0, len(point1)):
        x = point1[i] - point2[i]
        dist += (x * x)

    # print(dist)

    return dist


def calcHopkinsStatistic(data):
    m = len(data)
    n = float(m) * 0.2
    n = int(n)

    sampleP = random.sample(range(0, m), n)
    sampleQ = random.sample(range(0, m), n)
    # print(sampleP)
    # print(sampleQ)

    sumX = 0
    for i in sampleP:
        minDist = 0
        flag = False
        for j in range(0, len(data)):
            if i == j:
                continue
            d = getEuclideanDistance(data[i], data[j])
            if flag == False or minDist > d:
                minDist = d
            flag = True

        sumX += minDist

    sumY = 0
    for i in sampleQ:
        minDist = 0
        flag = False
        for j in range(0, len(data)):
            if i == j:
                continue
            d = getEuclideanDistance(data[i], data[j])
            if flag == False or minDist > d:
                minDist = d
            flag = True

        sumY += minDist

    H = float(sumY) / float(sumX + sumY)
    print("Hopkins Statistic: " + str(H))

    return H
