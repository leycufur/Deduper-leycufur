
# Deduper

## Overview
The Deduper script is designed to efficiently remove PCR duplicates from sorted SAM files containing single-end reads. It processes files while managing memory use effectively to handle large datasets, such as those commonly found in genomic studies.

## Features
- **UMI Support**: Works with user-provided lists of UMIs to accurately identify unique reads.
- **CIGAR String Adjustment**: Adjusts read positions based on CIGAR strings to accurately determine duplicates, accounting for soft clipping and other modifications.
- **Bitwise Flag Check**: Determines the orientation (forward or reverse) of reads to ensure accurate deduplication.
- **Performance Metrics**: Outputs statistics on total reads processed, number of unique reads, duplicates, and unknown UMIs.

## Requirements
- Python 3.11.5 or higher

## Installation
Clone the repository and navigate into the directory:
```bash
git clone https://github.com/<your-github-username>/Deduper-<your-github-username>.git
cd Deduper-<your-github-username>
```

## Usage
To run the Deduper script, use the following command:
```bash
./<your_last_name>_deduper.py -u <umi_file.txt> -f <input_sorted.sam> -o <output_deduped.sam>
```
### Command-line Arguments
- `-f, --file`: Specifies the absolute file path to the sorted SAM file.
- `-o, --output`: Specifies the absolute file path to output the deduplicated SAM file.
- `-u, --umi`: Specifies the file containing the list of UMIs.
- `-h, --help`: Displays help information.

## Function Descriptions
- **`get_args()`**: Parses command-line arguments using argparse.
- **`make_umi_list(umi_file)`**: Reads UMIs from a file and stores them in a list for quick access.
- **`check_bitwise_flag(flag)`**: Checks the bitwise flag from the SAM file to determine the read's strand.
- **`adjust_start_position(flag, position, cigar_string)`**: Adjusts the start position of a read considering its CIGAR string and strand orientation.

## Example Input and Output
**Input (SAM format)**:
```
@header_line
NS500451:154:HWKTMBGXX:1:11101:10000:1000 16 chr1 3000001 60 50M * 0 0 ...
```
**Output (SAM format)**:
```
@header_line
NS500451:154:HWKTMBGXX:1:11101:10000:1000 16 chr1 3000001 60 50M * 0 0 ...
```

## Contributing
Contributions are welcome! Please fork the repository and submit pull requests, or create issues for bugs and feature requests.
