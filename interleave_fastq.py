#!/usr/bin/env python3
import argparse
from Bio import SeqIO

def interleave_fastq(forward_file, reverse_file, output_file):
    """
    Interleaves paired-end FASTQ files into a single output FASTQ file.
    :param forward_file: Path to the forward reads FASTQ file.
    :param reverse_file: Path to the reverse reads FASTQ file.
    :param output_file: Path to the output interleaved FASTQ file.
    """
    try:
        with open(forward_file, "r") as fwd, open(reverse_file, "r") as rev, open(output_file, "w") as out:
            fwd_records = SeqIO.parse(fwd, "fastq")
            rev_records = SeqIO.parse(rev, "fastq")
            
            for fwd_record, rev_record in zip(fwd_records, rev_records):
                SeqIO.write(fwd_record, out, "fastq")
                SeqIO.write(rev_record, out, "fastq")
                
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Interleave Paired-End FASTQ Files')
    parser.add_argument('forward_file', help='Forward reads FASTQ file')
    parser.add_argument('reverse_file', help='Reverse reads FASTQ file')
    parser.add_argument('output_file', help='Output interleaved FASTQ file')
    args = parser.parse_args()
    
    interleave_fastq(args.forward_file, args.reverse_file, args.output_file)

