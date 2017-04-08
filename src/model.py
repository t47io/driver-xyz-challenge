class PartData:
    """Construct data representation of a "part", which can be either a single read or a partial assembly of reads

    Args:
        sequence (string): The sequence
        left (:obj:`int`, optional): The minimum length of overlapping region with its left neighboring part.
        right (:obj:`int`, optional): The minimum length of overlapping region with its right neighboring part.

    Returns:
        :class:`PartData` of {
            'sequence': string,
            'left': int,
            'right': int
        }
    """

    def __init__(self, sequence, left=None, right=None):
        self.sequence = sequence
        self.left = left if left is not None else len(sequence) / 2
        self.right = right if right is not None else len(sequence) / 2


    def __eq__(self, other):
        return (self.sequence == other.sequence)


    def isMatchInside(self, other):
        """Checks if self is encompassed by other

            ================================ other
                    ---------                self

            In this case, self is already covered and do not contribute to the assembling process.

        Args:
            other (:class:`PartData`): The other assembly to merge into

        Returns:
            bool: Whether self is completely inside other
        """
        return (self.sequence in other.sequence)

    def isMatchLeft(self, other):
        """Checks if self is the left neighbor of other

                        ==================== other
                        | len |
                  -------------              self

            In this case, the overlap region should be at least as long as the smaller of self's right and the other's left.

        Args:
            other (:class:`PartData`): The other assembly to merge into

        Returns:
            bool: Whether the self is left neighbor of other
        """
        minOverlapLength = max(self.right, other.left)
        overlapSequence = other.sequence[0:minOverlapLength]
        matchStartIndex = self.sequence.rfind(overlapSequence)
        if matchStartIndex != -1 and \
            self.sequence[matchStartIndex:] == other.sequence[:(len(self.sequence)-matchStartIndex)]:
            return matchStartIndex
        else:
            return -1

    def isMatchRight(self, other):
        """Checks if self is the right neighbor of other

               ====================       other
                            | len |
                            ------------- self

            In this case, the overlap region should be at least as long as the smaller of self's left and the other's right.

        Args:
            other (:class:`PartData`): The other assembly to merge into

        Returns:
            bool: Whether the self is left neighbor of other
        """
        return other.isMatchLeft(self)


    def extendLeft(self, other):
        """Assembles self and other when isMatchLeft

        Args:
            other (:obj:`PartData`): The other assembly to merge into


        Returns:
            :class:`PartData`: The merged assembly
        """
        matchStartIndex = self.isMatchLeft(other)
        newSequence = self.sequence[0:matchStartIndex] + other.sequence
        return PartData(newSequence, self.left, other.right)

    def extendRight(self, other):
        """Assembles self and other when isMatchRight

        Args:
            other (:class:`PartData`): The other assembly to merge into

        Returns:
            :class:`PartData`: The merged assembly
        """
        return other.extendLeft(self)


def initiateReadData(readsList):
    """Converts list of reads to list of :class:`PartData`

    Args:
        readsList (:obj:`list` of string): List of reads in string

    Returns:
        :obj:`list` of :class:`PartData`
    """

    return [PartData(read) for read in readsList]
