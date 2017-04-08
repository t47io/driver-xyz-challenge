from . import model

def assembleParts(remainingReadsList):
    """Recursively assembles the reads

    Args:
        remainingReadsList (:obj:`list` of :class:`PartData`): The list of parts to assemble

    Returns:
        sequence (string): The fully assembled context
    """

    if len(remainingReadsList) == 1:
        # successful result return the string
        return remainingReadsList[0].sequence

    # no longer checks for inside cases
    # since it can be bridging elsewhere in a repetitive sequence
    # for (i, part) in reversed(list(enumerate(remainingReadsList))):
    #     for otherPart in remainingReadsList[0:i]:
    #         if part.isMatchInside(otherPart):
    #             remainingReadsList.pop(i)
    #             break

    # first try extend to left
    for part in remainingReadsList:
        # find a list of probable neighbors
        leftNeighbors = [
            otherPart
            for otherPart in remainingReadsList
            if otherPart != part and part.isMatchLeft(otherPart) != -1
        ]

        # if no neighbr, pass
        if len(leftNeighbors):
            # try each neighbor option
            for neighbor in leftNeighbors:
                mergedPart = part.extendLeft(neighbor)
                assembledPartsList = [
                    otherPart
                    for otherPart in remainingReadsList
                    if otherPart != part and otherPart != neighbor
                ]
                assembledPartsList.append(mergedPart)

                # recursively assemble
                result = assembleParts(assembledPartsList)
                # if successful, that's it
                if result is not None and isinstance(result, str):
                    return result

    # next try extend to right
    for part in remainingReadsList:
        rightNeighbors = [
            otherPart
            for otherPart in remainingReadsList
            if otherPart != part and part.isMatchRight(otherPart) != -1
        ]
        if len(rightNeighbors):
            for neighbor in rightNeighbors:
                mergedPart = part.extendRight(neighbor)
                assembledPartsList = [
                    otherPart
                    for otherPart in remainingReadsList
                    if otherPart != part and otherPart != neighbor
                ]
                assembledPartsList.append(mergedPart)

                result = assembleParts(assembledPartsList)
                if result is not None and isinstance(result, str):
                    return result

    # When can't assemble any more (dead end of this DFS)
    return None
