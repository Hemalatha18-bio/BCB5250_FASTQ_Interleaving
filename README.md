# BCB5250 FASTQ Interleaving

## Overview

This repository contains a small Python command-line utility for interleaving paired-end FASTQ reads. It reads R1 and R2 FASTQ files in parallel and writes records in alternating order to a single interleaved FASTQ output.

The project is a compact bioinformatics programming exercise demonstrating FASTQ parsing, paired-read validation, command-line interfaces, compressed-file handling, testing, and reproducible workflow practices.

## Features

- Interleaves paired-end R1/R2 FASTQ files.
- Supports plain `.fastq` and gzip-compressed `.fastq.gz` inputs and outputs.
- Detects unequal numbers of forward and reverse reads.
- Optionally checks that paired read identifiers match.
- Removes partial output files when parsing or validation fails.
- Uses Biopython for FASTQ parsing and writing.
- Includes small reproducible example FASTQ files.
- Includes pytest tests and GitHub Actions CI.

## Requirements

- Python 3.9+
- Biopython
- pytest for development/testing

Install dependencies with:

```bash
pip install -r requirements.txt
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

## Reproducible Example

Run the included example data with:

```bash
python interleave_fastq.py \
  examples/sample_R1.fastq \
  examples/sample_R2.fastq \
  example_output.fastq \
  --validate-ids
```

The resulting file should match `examples/expected_interleaved.fastq`.

## Pair Validation

The utility always checks that R1 and R2 contain the same number of records. If one input ends before the other, the command raises an error instead of silently dropping extra reads.

When `--validate-ids` is supplied, the script also compares paired record IDs. Common `/1` and `/2` suffixes are removed before comparison.

Because FASTQ naming conventions vary between sequencing platforms and pipelines, ID validation is optional rather than enabled by default.

## Testing and CI

Run the test suite locally with:

```bash
pytest -q
```

The tests cover normal interleaving, unequal read counts, mismatched read IDs, partial-output cleanup, and gzip output. GitHub Actions runs the same tests for pull requests and pushes targeting `main`.

## Repository Structure

```text
BCB5250_FASTQ_Interleaving/
├── .github/workflows/ci.yml
├── .gitignore
├── FASTQ Report.pdf
├── README.md
├── interleave_fastq.py
├── requirements.txt
├── examples/
│   ├── sample_R1.fastq
│   ├── sample_R2.fastq
│   └── expected_interleaved.fastq
└── tests/
    └── test_interleave_fastq.py
```

`FASTQ Report.pdf` is retained as supporting course/project documentation. Large generated FASTQ outputs are intentionally excluded from the cleaned portfolio version; `.gitignore` keeps generated FASTQ files out while allowing the tiny files under `examples/`.

## Limitations

- This tool interleaves existing paired-end reads; it does not perform trimming, quality filtering, alignment, or sequence correction.
- Optional ID validation handles common `/1` and `/2` suffixes but does not attempt to normalize every possible sequencing-platform naming convention.
- FASTQ correctness beyond what Biopython can parse is not independently validated.

## Skills Demonstrated

Python, Biopython, FASTQ parsing, paired-end sequencing concepts, CLI design, validation/error handling, gzip file processing, pytest, GitHub Actions, and reproducible bioinformatics scripting.

## Author

Hemalatha Ponnam
