# driver-xyz-challenge

## Problem

See descriptions [here](https://github.com/t47io/driver-xyz-challenge/challenge.md). The solution is based on the following assumptions:

* All reads are on the _sense_ strand. No attempt for matching reverse complement.

* Zero tolerance on nucleotide mismatches (common for sequencing errors).

## Usage

To assemble the reads, e.g. with the **Rosalind** example data, run:

```sh
git clone https://github.com/t47io/driver-xyz-challenge.git
cd drive-xyz-challenge

# python 2.x
python solution.py data/Rosalind_data.txt
```

The result is saved in `data/Rosalind_data_assembled.txt` in FASTA format.


## Design

> The specific set of sequences you will get satisfy a very unique property:  there exists a unique way to reconstruct the entire chromosome from these reads by gluing together pairs of reads that overlap by more than half their length.

This constraint makes the approach simple:

We represent a single read and a partially assembled chunk as **`part`**. It records the sequence, and the minimum overlapping length to its direct neighbors:

```js
{
  'sequence': string,
  'minOverlapLength': {
    'left': int,
    'right': int
  }
}
```

* For a single read, the `'left'` and `'right'` are just half of its `'sequence'` length.

* For a partialy assembly, the `'left'` is the `'left'` of its left-most single read:

```
  (all its single reads)

  <-L-> [half of read length]
  ----------                                    read 1
         -------------                          read 2
                   ------------                 read 3
                          -------------         read 4
                                 -------------  read 5
                                        <- R->
  ============================================  assembly
```

Now given two `part`s `A` and `B`, there are 4 possibilities:

#### 1. `A` is encompassed by `B`

> Then `A` does not contribute to the full assembly since `B` got all the information.

#### 2. `A` is the left neighbor of `B`

> Then merge them, and update the `'sequence'` and new `'left'` value

#### 3. `A` is the right neighbor of `B`

> Then merge them, and update the `'sequence'` and new `'right'` value

#### 4. None above

> Then copy both into the new list, as separate "_assembly sites_" in parallel

And now recursively merging a list of `part`s, we should be able to reduce into one single `part` in the end.

If the number of `part`s does not decrease in a round, it means we are not able to further assemble. It would raise an error.

#### The above _greedy_ approach was implemented first, see [this commit](https://github.com/t47io/driver-xyz-challenge/tree/4548ee59d1344e4d2c986b872b63391b8cbe0988). However, it is _sensitive to the order of read appearance_.

For example, consider a full-length sequence of `ABCAD`, with fragments:

```
AB, BC, CA, AD
```

The order of the appearance of these 4 fragments influcence the assembly for the aforementioned greedy approach:

```
AB, BC, CA, AD => ABC, CAD => ABCAD
_or_
AD, BC, CA, AB => AD, BCA, AB => AD, BCAB
```

Thus, an improved version finds all possible extentions for a given read, and assembles it depth-first. For a particular assembly order, if it reaches dead end, we just give it up. Once a solution is found, the program terminates.

In this new version, we do not remove reads when it's encompassed by another, since it could be useful bridging elsewhere in a highly repetitive sequence to assemble. For example, in the case of full-sequence `ABABABC`, with fragments:

```
ABA, BAB, ABA, BAB, ABC
```

Removing duplicates will end up with a shorter assembled full-length. Admittedly, this is a case out of the scope of this challenge, since it does not have 1 single solution given the inputs.


## Test

The following tests are performed on the assembled result:

* Each input read should be matched inside the assembled full-length.

* Each pair of neighboring input reads should satisfy minimum overlapping length.

* The assembled full-length should be completely covered by input reads.

The testing logic is inside `src/test.py`. Additional test cases are included in `data/`.


## To-Do

Write a random sequence generator that provides a full-length sequence, and a set of reads. This would help further testing the current solution.
