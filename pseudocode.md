Problem: 
Given a SAM file of uniquely mapped reads, remove all PCR duplicates
```
check_UMI
Description: This function checks if the UMI is in a dictionary/list/set
Input: dictionary/list/set (not sure which yet)
Return statement: returns TRUE or FALSE if the UMI is in the dictionary

example: NS500451:154:HWKTMBGXX:1:11101:94095:71756:AACGCCAT
input: check_UMI(AACGCCAT)
return: TRUE

check_start
Description: This function looks at the CIGAR string to check for soft clipping and adjusts the start position 
Input: appropriate SAM columns
Return statement: returns adjusted start position

example: read    0    chr4    500    30    10S40M    =    600    0    TTAGGCTACG    GGGGG    XT:A:U    RG:Z:2
input: cols 2, 4, 6 
check_start(0, 500, 10S40M)
return: start position: 490
```
```
High-Level Steps
Initialize data structures to keep track of processed reads and UMIs.
Parse the input SAM file line by line.
Extract the UMI from the QNAME field.
Check if the UMI and alignment position uniquely identify a read.
If the read is unique, write it to the output SAM file and mark the UMI as processed.
Repeat for each line in the input SAM file.
Close the input and output files.
```
Pseudocode

```
create UMI dictionary/set from provided file
create and empty set that stores "checked off" UMIs 

open SAM file
  if line starts with "@"
    write to output

  line split/strip SAM header to assign variables to columns
    check if the UMI in the record matches one in the dictionary using check_UMI
      if TRUE 
        write that line to the output file
        add UMI to "checked" set
     else
        check_start to adjust start position
          check if UMI is in dictionary
            if check_UMI is not in set
              add to set and write to output file
            
        

  
```
