from . import model


def matchReadInside(singleRead, assembledPart):
    return (singleRead['sequence'] in assembledPart['sequence'])


def matchReadExtendLeft(singleRead, assembledPart):
    minOverlapLength = max(singleRead['minOverlapLength']['right'], assembledPart['minOverlapLength']['left'])
    overlapSequence = assembledPart['sequence'][0:minOverlapLength]

    matchStartIndex = singleRead['sequence'].find(overlapSequence)
    if matchStartIndex == -1:
        return (False, assembledPart)
    else:
        newSequence = singleRead['sequence'][0:matchStartIndex] + assembledPart['sequence']
        newLeftLength = singleRead['minOverlapLength']['left']
        return (True, model.partData(newSequence, newLeftLength, singleRead['minOverlapLength']['right']))


def matchReadExtendRight(singleRead, assembledPart):
    minOverlapLength = max(singleRead['minOverlapLength']['left'], assembledPart['minOverlapLength']['right'])
    overlapSequence = assembledPart['sequence'][-minOverlapLength:]

    matchStartIndex = singleRead['sequence'].find(overlapSequence)
    if matchStartIndex == -1:
        return (False, assembledPart)
    else:
        newSequence = assembledPart['sequence'] + singleRead['sequence'][(matchStartIndex + minOverlapLength):]
        newRightLength = singleRead['minOverlapLength']['right']
        return (True, model.partData(newSequence, singleRead['minOverlapLength']['left'], newRightLength))


def assembleParts(remainingReadsList):
    remainingListLengthBefore = len(remainingReadsList)
    assembledPartsList = []

    while len(remainingReadsList) > 0:
        singleRead = remainingReadsList[-1]

        isMatchFound = False
        for (i, assembledPart) in enumerate(assembledPartsList):
            isMatchFound = matchReadInside(singleRead, assembledPart)
            if isMatchFound:
                remainingReadsList.pop(-1)
                break

            (isMatchFound, extendedPart) = matchReadExtendLeft(singleRead, assembledPart)
            if isMatchFound:
                assembledPartsList[i] = extendedPart
                remainingReadsList.pop(-1)
                break

            (isMatchFound, extendedPart) = matchReadExtendRight(singleRead, assembledPart)
            if isMatchFound:
                assembledPartsList[i] = extendedPart
                remainingReadsList.pop(-1)
                break

        if not isMatchFound:
            assembledPartsList.append(remainingReadsList.pop(-1))

    if len(assembledPartsList) == 1 and len(remainingReadsList) == 0:
        return assembledPartsList[0]['sequence']
    elif len(assembledPartsList) == remainingListLengthBefore:
        raise RuntimeError('\033[41mCould NOT assemble\033[0m reads, possibly by sequencing mismatches.')
    else:
        return assembleParts(assembledPartsList)

