from src import assembly
from src import fileUtil
from src import model


def main():
    # (reads, labels) = fileUtil.readFasta('data/naive_data.txt')
    (reads, labels) = fileUtil.readFasta('data/Rosalind_data.txt')

    readsList = model.initiateReadData(reads)
    fileUtil.writeFasta('data/Rosalind_assembled.txt', assembly.assembleParts(readsList), 'Rosalind_assembled');


if __name__ == '__main__':
    main()
