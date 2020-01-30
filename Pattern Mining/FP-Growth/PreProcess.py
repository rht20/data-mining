import math


def loadData(dataset, transactions, items, freq):
    fp = open(dataset, "r")
    for line in fp:
        tran = []
        for item in line.split():
            x = int(item)
            tran.append(x)
            if x not in freq:
                items.append(x)
                freq[x] = 1
            else:
                freq[x] = freq[x] + 1

        transactions.append(tran)
    fp.close()

    # print(items)
    # print(transactions)
    # print(freq)


def preProcess(dataset, transactions, items, freq, threshold):
    tmpList = []
    loadData(dataset, tmpList, items, freq)

    threshold = math.ceil((threshold * float(len(tmpList))) / 100.0)
    min_support = int(threshold)

    for transaction in tmpList:
        tmp = []
        for item in transaction:
            tmp.append((item, freq[item]))

        tmp.sort(key=lambda x: (-x[1], x[0]))

        tran = []
        for item in tmp:
            if freq[item[0]] >= min_support:
                tran.append(item[0])
            else:
                break
        transactions.append(tran)
    # print(transactions)


# process("book.dat", [], [], {}, 30)
