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
