import math
from time import time
from Input import inputFunction
from Trie import Node, insertInTrie, updateTrie, travarseTrie

freq = {}
transactions = []
itemSet = []
min_support = 0

def isOk(L1, L2):
    for i in range(0, len(L1)-1):
        if L1[i] != L2[i]:
            return False

    return L1[len(L1)-1] < L2[len(L2)-1]


def candidateGeneration():
    newCandidate = []
    for i in range(0, len(itemSet)):
        for j in range(i+1, len(itemSet)):
            if isOk(itemSet[i], itemSet[j]):
                tmp = itemSet[i] + itemSet[j][len(itemSet[j])-1:]
                newCandidate.append(tmp)

    return newCandidate


def hasInfrequentSubset(itemList):
    for i in range(0, len(itemList)):
        tmp = itemList[:i] + itemList[i+1:]
        tmp = str(tmp)
        if (tmp not in freq) or (freq[tmp] < min_support):
            return True

    return False


def pruning(itemList):
    newItemList = []
    for item in itemList:
        if hasInfrequentSubset(item) == False:
            newItemList.append(item)

    global itemSet
    for item in itemSet:
        del freq[str(item)]
    itemSet = newItemList


def Apriori():
    global itemSet
    level = 1
    tmp = []
    afterJoin = len(itemSet)
    afterPrune = 0
    actualItemCnt = 0
    total = 0

    # Level-1
    for item in itemSet:
        if freq[str(item)] >= min_support:
            tmp.append(item)
        else:
            del freq[str(item)]
    itemSet = tmp
    itemSet.sort()
    # print(itemSet)
    afterPrune = len(itemSet)
    actualItemCnt = afterPrune
    total += actualItemCnt
    print("Level - " + str(level) + " | After Join - " + str(afterJoin) + " | After Prune - " + str(afterPrune) + " | Actual Frequent - " + str(actualItemCnt))

    while len(itemSet) > 0:
        level += 1
        newItemSet = candidateGeneration()
        # print(newItemSet)
        afterJoin = len(newItemSet)

        pruning(newItemSet)
        # print(itemSet)
        afterPrune = len(itemSet)

        root = Node(-1)
        for item in itemSet:
            insertInTrie(root, item)

        for transaction in transactions:
            updateTrie(root, transaction, 0, 0)

        # print(freq)
        travarseTrie(root, [], freq)
        # print(freq)
        del root

        tmp = []
        for item in itemSet:
            if freq[str(item)] >= min_support:
                tmp.append(item)
        itemSet = tmp
        actualItemCnt = len(itemSet)
        total += actualItemCnt
        # print(itemSet)
        print("Level - " + str(level) + " | After Join - " + str(afterJoin) + " | After Prune - " + str(afterPrune) + " | Actual Item Count - " + str(actualItemCnt))

    print("Total - " + str(total))


def main():
    print("Select Dataset:")
    print("1. book.dat")
    print("2. mushroom.dat")
    print("3. chess.dat")
    print("4. connect.dat")
    print("5. pumsb_star.dat")
    print("6. retail.dat")

    d = input()
    d = int(d)
    if d == 1:
        inputFunction("../Dataset/book.dat", transactions, itemSet, freq)
    elif d == 2:
        inputFunction("../Dataset/mushroom.dat", transactions, itemSet, freq)
    elif d == 3:
        inputFunction("../Dataset/chess.dat", transactions, itemSet, freq)
    elif d == 4:
        inputFunction("../Dataset/connect.dat", transactions, itemSet, freq)
    elif d == 5:
        inputFunction("../Dataset/pumsb_star.dat", transactions, itemSet, freq)
    elif d == 6:
        preProcess("../Dataset/retail.dat", transactions, items, freq)

    print("Enter Threshold:")
    threshold = input()
    threshold = float(threshold)
    threshold = math.ceil((threshold * float(len(transactions))/100.0))
    global min_support
    min_support = int(threshold)

    start = time()
    Apriori()
    end = time()
    print("Execution Time = " + str(end - start))


if __name__ == main():
    main()
