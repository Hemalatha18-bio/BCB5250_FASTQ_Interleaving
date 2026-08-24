#!/usr/bin/env python3
"""Interleave paired-end FASTQ files with basic pairing validation."""

import argparse
import gzip
from itertools import zip_longest
from pathlib import Path

from Bio import SeqIO


def open_text(path, mode):
    """Open plain-text or gzip-compressed FASTQ files in text mode."""
    path = Path(path)
    if path.suffix.lower() == ".gz":
        return gzip.open(path, mode + "t")
    return path.open(mode, encoding="utf-8")


def normalized_read_id(record_id):
    """Normalize common /1 and /2 mate suffixes for optional ID checking."""
    if record_id.endswith("/1") or record_id.endswith("/2"):
        return record_id[:-2]
    return record_id


def interleave_fastq(forward_file, reverse_file, output_file, validate_ids=False):
    """Interleave R1/R2 FASTQ records and return the number of read pairs written.

    Raises
    ------
    FileNotFoundError
        If either input file does not exist.
    ValueError
        If the two inputs contain different numbers of reads or, when requested,
        paired record identifiers do not match.
    """
    forward_path = Path(forward_file)
    reverse_path = Path(reverse_file)
    output_path = Path(output_file)

    for input_path in (forward_path, reverse_path):
        if not input_path.exists():
            raise FileNotFoundError(f"Input FASTQ file not found: {input_path}")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    pair_count = 0

    try:
        with open_text(forward_path, "r") as fwd, open_text(reverse_path, "r") as rev, open_text(
            output_path, "w"
        ) as out:
            fwd_records = SeqIO.parse(fwd, "fastq")
            rev_records = SeqIO.parse(rev, "fastq")

            for pair_number, (fwd_record, rev_record) in enumerate(
                zip_longest(fwd_records, rev_records), start=1
            ):
                if fwd_record is None or rev_record is None:
                    raise ValueError(
                        "Forward and reverse FASTQ files contain different numbers of reads "
                        f"(mismatch detected at pair {pair_number})."
                    )

                if validate_ids and normalized_read_id(fwd_record.id) != normalized_read_id(rev_record.id):
                    raise ValueError(
                        f"Read ID mismatch at pair {pair_number}: "
                        f"'{fwd_record.id}' vs '{rev_record.id}'."
                    )

                SeqIO.write(fwd_record, out, "fastq")
                SeqIO.write(rev_record, out, "fastq")
                pair_count += 1
    except Exception:
        # Avoid leaving a partial output behind when validation or parsing fails.
        if output_path.exists():
            output_path.unlink()
        raise

    return pair_count


def parse_args():
    parser = argparse.ArgumentParser(
        description="Interleave paired-end FASTQ files (plain or .gz compressed)."
    )
    parser.add_argument("forward_file", help="Forward/R1 FASTQ file")
    parser.add_argument("reverse_file", help="Reverse/R2 FASTQ file")
    parser.add_argument("output_file", help="Output interleaved FASTQ file")
    parser.add_argument(
        "--validate-ids",
        action="store_true",
        help="Require paired read IDs to match after removing common /1 and /2 suffixes.",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    pairs = interleave_fastq(
        args.forward_file,
        args.reverse_file,
        args.output_file,
        validate_ids=args.validate_ids,
    )
    print(f"Interleaved {pairs} read pairs into {args.output_file}")


if __name__ == "__main__":
    main()
