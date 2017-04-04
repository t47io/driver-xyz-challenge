from src import assembly
from src import fileUtil
from src import model

from test import findIndex

def main():
    # (reads, labels) = fileUtil.readFasta('data/naive_data.txt')
    (reads, labels) = fileUtil.readFasta('data/Rosalind_data.txt')

    readsList = model.initiateReadData(reads)
    result = assembly.assembleParts(readsList)
    resultName = 'Rosalind_assembled'
    fileUtil.writeFasta('data/%s.txt' % resultName, result, resultName);
    print('\033[92mSUCCESS\033[0m: Read assembly (\033[94m%s\033[0m) finished.' % resultName)

    findIndex.convertReadsToPositions(result, reads, labels)
    print('\033[92mSUCCESS\033[0m: Read assembly passed test.')


if __name__ == '__main__':
    main()
