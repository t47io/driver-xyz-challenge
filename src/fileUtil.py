def readFasta(fileName):
    labels = []
    reads = []
    read = ''

    f = open(fileName, 'r')
    for line in f.readlines():
        line = line.strip()

        if line.startswith('>'):
            if not len(read):
                continue
            labels.append(line[1:])
            reads.append(read)
            read = ''
        else:
            read += line
    reads.append(read)

    return (reads, labels)


def writeFasta(fileName, sequenceList, labelList):
    if type(sequenceList) is str and type(labelList) is str:
        sequenceList = [sequenceList]
        labelList = [labelList]
    elif len(sequenceList) != len(labelList):
        raise ValueError('Mismatch in number of sequences (%s) and labels (%s) to write to FASTA file' % (len(sequenceList), len(labelList)))

    f = open(fileName, 'w')
    for i in xrange(len(sequenceList)):
        f.write('>%s\n' % labelList[i])
        f.write('%s\n' % sequenceList[i])

    f.close()
