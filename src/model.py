def partData(sequence, leftOverlapLength=None, rightOverlapLength=None):
    if leftOverlapLength is None:
        leftOverlapLength = len(sequence) / 2
    if rightOverlapLength is None:
        rightOverlapLength = len(sequence) / 2

    return {
        'sequence': sequence,
        'minOverlapLength': {
            'left': leftOverlapLength,
            'right': rightOverlapLength
        }
    }


def initiateReadData(readsList):
    return [partData(read) for read in readsList]