import random
import matplotlib.pyplot as plt


def chooseInitialClusterCentroids(data, k):
    centroidsCoordinate = []

    list = random.sample(range(0, len(data)), k)
    for i in list:
        centroidsCoordinate.append(data[i])

    # print(centroidsCoordinate)

    return centroidsCoordinate


def getEuclideanDistance(point1, point2):
    dist = 0
    for i in range(0, len(point1)):
        x = point1[i] - point2[i]
        dist += (x * x)

    # print(dist)

    return dist


def getSum(point1, point2):
    sum = []
    for i in range(0, len(point1)):
        x = point1[i] + point2[i]
        sum.append(x)

    # print(sum)

    return sum


def updateCluster(data, centroidsCoordinate, k):
    clusterID = {}
    clusterList = []
    for i in range(0, k):
        clusterList.append([])

    for i in range(0, len(data)):
        indx = -1
        minDist = 0
        for j in range(0, k):
            dist = getEuclideanDistance(data[i], centroidsCoordinate[j])
            if indx == -1 or minDist > dist:
                indx = j
                minDist = dist

        clusterID[i] = indx
        clusterList[indx].append(i)

    # print(clusterID)
    # print(clusterList)

    return clusterID, clusterList


def updateCentroids(data, clusterList, k):
    newCentroidsCoordinate = []

    for i in range(0, k):
        sum = []
        flag = False
        for j in range(0, len(clusterList[i])):
            if flag == False:
                flag = True
                sum = data[clusterList[i][j]]
            else:
                sum = getSum(sum, data[clusterList[i][j]])

        if flag == True:
            for j in range(0, len(sum)):
                sum[j] /= float(len(clusterList[i]))

        newCentroidsCoordinate.append(sum)

    # print(newCentroidsCoordinate)

    return newCentroidsCoordinate


def isSame(prevCentroidsCoordinate, newCentroidsCoordinate, k):
    error = 0
    for i in range(0, k):
        error += getEuclideanDistance(prevCentroidsCoordinate[i], newCentroidsCoordinate[i])

    if error == 0:
        return True

    return False


def getWCV(data, clusterID, centroidsCoordinate):
    error = 0
    for i in range(0, len(data)):
        error += getEuclideanDistance(data[i], centroidsCoordinate[clusterID[i]])

    return error


def makePlot(iterationList, wcvList):
    # print(wcvList)

    plt.plot(iterationList, wcvList)
    plt.xlabel("Iteration")
    plt.ylabel("WCV")
    plt.show()


def kMeans(data, k):
    centroidsCoordinate = chooseInitialClusterCentroids(data, k)
    clusterID = {}
    clusterList = []
    wcvList = []
    iterationList = []
    itr = 0

    while True:
        clusterID, clusterList = updateCluster(data, centroidsCoordinate, k)
        wcvList.append(getWCV(data, clusterID, centroidsCoordinate))
        iterationList.append(itr)
        prevCentroidsCoordinate = centroidsCoordinate
        centroidsCoordinate = updateCentroids(data, clusterList, k)

        if isSame(prevCentroidsCoordinate, centroidsCoordinate, k) == True:
            break

        itr += 1

    makePlot(iterationList, wcvList)

    return clusterID, clusterList
