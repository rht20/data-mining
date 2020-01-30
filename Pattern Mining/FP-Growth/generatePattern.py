from HeaderTableClass import HT_Node
from FP_Tree import Node, insert, traverse, linkedNodeTraverse


def traverseFPTree(node):
    itemList = []
    new_node = node.parent

    while new_node.is_root == False:
        itemList.append(new_node.label)
        new_node = new_node.parent

    return itemList


def projection(node, min_support):
    items = []
    transactions = []
    freq = {}
    tmpList = []
    supportCountList = []
    new_node = node

    while new_node != None:
        itemList = traverseFPTree(new_node)
        # print(itemList)

        for item in itemList:
            if item not in freq:
                items.append(item)
                freq[item] = new_node.support_count
            else:
                freq[item] += new_node.support_count
        tmpList.append(itemList)
        new_node = new_node.next_node
    # print(tmpList)
    # print(freq)

    new_node = node
    for tran in tmpList:
        tmp = []
        for item in tran:
            tmp.append((item, freq[item]))

        tmp.sort(key=lambda x: (-x[1], x[0]))

        tmp2 = []
        for item in tmp:
            if item[1] >= min_support:
                tmp2.append(item[0])
            else:
                break
        transactions.append(tmp2)
        supportCountList.append(new_node.support_count)
        new_node = new_node.next_node

    # print(transactions)

    return transactions, items, freq, supportCountList


def createHeaderTable(items, freq, min_support):
    headerTable = []
    lastNode = {}

    for item in items:
        if freq[item] < min_support:
            continue
        nd = HT_Node(item, freq[item])
        headerTable.append(nd)
        lastNode[item] = nd

    headerTable.sort(key=lambda x: (-x.support_count, x.label))
    # for item in headerTable:
    #     print(str(item.label) + " " + str(item.support_count))

    return headerTable, lastNode


def isSinglePath(node):
    if len(node.child) > 1:
        return False
    elif len(node.child) == 0:
        return True

    return isSinglePath(node.child[0])


def generateCombination(node, pattern):
    if node.is_root == True:
        if len(node.child) > 0:
            return generateCombination(node.child[0], pattern)
        else:
            return []
    else:
        if len(node.child) > 0:
            return generateCombination(node.child[0], pattern) + generateCombination(node.child[0], pattern+[node.label])
        else:
            if len(pattern) > 0:
                return [pattern] + [pattern+[node.label]]
            return [[node.label]]


def process(FPTreeRoot, headerTable, min_support):

    if isSinglePath(FPTreeRoot) == True:
        return generateCombination(FPTreeRoot, [])

    patternList = []
    headerTable.reverse()

    for item in headerTable:
        transactions, items, freq, supportCountList = projection(item.next_node, min_support)
        # print(items)
        # print(transactions)
        # print(freq)

        new_headerTable, new_lastNode = createHeaderTable(items, freq, min_support)

        new_root = Node(-1, None)
        new_root.is_root = True
        insert(new_root, transactions, new_lastNode, supportCountList)
        # print("Tree")
        # traverse(new_root)
        # for item in new_headerTable:
        #     print(str(item.label) + " " + str(item.support_count))
        #     linkedNodeTraverse(item.next_node)

        tmpPatternList = process(new_root, new_headerTable, min_support)
        # print(tmpPatternList)
        for i in range(0, len(tmpPatternList)):
            tmpPatternList[i].append(item.label)

        tmpPatternList.append([item.label])
        patternList += tmpPatternList
        # print(patternList)
        # patternList = []

        del new_root
        del new_headerTable
        del new_lastNode

    return patternList
