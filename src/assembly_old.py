from . import model


def matchReadInside(singleRead, assembledPart):
    """Checks if the read is encompassed by the assembly

        ================================ assembly
                ---------                read

        In this case, the read is already covered and do not contribute to the assembling process.

    Args:
        singleRead (:obj:`partData`): The single read to examine
        assembledPart (:obj:`partData`): The assembly to merge into

    Returns:
        bool: Whether the read is completely inside the assembly
    """

    return (singleRead['sequence'] in assembledPart['sequence'])


def matchReadExtendLeft(singleRead, assembledPart):
    """Checks if the read is the left neighbor of the assembly, and merge them if possible

                    ==================== assembly
                    |  L  |
              -------------              read

        In this case, the overlap region should be at least as long as the smaller of assembly's left "minOverlapLength" and the read's right "minOverlapLength". If matched, merge into one assembly, and updating the new left "minOverlapLength" to the read's left "minOverlapLength".

    Args:
        singleRead (:obj:`partData`): The single read to examine
        assembledPart (:obj:`partData`): The assembly to merge into

    Returns:
        flag (bool): Whether the read is left neighbor of the assembly
        assembledPart (:obj:`partData`): The merged new assembly
    """

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
    """Checks if the read is the right neighbor of the assembly, and merge them if possible

           ====================       assembly
                        |  L  |
                        ------------- read

        In this case, the overlap region should be at least as long as the smaller of assembly's right "minOverlapLength" and the read's left "minOverlapLength". If matched, merge into one assembly, and updating the new right "minOverlapLength" to the read's right "minOverlapLength".

    Args:
        singleRead (:obj:`partData`): The single read to examine
        assembledPart (:obj:`partData`): The assembly to merge into

    Returns:
        flag (bool): Whether the read is right neighbor of the assembly
        assembledPart (:obj:`partData`): The merged new assembly
    """

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
    """Recursively assembles the reads

    Args:
        remainingReadsList (:obj:`list` of :obj:`partData`): The list of parts to assemble

    Returns:
        sequence (string): The fully assembled context

    Raises:
        RuntimError: When it's not possible to assemble any parts together from the list

    """

    remainingListLengthBefore = len(remainingReadsList)
    assembledPartsList = []

    while len(remainingReadsList) > 0:
        # Work on the last item of the list (easier to pop)
        singleRead = remainingReadsList[-1]

        isMatchFound = False
        # Compare against all the assembled parts
        for (i, assembledPart) in enumerate(assembledPartsList):
            # if match inside, discard the read
            isMatchFound = matchReadInside(singleRead, assembledPart)
            if isMatchFound:
                remainingReadsList.pop(-1)
                break

            # if match to left neighbor, assemble them and discard the read
            (isMatchFound, extendedPart) = matchReadExtendLeft(singleRead, assembledPart)
            if isMatchFound:
                assembledPartsList[i] = extendedPart
                remainingReadsList.pop(-1)
                break

            # if match to right neighbor, assemble them and discard the read
            (isMatchFound, extendedPart) = matchReadExtendRight(singleRead, assembledPart)
            if isMatchFound:
                assembledPartsList[i] = extendedPart
                remainingReadsList.pop(-1)
                break

        # if no match, move it as a new "assembly site" in the list
        if not isMatchFound:
            assembledPartsList.append(remainingReadsList.pop(-1))

    # When no more to assemble
    if len(assembledPartsList) == 1 and len(remainingReadsList) == 0:
        return assembledPartsList[0]['sequence']
    # When not able to assemble any pairs (thus reducing total number of parts)
    elif len(assembledPartsList) == remainingListLengthBefore:
        raise RuntimeError('\033[41mCould NOT assemble\033[0m reads, possibly by sequencing mismatches.')
    # Call to a new round of assemble
    else:
        return assembleParts(assembledPartsList)

