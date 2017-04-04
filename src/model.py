def partData(sequence, leftLen=None, rightLen=None):
    if leftLen is None:
        leftLen = len(sequence) / 2
    if rightLen is None:
        rightLen = len(sequence) / 2

    return {
        'sequence': sequence,
        'minOverlap': [leftLen, rightLen]
    }


def initiateReadData(readsList):
    return [partData(read) for read in readsList]