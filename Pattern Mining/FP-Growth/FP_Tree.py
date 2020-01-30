class Node(object):
    def __init__(self, label, parent):
        self.label = label
        self.support_count = 1
        self.parent = parent
        self.is_root = False
        self.child = []
        self.next_node = None


def insertInTree(root, itemList, lastNode, support):
    node = root
    for item in itemList:
        found = False
        for child in node.child:
            if child.label == item:
                found = True
                node = child
                if support == 0:
                    node.support_count += 1
                else:
                    node.support_count += support
                break
        if not found:
            new_node = Node(item, node)
            node.child.append(new_node)
            node = new_node
            if support != 0:
                node.support_count = support
            lastNode[item].next_node = node
            lastNode[item] = node


def insert(root, transactions, lastNode, supportCountList):
    i = 0
    for transaction in transactions:
        if len(supportCountList) == 0:
            insertInTree(root, transaction, lastNode, 0)
        else:
            insertInTree(root, transaction, lastNode, supportCountList[i])
            i += 1


def traverse(node):
    print(str(node.label) + " " + str(node.support_count))
    for child in node.child:
        traverse(child)


def linkedNodeTraverse(node):
    if node == None:
        return

    print(str(node.label) + " " + str(node.support_count) + " " + str(node.parent.label))

    linkedNodeTraverse(node.next_node)

