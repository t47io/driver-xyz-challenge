import re


def findReadPosition(fullAssembly, read, label=''):
    """Finds the index of a given target (read) inside the context (fullAssembly)

        ========================================= context
                  --------------                  target
                  ^            ^
            startIndex       endIndex

    Args:
        fullAssembly (string): String of context
        read (string): String target
        label (string, optional): Label of string target (for logging)

    Returns:
        :obj:`tuple` of (
            startIndex (int): The start index of the target in the context
            endIndex (int): The end index of the target in the context
        )

    Raises:
        AssertionError: When the target is not found in the context
    """
    matchIndices = [
        (match.start(), match.end())
        for match in re.finditer(read, fullAssembly)
    ]

    try:
        assert(len(matchIndices) > 0)
    except AssertionError:
        raise Exception('\033[41mERROR\033[0m: Found NO match for read (\033[94m%s\033[0m) in assembled result.' % label)

    return matchIndices


def convertReadsToPositions(fullAssembly, readsList, labelsList=None):
    """Find and sort indices of each tareget (read) in the context (fullAssembly)

        ========================================= context
        ----------
        ^        ^
               ------------
               ^          ^
                       --------------
                       ^            ^
                             ---------------
                             ^             ^
                                        ---------
                                        ^       ^

    Args:
        fullAssembly (string): String of context
        readsList (:obj:`list` of string): List of string targets
        labelsList (:obj:`list` of string, optional): List of label of string target (for logging)

    Returns
        readsIndices (:obj:`list` of :obj:`list` of `tuple(int, int)`): List of start and end indices tuples sorted by start index
        labelsList: (:obj:`list` of string): Input "labelsList" sorted according to output "readsIndices"

    """
    if labelsList is None:
        labelsList = [''] * len(readsList)

    readsIndicesCombinations = []
    for i in xrange(len(readsList)):
        # get all possible positions of a read
        indexTuples = findReadPosition(fullAssembly, readsList[i], labelsList[i])

        if not len(readsIndicesCombinations):
            readsIndicesCombinations = [[indexTuple] for indexTuple in indexTuples]
        else:
            # compose combinations of positions with previous reads
            newReadsIndicesCombinations = []
            for readsIndices in readsIndicesCombinations:
                for indices in indexTuples:
                    newReadsIndices = [readIndex for readIndex in readsIndices]
                    newReadsIndices.append(indices)
                    newReadsIndicesCombinations.append(newReadsIndices)

            readsIndicesCombinations = newReadsIndicesCombinations

    # sort reads by their start index
    sortIndicesCombinations = [
        sorted(range(len(readsIndices)), key=lambda x: readsIndices[x])
        for readsIndices in readsIndicesCombinations
    ]
    for (i, sortIndices) in enumerate(sortIndicesCombinations):
        readsIndices = readsIndicesCombinations[i]
        readsIndicesCombinations[i] = [
            readsIndices[j]
            for j in sortIndices
        ]

    return readsIndicesCombinations


def validateOverlapLengthEach(readsIndices, ratio=0.5):
    """Check if neighboring reads satisfy the minimum overlapping rule

        -------------------              read
                ----------------------   read
                | overlap |

    Args:
        readsIndices (:obj:`list` of `tuple(int, int)`): List of start and end indices tuples sorted by start index
        ratio (float, optional): Minimum overlap ratio between neighbors

    Returns:
        bool: Whether all the reads satisfy overlapping rule
    """
    for i in xrange(1, len(readsIndices)):
        previousRead = readsIndices[i - 1]
        currentRead = readsIndices[i]

        isLeftValid = (previousRead[1] - currentRead[0] >= (previousRead[1] - previousRead[0]) * ratio)
        isRightValid = (previousRead[1] - currentRead[0] >= (currentRead[1] - currentRead[0]) * ratio)
        if not (isLeftValid and isRightValid):
             return False
    return True


def validateOverlapLength(readsIndicesCombinations, ratio=0.5):
    """Check if neighboring reads satisfy the minimum overlapping rule

    Args:
        readsIndicesCombinations (:obj:`list` of :obj:`list` of `tuple(int, int)`): List of start and end indices tuples sorted by start index
        ratio (float, optional): Minimum overlap ratio between neighbors

    Raises
        AssertionError: When none of the combinations has all pairs of neighbors satisfy minimum overlapping length

    """
    isValid = False
    for readsIndices in readsIndicesCombinations:
        if validateOverlapLengthEach(readsIndices):
            return

    raise AssertionError('\033[41mERROR\033[0m: Overlapping length does not satisfy ratio (\033[93m%s\033[0m).' % ratio)
    


def validateCoverage(fullAssembly, readsIndicesCombinations):
    """Check if the entire context is covered by reads. Based on "validateOverlapLength()", now only need to check the ends not the middle.

        ========================== context
        ----------                 read 1
               ------------    ??  read 2

    Args:
        fullAssembly (string): String of context
        readsIndicesCombinations (:obj:`list` of :obj:`list` of `tuple(int, int)`): List of start and end indices tuples sorted by start index

    Raises:
        AssertionError: When the reads span is shorter than full context
    """

    fullAssemblyLength = len(fullAssembly)

    for readsIndices in readsIndicesCombinations:
        isStartValid = (readsIndices[0][0] == 0)
        isEndValid = (readsIndices[-1][1] == fullAssemblyLength)

        if (isStartValid and isEndValid):
             return

    raise AssertionError('\033[41mERROR\033[0m: Reads (\033[94m%s-%s\033[0m) do not cover full-length context (\033[93m%s\033[0m).' % (readsIndices[0][0], readsIndices[-1][1],fullAssemblyLength))

