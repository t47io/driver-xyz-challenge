from src import assembly
from src import fasta
from src import model
from src import test


def main():
    resultName = 'Rosalind_assembled'
    # (reads, labels) = fasta.readFasta('data/naive_data.txt')
    (reads, labels) = fasta.readFasta('data/Rosalind_data.txt')

    readsList = model.initiateReadData(reads)
    result = assembly.assembleParts(readsList)
    print('\033[92mSUCCESS\033[0m: Finished assembly of reads for (\033[94m%s\033[0m).' % resultName)

    fasta.writeFasta('data/%s.txt' % resultName, result, resultName);

    (readsIndices, labels) = test.convertReadsToPositions(result, reads, labels)
    test.validateOverlapLength(readsIndices, labels)
    print('\033[92mSUCCESS\033[0m: Test passed for assembly (\033[94m%s\033[0m).' % resultName)


if __name__ == '__main__':
    main()
