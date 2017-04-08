import argparse
import os
import time

from src import assembly
from src import fasta
from src import model
from src import test


def main():
    parser = argparse.ArgumentParser(description='\033[92mFragment Assembly\033[0m of FASTA reads into full-length sequence. Writes result to inputFile_assembled.ext', epilog='by \033[94mSiqi Tian\033[0m, 2017 for Driver.xyz challenge')
    parser.add_argument('inputFile', type=str, help='Input reads in FASTA format')
    args = parser.parse_args()


    t0 = time.time()
    (fileName, fileExtension) = os.path.splitext(args.inputFile)
    outputFile = '%s_assembled%s' % (fileName, fileExtension)

    # Read from input FASTA file
    (reads, labels) = fasta.readFasta(args.inputFile)

    # Perform assembly
    readsList = model.initiateReadData(reads)
    result = assembly.assembleParts(readsList)
    print('\033[92mSUCCESS\033[0m: Finished assembly of reads for (\033[94m%s\033[0m).' % outputFile)

    # Write to output FASTA file
    fasta.writeFasta(outputFile, result, '%s_assembled' % fileName);

    # Test if output is valid
    readsIndices = test.convertReadsToPositions(result, reads, labels)

    test.validateOverlapLength(readsIndices)
    test.validateCoverage(result, readsIndices)
    print('\033[92mSUCCESS\033[0m: Test passed for assembly (\033[94m%s\033[0m).' % outputFile)

    print('Time elapsed: \033[95m%.2f s\033[0m.' % (time.time() - t0))


if __name__ == '__main__':
    main()
