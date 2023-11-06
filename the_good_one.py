#!/usr/bin/env python

# This script was written using python version 3.11.5

import argparse
import re

def get_args():
    parser = argparse.ArgumentParser(description= "This script assumes a sorted sam file and outputs each first unique sam record to an output file and counts the number of total, unique, and duplicate sam records.")
    parser.add_argument("-f", "--file", help="absolute file path to sorted sam file", type=str)
    parser.add_argument("-o", "--output", help="absolute file path to deduplicated sam file", type=str)
    parser.add_argument("-u", "--umi", help="file containing the list of UMIs", type=str)
    return parser.parse_args()

args = get_args()
input_sam_file = args.file
output_sam_file = args.output
umi_file = args.umi

# umi_file = "/projects/bgmp/leylacuf/bioinfo/Bi624/Deduper/STL96_test.txt"
# input_sam_file = "Deduper/testfile_sorted.sam"
# output_sam_file = "Deduper/deduped.sam"


# Adding known UMIs to the UMI_list
def make_umi_list(umi_file):
    with open(umi_file, 'r') as fh1:
        for line in fh1:
            UMI_list.append(line.strip())
    return UMI_list


# Checking bitwise flag for forward or reverse strandedness
def check_bitwise_flag(flag):
    if (flag & 16):
        strand = "reverse"
    else:
        strand = "forward"
    return strand


# Adjusting the start position considering soft clipping. Example:
# cigar_string: "50M20D10S" 
# cigar_pattern: [(50, 'M'), (20, 'D'), (10, 'S')]
# length would take on the values 50, 20, and 10 

def adjust_start_position(flag, position, cigar_string):
    cigar_pattern = re.findall(r'(\d+)([MDNS])', cigar_string)
    for i, (length, pattern) in enumerate(cigar_pattern):
        if pattern == 'S' and i == 0 and check_bitwise_flag(flag) == "forward":
            soft_clipping_length = int(length)
            position -= soft_clipping_length
        elif check_bitwise_flag(flag) == "reverse":
            if "S" in cigar_pattern[0]:
                cigar_pattern = cigar_pattern[1::]
            for i in range(len(cigar_pattern)):
                position += int(cigar_pattern[i][0])
        return position
        
# print(adjust_start_position(16, 100, "10M10S20D"))
              

    #     elif pattern == 'S' and i != 0 and check_bitwise_flag(flag) == "reverse":
    #     elif pattern in ['M', 'N', 'D', 'S'] and check_bitwise_flag(flag) == "reverse":
    #         position += int(length)
    # return position

# def fwd_adjust_start_position(flag, position, cigar_string):
#     cigar_pattern = re.findall(r'(\d+)([MDNS])', cigar_string)
#     for length, pattern in cigar_pattern:
#         if pattern == 'S':
#             soft_clipping_length = int(length)
#             if check_bitwise_flag(flag) == "forward":
#                 position -= soft_clipping_length
#     return position

# def rvs_adjust_start_position(flag, position, cigar_string):
#     cigar_pattern = re.findall(r'(\d+)([MDNS])', cigar_string)
#     for length, pattern in cigar_pattern:
#         if pattern == 'M'


# cigar_pattern_regex = re.compile(r'(\d+)([MDNS])')
# def adjust_start_position(flag, position, cigar_string):
#     cigar_pattern = cigar_pattern_regex.findall(cigar_string)
#     for length, pattern in cigar_pattern:
#         if pattern == 'S':
#             soft_clipping_length = int(length)
#             if check_bitwise_flag(flag) == "forward":
#                 position -= soft_clipping_length
#             elif check_bitwise_flag(flag) == "reverse":
#                 position += soft_clipping_length
#     return position




UMI_list = []
def main():
    unique_reads = 0
    duplicates = 0
    total_reads = 0
    unknown_umi = 0
    previous_rname = None
    seen_record = set()
    make_umi_list(umi_file)
    with open(input_sam_file, 'r') as input_sam, open(output_sam_file, 'w') as deduped_sam:
        for line in input_sam:
            if line.startswith('@'):
                deduped_sam.write(line)  # Writing the headers to the output file
            else:
                total_reads += 1
                fields = line.strip().split('\t')
                UMI = fields[0].split(":")[-1]
                rname = fields[2]
                flag = int(fields[1])
                cigar_string = fields[5]
                position = int(adjust_start_position(flag, int(fields[3]), cigar_string))
                if UMI in UMI_list:
                    if rname != previous_rname:
                        previous_rname = rname
                        seen_record.clear()
                    if (UMI, rname, position, flag) in seen_record:
                        duplicates += 1
                    elif (UMI, rname, position, flag) not in seen_record:
                        seen_record.add((UMI, rname, position, flag))
                        deduped_sam.write(line)
                        unique_reads += 1
                if UMI not in UMI_list:
                    unknown_umi += 1
    print(f"Total reads: {total_reads}")
    print(f"Unique reads: {unique_reads}")
    print(f"Duplicates: {duplicates}")
    print(f"Unknown Umis: {unknown_umi}")


if __name__ == '__main__':
    main()
