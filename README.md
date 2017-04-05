# driver-xyz-challenge

## Problem

See [here](https://github.com/t47io/driver-xyz-challenge/challenge.md).


## Usage

To assemble the reads, e.g. with the **Rosalind** example data, run:

```sh
git clone https://github.com/t47io/driver-xyz-challenge.git
cd drive-xyz-challenge

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

Now given two **`part`s** `A` and `B`, there are 4 possibilities:

#### 1. `A` is encompassed by `B`

> Then `A` does not contribute to the full assembly since `B` got all the information.

#### 2. `A` is the left neighbor of `B`

> Then merge them, and update the `'sequence'` and new `'left'` value

#### 3. `A` is the right neighbor of `B`

> Then merge them, and update the `'sequence'` and new `'right'` value

#### 4. None above

> Then copy both into the new list, as separate "_assembly sites_" in parallel

#### (5.) `A` encompasses `B` (inverse of 1.)

> Treated as 4., since eventually `B` would be gone.

And now recursively merging a list of **`part`s**, we should be able to reduce into one single **`part`** in the end.

If the number of **`part`s** does not decrease in a round, it means we are not able to further assemble. It would raise an error (see [Limitation](#limitation)).


## Test

The following tests are performed on the assembled result:

* Each input read should be matched inside the assembled full-length.

* Each pair of neighboring input reads should satisfy minimum overlapping length.

* The assembled full-length should be completely covered by input reads.

The testing logic is inside `src/test.py`.


## Limitation

The solution is based on the following assumptions:

* All reads are on the _sense_ strand. No attempt for matching reverse complement.

* Zero tolerance on nucleotide mismatches (common for sequencing errors).

In addition, for a full-length sequence with reptitive nature, the result is influenced by the order of the reads. For example:

> Desired output:
```
ABCBD
```

> Read input:
```
AB, BD, BC, CB
```

It can assemble into `ABD, BCB` and fail.


## To-Do

Write a random sequence generator that provides a full-length sequence, and a set of reads. This would help further testing the current solution.
