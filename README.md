# BCB5250 FASTQ Interleaving

This repository contains a Python script for interleaving paired-end FASTQ files.  
The script reads two separate FASTQ files (R1 and R2) and outputs a single interleaved FASTQ file.

##  How It Works
- Uses **BioPython** to read FASTQ records.
- Writes forward and reverse reads **sequentially** to an output file.
- Handles **exceptions** such as uneven read counts.

##  Running the Script
### **1. Install Dependencies**
```sh
pip install biopython --user
