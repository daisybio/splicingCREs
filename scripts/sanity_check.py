#!/usr/bin/env python3

import numpy as np
from scipy.stats import pearsonr
import glob
import decimal
import os

#segmentation_file = "/nfs/home/students/a.schuhe/scripts/splicingREMs/output_STITCHIT/*"
#histone_modifications = ['H3K27ac',  'H3K27me3',  'H3K36me3',  'H3K4me1',  'H3K4me3',  'H3K9me3']


root_folders = [
    "/nfs/home/students/a.schuhe/scripts/splicingREMs/output_STITCHIT/H3K27ac",
    "/nfs/home/students/a.schuhe/scripts/splicingREMs/output_STITCHIT/H3K27me3",
    "/nfs/home/students/a.schuhe/scripts/splicingREMs/output_STITCHIT/H3K36me3",
    "/nfs/home/students/a.schuhe/scripts/splicingREMs/output_STITCHIT/H3K4me1",
    "/nfs/home/students/a.schuhe/scripts/splicingREMs/output_STITCHIT/H3K4me3",
    "/nfs/home/students/a.schuhe/scripts/splicingREMs/output_STITCHIT/H3K9me3"
]

for root_folder in root_folders:
    for root, dirs, files in os.walk(root_folder):
        for file in files:
            histone_modi = root_folder.rstrip().split("/")[5]
            segmentation_file = os.path.join(root, file)
            geneID = segmentation_file.rstrip().split("_")[2]
            wildcard_relevant_compare_file = "/nfs/home/students/a.schuhe/scripts/splicingREMs/output_continous/" + f'{geneID}' + "*" + f'{histone_modi}.txt'
            relevant_compare_file = glob.glob(wildcard_relevant_compare_file)[0]

            # Perform operations on each file
            with open(relevant_compare_file, 'r') as rel_file:
                lines = rel_file.readlines()
                psi_values = lines[1]
                psi_list = psi_values.rstrip().split("\t")
                psi_list.pop(0) #delete geneID
                relevant_names = lines[0].rstrip().split("\t")

            hash_psi_original = {key: value for key, value in zip(relevant_names, psi_list)}

            seg_psi_values = []
            seg_names = []

            with open(segmentation_file, "r") as seg_file:
                lines = seg_file.readlines()
                for line in lines[1:]:
                    row = line.rstrip().split("\t")
                    seg_psi_value = row[-1]
                    seg_name = row[0]
                    seg_psi_values.append(seg_psi_value)
                    seg_names.append(seg_name)

            hash_psi_segmentation = {key: value for key, value in zip(seg_names, seg_psi_values)}

            keys_match = set(hash_psi_original.keys()) == set(hash_psi_segmentation.keys())

            if keys_match:
                pass
                #print("The row names of the Segmentation File match with the given input names.")
            else:
                print("The row names don't match!")

            values_identical = True

            for key in hash_psi_segmentation:
                value_seg = hash_psi_segmentation[key]
                digits_seg = value_seg.replace(".","")
                num_digits_seg = len(digits_seg)-1 #exclude leading 0
                value_orig = decimal.Decimal(hash_psi_original[key])
                value_original = round(value_orig, num_digits_seg)

                #if not str(value_original).startswith(value_seg):
                if str(value_original)[:5] != value_seg[:5]: #after the first check -> the first five digits must be equal between both (may be caused due to rounding inaccuracies)
                    values_identical = False
                    print(value_original)
                    print(value_seg)
                    break

            if values_identical:
                pass
                #print("The values of hash_psi_segmentation are identical to the first digits of the values of hash_psi_original.")
            else:
                print("The values of hash_psi_segmentation are not identical to the first digits of the values of hash_psi_original.")
                print(segmentation_file)
                print(relevant_compare_file)
