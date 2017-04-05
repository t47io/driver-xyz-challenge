def findReadPosition(fullAssembly, read, label):
    startIndex = fullAssembly.find(read)
    try:
        assert(startIndex != -1)
    except AssertionError:
        raise Exception('\033[41mERROR\033[0m: Found NO match for read (\033[94m%s\033[0m) in assembled result.' % label)
    endIndex = startIndex + len(read) - 1

    return (startIndex, endIndex)


def convertReadsToPositions(fullAssembly, reads, labels):
    readsIndices = []
    for i in xrange(len(reads)):
        readsIndices.append(findReadPosition(fullAssembly, reads[i], labels[i]))

    sortIndices = sorted(range(len(readsIndices)), key=lambda x: readsIndices[x][0])
    readsIndices = [readsIndices[i] for i in sortIndices]
    labels = [labels[i] for i in sortIndices]

    return (readsIndices, labels)


def validateOverlapLength(readsIndices, labels):
    for i in xrange(1, len(readsIndices)):
        previousRead = readsIndices[i - 1]
        currentRead = readsIndices[i]

        try:
            assert(previousRead[1] - currentRead[0] >= (previousRead[1] - previousRead[0]) / 2)
            assert(previousRead[1] - currentRead[0] >= (currentRead[1] - currentRead[0]) / 2)
        except AssertionError:
            raise Exception('\033[41mERROR\033[0m: Overlapping length between read (\033[94m%s\033[0m) and read (\033[94m%s\033[0m) does not satisfy half.' % (labels[i - 1], labels[i]))
