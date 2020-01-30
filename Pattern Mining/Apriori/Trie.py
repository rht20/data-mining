class Node(object):
    def __init__(self, val):
        self.val = val
        self.child = []
        self.cnt = 0
        self.finished = False


def insertInTrie(root, itemList):
    node = root
    for item in itemList:
        found = False
        for child in node.child:
            if child.val == item:
                found = True
                node = child
                break
        if not found:
            newNode = Node(item)
            node.child.append(newNode)
            node = newNode
    node.finished = True


def updateTrie(root, itemList, pos1, pos2):
    if root.finished == True:
        root.cnt += 1
        return

    if pos1 >= len(root.child):
        return
    if pos2 >= len(itemList):
        return

    if root.child[pos1].val == itemList[pos2]:
        updateTrie(root.child[pos1], itemList, 0, pos2+1)
        updateTrie(root, itemList, pos1+1, pos2+1)
    elif root.child[pos1].val < itemList[pos2]:
        updateTrie(root, itemList, pos1+1, pos2)
    else:
        updateTrie(root, itemList, pos1, pos2+1)


def travarseTrie(node, itemList, freq):
    if node.finished == True:
        # print(str(itemList) + " " + str(node.cnt))
        freq[str(itemList)] = node.cnt
        return

    for child in node.child:
        itemList.append(child.val)
        travarseTrie(child, itemList, freq)
        itemList.pop(len(itemList)-1)

