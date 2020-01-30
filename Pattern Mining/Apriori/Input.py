def inputFunction(dataset, transactions, itemSet, freq):
    fp = open(dataset, "r")
    for line in fp:
        tran = []
        for item in line.split():
            x = int(item)
            tran.append(x)
            tmp1 = [x]
            tmp2 = str(tmp1)
            if tmp2 not in freq:
                itemSet.append(tmp1)
                freq[tmp2] = 1
            else:
                freq[tmp2] = freq[tmp2] + 1

        transactions.append(tran)
    fp.close()

    # print(transactions)
    # print(itemSet)
    # print(freq)
