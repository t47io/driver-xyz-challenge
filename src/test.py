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
        startIndex (int): The start index of the target in the context
        endIndex (int): The end index of the target in the context

    Raises:
        AssertionError: When the target is not found in the context
    """

    startIndex = fullAssembly.find(read)
    try:
        assert(startIndex != -1)
    except AssertionError:
        raise Exception('\033[41mERROR\033[0m: Found NO match for read (\033[94m%s\033[0m) in assembled result.' % label)
    endIndex = startIndex + len(read)

    return (startIndex, endIndex)


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
        readsIndices (:obj:`list` of `tuple(int, int)`): List of start and end indices tuples sorted by start index
        labelsList: (:obj:`list` of string): Input "labelsList" sorted according to output "readsIndices"

    """

    if labelsList is None:
        labelsList = [''] * len(readsList)

    readsIndices = []
    for i in xrange(len(readsList)):
        readsIndices.append(findReadPosition(fullAssembly, readsList[i], labelsList[i]))

    sortIndices = sorted(range(len(readsIndices)), key=lambda x: readsIndices[x][0])
    readsIndices = [readsIndices[i] for i in sortIndices]
    labelsList = [labelsList[i] for i in sortIndices]

    return (readsIndices, labelsList)


def validateOverlapLength(readsIndices, labelsList=None, ratio=0.5):
    """Check if neighboring reads satisfy the minimum overlapping rule

        -------------------              read
                ----------------------   read
                | overlap |

    Args:
        readsIndices (:obj:`list` of `tuple(int, int)`): List of start and end indices tuples sorted by start index
        labelsList (:obj:`list` of string, optional): List of label of string target (for logging)
        ratio (float, optional): Minimum overlap ratio between neighbors

    Raises
        AssertionError: When any pairs of neighbors fail to satisfy minimum overlapping length

    """

    if labelsList is None:
        labelsList = [''] * len(readsIndices)

    for i in xrange(1, len(readsIndices)):
        previousRead = readsIndices[i - 1]
        currentRead = readsIndices[i]

        try:
            assert(previousRead[1] - currentRead[0] >= (previousRead[1] - previousRead[0]) * ratio)
            assert(previousRead[1] - currentRead[0] >= (currentRead[1] - currentRead[0]) * ratio)
        except AssertionError:
            raise Exception('\033[41mERROR\033[0m: Overlapping length between read (\033[94m%s\033[0m) and read (\033[94m%s\033[0m) does not satisfy ratio (\033[93m%s\033[0m).' % (labelsList[i - 1], labelsList[i], ratio))


def validateCoverage(fullAssembly, readsIndices):
    """Check if the entire context is covered by reads. Based on "validateOverlapLength()", now only need to check the ends not the middle.

        ========================== context
        ----------                 read 1
               ------------    ??  read 2

    Args:
        fullAssembly (string): String of context
        readsIndices (:obj:`list` of `tuple(int, int)`): List of start and end indices tuples sorted by start index

    Raises:
        AssertionError: When the reads span is shorter than full context
    """

    fullAssemblyLength = len(fullAssembly)

    try:
        assert(readsIndices[0][0] == 0)
        assert(readsIndices[-1][1] == fullAssemblyLength)
    except AssertionError:
        raise Exception('\033[41mERROR\033[0m: Reads (\033[94m%s-%s\033[0m) do not cover full-length context (\033[93m%s\033[0m).' % (readsIndices[0][0], readsIndices[-1][1],fullAssemblyLength))

