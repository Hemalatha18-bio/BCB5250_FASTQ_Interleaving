# BCB5250 FASTQ Interleaving

## Overview

This repository contains a small Python command-line utility for interleaving paired-end FASTQ reads. It reads R1 and R2 FASTQ files in parallel and writes records in alternating order to a single interleaved FASTQ output.

The project is a compact bioinformatics programming exercise demonstrating FASTQ parsing, paired-read validation, command-line interfaces, compressed-file handling, and reproducible workflow practices.

## Features

- Interleaves paired-end R1/R2 FASTQ files.
- Supports plain `.fastq` and gzip-compressed `.fastq.gz` inputs and outputs.
- Detects unequal numbers of forward and reverse reads.
- Optionally checks that paired read identifiers match.
- Removes partial output files when parsing or validation fails.
- Uses Biopython for FASTQ parsing and writing.

## Requirements

- Python 3.9+
- Biopython

Install the dependency with:

```bash
pip install biopython
```

## Usage

Basic usage:

```bash
python interleave_fastq.py reads_R1.fastq reads_R2.fastq interleaved.fastq
```

For gzip-compressed FASTQ files:

```bash
python interleave_fastq.py reads_R1.fastq.gz reads_R2.fastq.gz interleaved.fastq.gz
```

To additionally validate paired read IDs:

```bash
python interleave_fastq.py \
  reads_R1.fastq.gz \
  reads_R2.fastq.gz \
  interleaved.fastq.gz \
  --validate-ids
```

The script reports the number of read pairs written when successful.

## Pair Validation

The utility always checks that R1 and R2 contain the same number of records. If one input ends before the other, the command raises an error instead of silently dropping extra reads.

When `--validate-ids` is supplied, the script also compares the paired record IDs. Common `/1` and `/2` suffixes are removed before comparison.

Because FASTQ naming conventions vary between sequencing platforms and pipelines, ID validation is optional rather than enabled by default.

## Example Interleaved Layout

For two paired reads, the output order is:

```text
R1 read 1
R2 read 1
R1 read 2
R2 read 2
```

Each entry remains a complete four-line FASTQ record.

## Repository Notes

`FASTQ Report.pdf` is retained as supporting course/project documentation. Large generated FASTQ outputs are not necessary for the reproducible portfolio version of this project; small synthetic test files are preferable for automated testing and examples.

## Limitations

- This tool interleaves existing paired-end reads; it does not perform trimming, quality filtering, alignment, or sequence correction.
- Optional ID validation handles common `/1` and `/2` suffixes but does not attempt to normalize every possible sequencing-platform naming convention.
- FASTQ correctness beyond what Biopython can parse is not independently validated.

## Planned Cleanup Improvements

- Add small synthetic R1/R2 example files.
- Add pytest coverage for normal pairs, unequal read counts, ID mismatches, and gzip input/output.
- Add GitHub Actions CI.
- Add `.gitignore` rules for large/generated FASTQ files.
- Remove the existing large generated `interleaved.fastq` from the cleaned branch after preserving the reproducible small examples.

## Skills Demonstrated

Python, Biopython, FASTQ parsing, paired-end sequencing concepts, CLI design, validation/error handling, gzip file processing, and reproducible bioinformatics scripting.

## Author

Hemalatha Ponnam
