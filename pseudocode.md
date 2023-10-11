Problem: 
Given a SAM file of uniquely mapped reads, remove all PCR duplicates

High level functions:
extract_umi
Description: This function looks at each SAM record and extracts the UMI from the QNAME
Input: SAM file (SAM col 1)
Return statement: returns UMI

soft_clip_check
Description: This function checks if the read has been soft clipped
### Input: SAM file (SAM col 6) (maybe find a way to check only the CIGAR string rather than the entire SAM record?)
### Return statement: returns location of soft clip base(s)

check_UMI
Description: This function checks if the UMI is in a dictionary/list/set
Input: dictionary/list/set (not sure which yet)
Return statement: returns TRUE or FALSE if the UMI is in the dictionary

check_strand
Description: This function looks at the bitwise flag to check strandedness (+ or -)
Input: bitwise flag of SAM file
Return statement: returns + or - to represent strandedness

## Pseudocode

create UMI dictionary/set

open SAM file
  write all lines that start with "@" to SAM output file
  line split/strip SAM header to assign variables to columns
  
