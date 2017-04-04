from src import fileUtil




def main():
    (reads, labels) = fileUtil.readFasta('data/Rosalind_data.txt')
    print(reads)
    print(labels)




if __name__ == '__main__':
    main()
