import matplotlib.pyplot as plt


def getEuclideanDistance(point1, point2):
    dist = 0
    for i in range(0, len(point1)):
        x = point1[i] - point2[i]
        dist += (x * x)

    # print(dist)

    return dist


def updateClosestMedoids(data, distance, medoids):
    closestMedoidInfo = {}

    for i in range(0, len(data)):
        id1 = -1
        id2 = -1
        min1 = 0
        min2 = 0
        for j in medoids:
            d = distance[(i, j)]
            if id1 == -1 or min1 > d:
                id2 = id1
                min2 = min1
                id1 = j
                min1 = d
            elif id2 == -1 or min2 > d:
                id2 = j
                min2 = d

        closestMedoidInfo[i] = [(id1, min1), (id2, min2)]

    return closestMedoidInfo


def build(data, distance, k):
    mark = {}
    medoids = []
    for i in range(0, len(data)):
        mark[i] = False

    indx = -1
    minDistSum = 0
    for i in range(0, len(data)):
        distSum = 0
        for j in range(0, len(data)):
            distSum += distance[(i, j)]

        if indx == -1 or minDistSum > distSum:
            indx = i
            minDistSum = distSum

    mark[indx] = True
    medoids.append(indx)

    closestMedoidInfo = {}
    for i in range(0, len(data)):
        closestMedoidInfo[i] = [(indx, distance[(i, indx)]), (-1, 0)]

    for i in range(1, k):
        indx = -1
        mxGain = 0
        for p in range(0, len(data)):
            if mark[p] == True:
                continue

            gain = 0
            for q in range(0, len(data)):
                if mark[q] == True:
                    continue

                d = distance[(p, q)]
                if d < closestMedoidInfo[q][0][1]:
                    gain += (closestMedoidInfo[q][0][1] - d)

            if indx == -1 or mxGain < gain:
                indx = p
                mxGain = gain

        mark[indx] = True
        medoids.append(indx)

        for j in range(0, len(data)):
            d = distance[(j, indx)]
            if d < closestMedoidInfo[j][0][1]:
                pr = closestMedoidInfo[j][0]
                closestMedoidInfo[j] = [(indx, d), pr]
            elif closestMedoidInfo[j][1][0] == -1 or closestMedoidInfo[j][1][1] > d:
                pr = closestMedoidInfo[j][0]
                closestMedoidInfo[j] = [pr, (indx, d)]

    return medoids, mark, closestMedoidInfo


def getWCV(data, closestMedoidInfo):
    error = 0
    for i in range(0, len(data)):
        error += closestMedoidInfo[i][0][1]

    return error


def swap(data, distance, medoids, mark, closestMedoidInfo, k):
    halt = False
    itr = 0
    wcvList = []
    iterationList = []

    while halt == False:
        halt = True

        wcvList.append(getWCV(data, closestMedoidInfo))
        iterationList.append(itr)
        itr += 1

        indxI = -1
        indxH = -1
        mxContribution = 0
        for i in range(0, k):
            for h in range(0, len(data)):
                if mark[h] == True:
                    continue

                contribution = 0
                for j in range(0, len(data)):
                    # if mark[j] == True:
                    #     continue

                    d = distance[(j, h)]
                    if closestMedoidInfo[j][0][0] == medoids[i]:
                        contribution += (min(closestMedoidInfo[j][1][1], d) - closestMedoidInfo[j][0][1])
                    elif d < closestMedoidInfo[j][0][1]:
                        contribution += (d - closestMedoidInfo[j][0][1])

                if indxI == -1 or mxContribution > contribution:
                    indxI = i
                    indxH = h
                    mxContribution = contribution

        if mxContribution < 0:
            mark[indxH] = True
            mark[medoids[indxI]] = False
            medoids[indxI] = indxH
            closestMedoidInfo = updateClosestMedoids(data, distance, medoids)
            halt = False

    return medoids, closestMedoidInfo, iterationList, wcvList


def makePlot(iterationList, wcvList):
    # print(wcvList)

    plt.plot(iterationList, wcvList)
    plt.xlabel("Iteration")
    plt.ylabel("WCV")
    plt.show()


def PAM(data, k):
    distance = {}
    for i in range(0, len(data)):
      for j in range(0, len(data)):
        distance[(i, j)] = getEuclideanDistance(data[i], data[j])
    
    medoids, mark, closestMedoidInfo = build(data, distance, k)
    medoids, closestMedoidInfo, iterationList, wcvList = swap(data, distance, medoids, mark, closestMedoidInfo, k)

    mp = {}
    for i in range(0, len(medoids)):
      mp[medoids[i]] = i

    clusterID = {}
    clusterList = []
    for i in range(0, k):
      clusterList.append([])

    for i in range(0, len(data)):
      clusterID[i] = mp[closestMedoidInfo[i][0][0]]
      # print(str(closestMedoidInfo[i][0][0])+" "+str(mp[closestMedoidInfo[i][0][0]]))
      clusterList[mp[closestMedoidInfo[i][0][0]]].append(i)

    makePlot(iterationList, wcvList)

    return clusterID, clusterList
