from src import assembly
from src import fileUtil
from src import model



def main():
    (reads, labels) = fileUtil.readFasta('data/Rosalind_data.txt')

    readsList = model.initiateReadData(reads)
    print readsList
    print assembly.assembleParts(readsList)




if __name__ == '__main__':
    main()
