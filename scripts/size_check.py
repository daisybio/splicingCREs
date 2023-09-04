#!/usr/bin/env python3# File paths

import glob
import os

#Aim of the script: Check if the output files for one event ID regarding Pearson and Spearman genetrated by STITCHIT have the same segments and rows (they shouldn't differ because I ran STITCHIT with a p-value of 1)

root_folders = [
    "/nfs/home/students/a.schuhe/scripts/splicingREMs/output_STITCHIT/H3K27ac",
    "/nfs/home/students/a.schuhe/scripts/splicingREMs/output_STITCHIT/H3K27me3",
    "/nfs/home/students/a.schuhe/scripts/splicingREMs/output_STITCHIT/H3K36me3",
    "/nfs/home/students/a.schuhe/scripts/splicingREMs/output_STITCHIT/H3K4me1",
    "/nfs/home/students/a.schuhe/scripts/splicingREMs/output_STITCHIT/H3K4me3",
    "/nfs/home/students/a.schuhe/scripts/splicingREMs/output_STITCHIT/H3K9me3"
]

#In those lists eventIDs will be appended that have different segments regarding the output files of STITCHIT: Segmentation_..._Pearson.txt and Segmentation_..._Spearman.txt. 
H3K27ac_difSeg = []
H3K27me3_difSeg = []
H3K36me3_difSeg = []
H3K4me1_difSeg = []
H3K4me3_difSeg = []
H3K9me3_difSeg = []
allHM_difSeg = []


#In those lists eventIDs will be appended that have different rows (IHEC entries) regarding the output files of STITCHIT: Segmentation_..._Pearson.txt and Segmentation_..._Spearman.txt. 
H3K27ac_difRow = []
H3K27me3_difRow = []
H3K36me3_difRow = []
H3K4me1_difRow = []
H3K4me3_difRow = []
H3K9me3_difRow = []
allHM_difRow = []


for root_folder in root_folders:
    for root, dirs, files in os.walk(root_folder):
        for file in files:
            
            segmentation_filepath = os.path.join(root, file)
            segmentation_file_prefix = segmentation_filepath.rstrip().split("10")[0] #File prefix, e.g.: Segmentation_000000000000001_ 
            matching_segmentation_files = glob.glob(segmentation_file_prefix + '*')
            eventID = segmentation_filepath.rstrip().split("_")[2]
            histone_modi = root_folder.rstrip().split("/")[5]

            with open(matching_segmentation_files[0], 'r') as seg_file0, open(matching_segmentation_files[1],'r') as seg_file1:
                segments0 = seg_file0.readline().rstrip().split("\t")
                segments1 = seg_file1.readline().rstrip().split("\t")
                
                rows0 = []
                rows1 = []
                
                lines0 = seg_file0.readlines()
                lines1 = seg_file1.readlines()

                for line in lines0:
                    line = line.rstrip().split("\t")
                    rows0.append(line[0]) #rownames -> string remains unchanged
                
                for line in lines1:
                    line = line.rstrip().split("\t")
                    rows1.append(line[0])
                
                
                if (segments0 == segments1) and (rows0 == rows1):
                    pass
                else:
                    if(segments0 != segments1):
                        #print(f'The files with the event ID {eventID} do not match in segments.')
                        if histone_modi == "H3K27ac":
                            H3K27ac_difSeg.append(eventID)
                        elif histone_modi == "H3K27me3":
                            H3K27me3_difSeg.append(eventID)
                        elif histone_modi == "H3K36me3":
                            H3K36me3_difSeg.append(eventID)
                        elif histone_modi == "H3K4me1":
                            H3K4me1_difSeg.append(eventID)
                        elif histone_modi == "H3K4me3":
                            H3K4me3_difSeg.append(eventID)
                        elif histone_modi == "H3K9me3":
                            H3K9me3_difSeg.append(eventID)
                    elif(rows0 != rows1):
                        #print(f'The files with the event ID {eventID} do not match in rows (IHEC entries).')
                        if histone_modi == "H3K27ac":
                            H3K27ac_difRow.append(eventID)
                        elif histone_modi == "H3K27me3":
                            H3K27me3_difRow.append(eventID)
                        elif histone_modi == "H3K36me3":
                            H3K36me3_difRow.append(eventID)
                        elif histone_modi == "H3K4me1":
                            H3K4me1_difRow.append(eventID)
                        elif histone_modi == "H3K4me3":
                            H3K4me3_difRow.append(eventID)
                        elif histone_modi == "H3K9me3":
                            H3K9me3_difRow.append(eventID)
                    else:
                        print(f'The files with the event ID {eventID} do not match in segments and rows (IHEC entries).')


if(sorted(H3K27ac_difSeg) == sorted(H3K27me3_difSeg) == sorted(H3K4me3_difSeg)):
    print('Regarding the Histone Modifications H3K27ac, H3K27me3 and H3K4me3: There is no difference in the amount of different segments in H3K27ac and H3K27me3.')
    print(f'There are {len(H3K27ac_difSeg)} files and therefore {len(H3K27ac_difSeg)/2} eventIDs (in each Histone Modification output folder) that have a different amount of segments between the output files (Segmentation_..._Pearson.txt and Segmentation_..._Spearman.txt) eventrated by STITCHIT.')

if(sorted(H3K36me3_difSeg) == sorted(H3K4me1_difSeg) == sorted(H3K9me3_difSeg)):
    print('Regarding the Histone Modifications H3K36me3, H3K4me1 and H3K9me3: There is no difference in the amount of different segments in H3K27ac and H3K27me3.')
    print(f'There are {len(H3K36me3_difSeg)} files and therefore {len(H3K36me3_difSeg)/2} eventIDs (in each Histone Modification output folder) that have a different amount of segments between the output files (Segmentation_..._Pearson.txt and Segmentation_..._Spearman.txt) eventrated by STITCHIT.')
print(f'The difference between these lies in the event IDs: {set(sorted(H3K27ac_difSeg)) ^ set(sorted(H3K36me3_difSeg))}.')
  
if(sorted(H3K27ac_difRow) == sorted(H3K27me3_difRow) == sorted(H3K36me3_difRow) == sorted(H3K4me1_difRow) == sorted(H3K4me3_difRow) == sorted(H3K9me3_difRow)):
    print(f'There are {len(H3K27ac_difRow)} files that differ in their rows (IHEC entries) between Segmentation_..._Pearson.txt and Segmentation_..._Spearman.txt.')
else:
    print('Something went wrong. Rework your workflow in this file.')
    
