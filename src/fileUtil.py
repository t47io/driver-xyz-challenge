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

