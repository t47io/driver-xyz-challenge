from . import model


def matchReadInside(read, assembly):
    return (read['sequence'] in assembly['sequence'])


def matchReadExtendLeft(read, assembly):
    minOverlapLen = max(read['minOverlap'][1], assembly['minOverlap'][0])
    overlapSequence = assembly['sequence'][0:minOverlapLen]

    matchIndex = read['sequence'].find(overlapSequence)
    if matchIndex == -1:
        return (False, assembly)
    else:
        newSequence = read['sequence'][0:matchIndex] + assembly['sequence']
        newLeftLen = read['minOverlap'][0]
        return (True, model.partData(newSequence, newLeftLen, read['minOverlap'][1]))


def matchReadExtendRight(read, assembly):
    minOverlapLen = max(read['minOverlap'][0], assembly['minOverlap'][1])
    overlapSequence = assembly['sequence'][-minOverlapLen:]

    matchIndex = read['sequence'].find(overlapSequence)
    if matchIndex == -1:
        return (False, assembly)
    else:
        newSequence = assembly['sequence'] + read['sequence'][matchIndex:]
        newRightLen = read['minOverlap'][1]
        return (True, model.partData(newSequence, read['minOverlap'][0], newRightLen))


def assembleParts(remainingReadsList):
    numRemainingBefore = len(remainingReadsList)
    assembledPartsList = []

    while len(remainingReadsList) > 0:
        read = remainingReadsList[-1]

        isMatchFound = False
        for (i, assembly) in enumerate(assembledPartsList):
            isMatchFound = matchReadInside(read, assembly)
            if isMatchFound:
                remainingReadsList.pop(-1)
                break

            (isMatchFound, newAssembly) = matchReadExtendLeft(read, assembly)
            if isMatchFound:
                assembledPartsList[i] = newAssembly
                remainingReadsList.pop(-1)
                break

            (isMatchFound, newAssembly) = matchReadExtendRight(read, assembly)
            if isMatchFound:
                assembledPartsList[i] = newAssembly
                remainingReadsList.pop(-1)
                break

        if not isMatchFound:
            assembledPartsList.append(remainingReadsList.pop(-1))

    if len(assembledPartsList) == 1:
        return assembledPartsList[0]['sequence']
    elif len(assembledPartsList) == numRemainingBefore:
        raise RuntimeError('Unmatched reads, abort.')
    else:
        return assembleParts(assembledPartsList)

