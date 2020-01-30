from time import time
from kMeans import kMeans
from kMedoids import PAM
from MeasurementCalculation import calcPurity, calcBCubedPrecision, calcHopkinsStatistic


def readDataFile(filePath, supervised):
    data = []
    classLabel = {}
    cnt = 0

    fp = open(filePath, "r")

    for line in fp:
        # print(line)
        tmp = line[0 : len(line)-1] # removing last newline character
        tmp = tmp.split(",")
        # print(tmp)

        if supervised == True:
            list = [float(tmp[i]) for i in range(0, len(tmp)-1)]
            classLabel[cnt] = tmp[len(tmp)-1]
            cnt += 1
        else:
            list = [float(tmp[i]) for i in range(0, len(tmp))]

        data.append(list)

    # print(data)
    # print(classLabel)

    return data, classLabel


def checkDataset(data):
    score = 0
    for i in range(0, 5):
        score += calcHopkinsStatistic(data)

    score /= 5.0
    print("Average Hopkins Score: " + str(score))


def main():
    k = input("Enter the value of k: ")
    k = int(k)

    print("Select Dataset:")
    print("1. iris")
    print("2. wine")
    print("3. glass")
    # print("4. seeds")
    # print("5. Sales Transactions")
    d = input()
    d = int(d)

    filePath = ""
    if d == 1:
        filePath = "Datasets/iris.data"
    elif d == 2:
        filePath = "Datasets/wine.data"
    elif d == 3:
        filePath = "Datasets/glass.data"
    # elif d == 4:
    #     filePath = "Datasets/seeds.txt"
    # else:
    #     filePath = "Datasets/Sales_Transactions_Dataset_Weekly.txt"
    else:
        return

    supervised = True
    if d == 5:
        supervised = False

    data, classLabel = readDataFile(filePath, supervised)
    # print(data)
    # print(len(data))
    # print(classLabel)

    checkDataset(data)
    # return

    start = time()
    print("k Means:")
    clusterID, clusterList = kMeans(data, k)
    end = time()
    calcPurity(classLabel, clusterID, clusterList, k)
    calcBCubedPrecision(classLabel, clusterID)
    print("Execution Time: " + str(end - start))

    print("k Medoids:")
    start = time()
    clusterID, clusterList = PAM(data, k)
    end = time()
    calcPurity(classLabel, clusterID, clusterList, k)
    calcBCubedPrecision(classLabel, clusterID)
    print("Execution Time: " + str(end - start))


if __name__ == main():
    main()
