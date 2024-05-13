#!/usr/bin/env python
"""
Script: vcf2msa.py
Description: Convert VCF (Variant Call Format) file to FASTA format.
Author: Utpal Smart
Date: 05.03.2024

Usage:
    python vcf2msa.py <file.vcf>

Input:
    - VCF file containing variant call data. This can either be a multivcf or a single-sample vcf.

Output:
    - Two files:
        - 'nucleotides_header.txt': Header file containing the list of individuals.
        - 'nucleotides_<filename>.fasta': FASTA file containing nucleotide sequences.

Steps:
    1. Read the input VCF file.
    2. Extract header information to create a list of individuals.
    3. Process each genotype field to extract nucleotide data.
    4. Write the nucleotide sequences aligned with the corresponding headers to the FASTA file.
    5. Print the number of individuals (NTAX) processed.

Notes:
    - Assumes haploid data format in the VCF file.
    - Assumes format to be GT:AD:DP:GQ:PL.
    - The likelihood field (PL) is used to determine the genotype.
    - If the likelihood is "0,0", the nucleotide is considered missing and represented as 'N'. 

    """

import sys

# Check if VCF file argument is provided
if len(sys.argv) != 2:
    print("Usage: python script.py file.vcf")
    sys.exit(1)

vcf_file = sys.argv[1]

try:
    # Open VCF file for reading
    with open(vcf_file, 'r') as vcf:
        # Open output files
        with open("nucleotides_header.txt", 'w') as out_header, open("nucleotides_" + vcf_file + ".fasta", 'w') as out_fasta:
            # Initialize dictionary to store nucleotides for each individual
            individuals = {}

            # Process VCF file line by line
            for line in vcf:
                line = line.strip()
                if line.startswith("#CHROM"):  # Make header file
                    inds = line.split()[9:]
                    ntax = len(inds)
                    print("NTAX =", ntax)  # Echo number of individuals
                    # Print header line
                    out_header.write(" ".join([ind + "-" for ind in inds]) + "\n")
                    # Initialize dictionary entries for each individual
                    individuals = {ind: [] for ind in inds}
                elif not line.startswith("#"):
                    fields = line.split()
                    scaff = fields[0]
                    pos = fields[1]
                    ref = fields[3]
                    alt = fields[4]
                    # Process each genotype field
                    for ind, gt in zip(inds, fields[9:]):
                        gt_parts = gt.split(":")
                        # Extract nucleotide
                        if gt_parts[4] == "0,0":  # Check if likelihood is "0,0"
                            nucleotide = 'N'  # Assign 'N' if likelihood is "0,0,0"
                        else:
                            nucleotide = ref if gt_parts[0] == '0' else alt
                        # Add nucleotide to individual's list
                        individuals[ind].append(nucleotide)

            # Write out nucleotides aligned with the corresponding headers
            for ind in inds:
                out_fasta.write(">" + ind + "\n")  # Write header with a newline
                out_fasta.write("".join(individuals[ind]) + '\n')  # Write sequence

except FileNotFoundError:
    print("File not found:", vcf_file)  # Echo file not found error
    sys.exit(1)
