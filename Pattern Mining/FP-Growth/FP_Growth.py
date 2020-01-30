import math
from time import time
from PreProcess import preProcess
from HeaderTableClass import HT_Node
from FP_Tree import Node, insert, traverse, linkedNodeTraverse
from generatePattern import process


def createHeaderTable(items, freq, headerTable, lastNode, min_support):
    for item in items:
        if freq[item] < min_support:
            continue
        nd = HT_Node(item, freq[item])
        headerTable.append(nd)
        lastNode[item] = nd

    headerTable.sort(key=lambda x: (-x.support_count, x.label))
    # for item in headerTable:
    #     print(str(item.label) + " " + str(item.support_count))


def printOutput(frequent_patterns):
    total = 0
    level = 1
    while level in frequent_patterns:
        print("Level - " + str(level) + " | Actual Item Count - " + str(frequent_patterns[level]))
        total += frequent_patterns[level]
        level += 1

    print("Total Frequent - " + str(total))


def main():
    transactions = []
    items = []
    freq = {}

    print("Select Dataset:")
    print("1. book.dat")
    print("2. mushroom.dat")
    print("3. chess.dat")
    print("4. connect.dat")
    print("5. pumsb_star.dat")
    print("6. retail.dat")

    d = input()
    d = int(d)

    print("Enter Threshold:")
    threshold = input()
    threshold = float(threshold)

    if d == 1:
        preProcess("../Dataset/book.dat", transactions, items, freq, threshold)
    elif d == 2:
        preProcess("../Dataset/mushroom.dat", transactions, items, freq, threshold)
    elif d == 3:
        preProcess("../Dataset/chess.dat", transactions, items, freq, threshold)
    elif d == 4:
        preProcess("../Dataset/connect.dat", transactions, items, freq, threshold)
    elif d == 5:
        preProcess("../Dataset/pumsb_star.dat", transactions, items, freq, threshold)
    elif d == 6:
        preProcess("../Dataset/retail.dat", transactions, items, freq, threshold)

    threshold = math.ceil((threshold * float(len(transactions))) / 100.0)
    min_support = int(threshold)

    # print(items)
    # print(transactions)
    # print(freq)
    # print(min_support)

    start = time()

    headerTable = []
    lastNode = {}
    createHeaderTable(items, freq, headerTable, lastNode, min_support)

    root = Node(-1, None)
    root.is_root = True
    insert(root, transactions, lastNode, [])
    # traverse(root)
    # for item in headerTable:
    #     print(str(item.label) + " xxx " + str(item.support_count))
    #     linkedNodeTraverse(item.next_node)

    patternList = process(root, headerTable, min_support)
    # print(patternList)

    mark = {}
    frequent_patterns = {}
    for i in range(0, len(patternList)):
        patternList[i].sort()

    for item in patternList:
        x = str(item)
        if x not in mark:
            mark[x] = True
        else:
            continue

        x = len(item)
        if x not in frequent_patterns:
            frequent_patterns[x] = 1
        else:
            frequent_patterns[x] += 1

    printOutput(frequent_patterns)

    end = time()
    print("Execution Time = " + str(end - start))


if __name__ == main():
    main()
