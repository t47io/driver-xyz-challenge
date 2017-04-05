def readFasta(fileName):
    """Read sequences and labels from a FASTA file.

    Args:
        fileName (string): Name of FASTA file.

    Returns:
        readsList (:obj:`list` of :obj:`string`): List of sequencing reads.
        labelsList (:obj:`list` of :obj:`string`): List of read labels.

    Raises:
        ValueError: When number of reads and labels do not match.
    """

    labelsList = []
    readsList = []
    singleRead = ''

    f = open(fileName, 'r')
    for line in f.readlines():
        line = line.strip()

        if line.startswith('>'):
            labelsList.append(line[1:])
            if len(singleRead):
                readsList.append(singleRead)
            singleRead = ''
        else:
            singleRead += line

    readsList.append(singleRead)
    f.close()
    print('\033[92mSUCCESS\033[0m: Read inputs from file (\033[94m%s\033[0m).' % fileName)

    if len(readsList) != len(labelsList):
        raise ValueError('\033[41mMismatch\033[0m in number of sequences (\033[94m%s\033[0m) and labels (\033[94m%s\033[0m) from input FASTA file' % (len(readsList), len(labelsList)))

    return (readsList, labelsList)


def writeFasta(fileName, sequenceList, labelList):
    """Write sequences and labels to a FASTA file.

    Args:
        fileName (string): Name of FASTA file.

    Returns:
        sequenceList (:obj:`list` of :obj:`string` or string): List of sequencing reads.
        labelsList (:obj:`list` of :obj:`string` or string): List of read labels; must be same length as "sequenceList".

    Raises:
        ValueError: When number of sequences and labels do not match.
    """

    if type(sequenceList) is str and type(labelList) is str:
        sequenceList = [sequenceList]
        labelList = [labelList]
    elif len(sequenceList) != len(labelList):
        raise ValueError('\033[41mMismatch\033[0m in number of sequences (\033[94m%s\033[0m) and labels (\033[94m%s\033[0m) to write to FASTA file' % (len(sequenceList), len(labelList)))

    f = open(fileName, 'w')
    for i in xrange(len(sequenceList)):
        f.write('>%s\n' % labelList[i])
        f.write('%s\n' % sequenceList[i])

    f.close()
    print('\033[92mSUCCESS\033[0m: Wrote result to file (\033[94m%s\033[0m).' % fileName)
