import gzip

import pytest
from Bio import SeqIO

from interleave_fastq import interleave_fastq


def write_fastq(path, records):
    with open(path, "w", encoding="utf-8") as handle:
        for name, seq in records:
            handle.write(f"@{name}\n{seq}\n+\n{'I' * len(seq)}\n")


def test_interleaves_reads_in_order(tmp_path):
    r1 = tmp_path / "r1.fastq"
    r2 = tmp_path / "r2.fastq"
    out = tmp_path / "out.fastq"
    write_fastq(r1, [("read1/1", "ACGT"), ("read2/1", "TTAA")])
    write_fastq(r2, [("read1/2", "TGCA"), ("read2/2", "AATT")])

    count = interleave_fastq(r1, r2, out, validate_ids=True)
    ids = [record.id for record in SeqIO.parse(out, "fastq")]

    assert count == 2
    assert ids == ["read1/1", "read1/2", "read2/1", "read2/2"]


def test_rejects_unequal_read_counts(tmp_path):
    r1 = tmp_path / "r1.fastq"
    r2 = tmp_path / "r2.fastq"
    out = tmp_path / "out.fastq"
    write_fastq(r1, [("read1/1", "ACGT"), ("read2/1", "TTAA")])
    write_fastq(r2, [("read1/2", "TGCA")])

    with pytest.raises(ValueError, match="different numbers of reads"):
        interleave_fastq(r1, r2, out)

    assert not out.exists()


def test_rejects_mismatched_ids_when_enabled(tmp_path):
    r1 = tmp_path / "r1.fastq"
    r2 = tmp_path / "r2.fastq"
    out = tmp_path / "out.fastq"
    write_fastq(r1, [("read1/1", "ACGT")])
    write_fastq(r2, [("other/2", "TGCA")])

    with pytest.raises(ValueError, match="Read ID mismatch"):
        interleave_fastq(r1, r2, out, validate_ids=True)

    assert not out.exists()


def test_supports_gzip_output(tmp_path):
    r1 = tmp_path / "r1.fastq"
    r2 = tmp_path / "r2.fastq"
    out = tmp_path / "out.fastq.gz"
    write_fastq(r1, [("read1/1", "ACGT")])
    write_fastq(r2, [("read1/2", "TGCA")])

    interleave_fastq(r1, r2, out, validate_ids=True)

    with gzip.open(out, "rt") as handle:
        ids = [record.id for record in SeqIO.parse(handle, "fastq")]
    assert ids == ["read1/1", "read1/2"]
