def partData(seq, leftLen=None, rightLen=None):
    if leftLen is None:
        leftLen = len(seq) / 2
    if rightLen is None:
        rightLen = len(seq) / 2

    return {
        'sequence': seq,
        'minOverlap': [leftLen, rightLen]
    }


def initiateReadData(readsList):
    return [partData(read) for read in readsList]