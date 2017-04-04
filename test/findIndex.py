def findReadPosition(fullAssembly, read, label):
    startIndex = fullAssembly.find(read)
    if startIndex == -1:
        raise AssertionError('\033[41mFound NO match\033[0m for read (\033[94m%s\033[0m) in assembled result.' % label)
    endIndex = startIndex + len(read) - 1

    return (startIndex, endIndex)


# def sortReadsByPosition(reads, labels):
#     pass


def convertReadsToPositions(fullAssembly, reads, labels):
    indices = []
    for i in xrange(len(reads)):
        indices.append(findReadPosition(fullAssembly, reads[i], labels[i]))

    indices.sort(key=lambda x: x[0])

    print indices
