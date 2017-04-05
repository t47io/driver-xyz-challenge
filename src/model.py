def partData(sequence, leftOverlapLength=None, rightOverlapLength=None):
    """Construct data representation of a "part", which can be either a single read or a partial assembly of reads

    Args:
        sequence (string): The sequence
        leftOverlapLength (:obj:`int`, optional): The minimum length of overlapping region with its left neighboring part.
        rightOverlapLength (:obj:`int`, optional): The minimum length of overlapping region with its right neighboring part.

    Returns:
        :obj:`dict` of {
            'sequence': string,
            'minOverlapLength': {
                'left': int,
                'right': int
            }
        }
    """

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
    """Converts list of reads to list of :obj:`partData`

    Args:
        readsList (:obj:`list` of string): List of reads in string

    Returns:
        :obj:`list` of :obj:`partData`
    """

    return [partData(read) for read in readsList]