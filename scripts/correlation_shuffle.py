#!/usr/bin/env python3# File paths
import random
import numpy as np
import pandas as pd
import glob
from scipy.stats import spearmanr, pearsonr
import os
import matplotlib.pyplot as plt
import statistics
from datetime import datetime

root_folders = [
    "/nfs/home/students/a.schuhe/scripts/splicingREMs/output_STITCHIT/H3K27ac",
    "/nfs/home/students/a.schuhe/scripts/splicingREMs/output_STITCHIT/H3K27me3",
    "/nfs/home/students/a.schuhe/scripts/splicingREMs/output_STITCHIT/H3K36me3",
    "/nfs/home/students/a.schuhe/scripts/splicingREMs/output_STITCHIT/H3K4me1",
    "/nfs/home/students/a.schuhe/scripts/splicingREMs/output_STITCHIT/H3K4me3",
    "/nfs/home/students/a.schuhe/scripts/splicingREMs/output_STITCHIT/H3K9me3"
]

# Column names for the dataframes
columns = ['Event', 'Event type', 'Total Amount of IHEC Entries', 
           'Amount Segments total', 'Segments total', 'Amount Significant Segments Spearman', 
           'Significant Segments Spearman', 'Significant Correlation Values Spearman', 
           'Correlation Values (total) Spearman', 'mean significant segments length Spearman', 
           'Amount Significant Segments Pearson', 'Significant Segments Pearson', 
           'Significant Correlation Values Pearson', 'Correlation Values (total) Pearson', 
           'mean significant segments length Pearson', 'Class', 'Iteration'] #'Region of interest'

# Significant Segments Spearman -> amount of significant segments (calculated with spearman and alpha as a threshold)
# Significant Segments Pearson -> amount of significant segments (caluclated with pearson and alpha as a threshold)

df_HM_SegSpearman = pd.DataFrame(columns=columns)

for root_folder in root_folders:
    for root, dirs, files in os.walk(root_folder):
        number_file_processed = 0
        print(f"PROCESSING THE ROOT FOLDER {root_folder}")
        for file in files:
            number_file_processed = number_file_processed+1
            print(f'i:{number_file_processed}')
            print(f'file:{file}')
        
            
            histone_modi = root_folder.rstrip().split("/")[5]
            segmentation_filepath = os.path.join(root, file)
            segmentation_filename = segmentation_filepath.rstrip().split("Segmentation")[1]
            eventID = segmentation_filepath.rstrip().split("_")[2] #number of the event 
            wildcard_event_id_complete_filepath = "/nfs/home/students/a.schuhe/scripts/splicingREMs/output_continous/" + f'{eventID}' + "*" + f'{histone_modi}.txt'
            wildcard_event_id_complete = glob.glob(wildcard_event_id_complete_filepath)[0]
            event_id_complete = wildcard_event_id_complete.rstrip().split("/")[5]
            event_type = event_id_complete.split("_")[2].split(":")[0] #SE or RI 
            
            p_or_s = segmentation_filename.rstrip().split("_")[3]
            p_or_s = p_or_s.rstrip().split(".")[0]
            
            if(p_or_s == "Pearson"): 
                continue
        
            skip_eventID =  ['000000000000010', '000000000000100', '000000000000101', '000000000000102', '000000000000103', '000000000000104', '000000000000105', '000000000000106', '000000000000107', '000000000000108', '000000000000210', '000000000000310', '000000000000410', '000000000000505','000000000000510', '000000000000565', '000000000000610', '000000000000659','000000000000676'] #skip the eventIDs where the Segmentation_..._Pearson.txt and Segmentation_..._Spearman.txt output files (generated by STITCHIT) have different segments -> checked with the code: size_check.py
            
            if eventID not in skip_eventID:

                processing_file = f'{histone_modi}_' + file
                print("Processing the file:" + processing_file )
                
                #Perform operation on each file
                with open(segmentation_filepath, 'r') as seg_file:

                    segments = seg_file.readline().rstrip().split("\t") #includes all the calculated segments (calculated by STITCHIT)
                    
                    amount_of_segments_ALL = len(segments) #INCLUDING the first element '' that indicates the rowname column and 'Expression' that indicates the PSI value column  --> real amount of segments = len(segments)-2
                    amount_of_computed_segments = len(segments)-2 #EXCLUDING the first element '' that indicates the rowname column AND 'Expression' that indicates the PSI value column  
                    
                    segment_vectors = [[] for i in range(amount_of_segments_ALL)] #it generates a sequence of numbers from 0 to amount_of_segments_ALL-1. It creates amount_of_segments_ALL empty lists (And it will iterate from 0 to amount_of_segments_ALL-1 (inclusive). There is a '-1' behind 'amount_of_segments_ALL' because the list starts with the indicator [0] 

                    lines = seg_file.readlines()

                    for line in lines:
                        line = line.rstrip().split("\t")
                        segment_vectors[0].append(line[0]) #segment_vectors[0] includes all the rownames (...fc.signal files) -> string remains unchanged

                        for i in range(1,amount_of_segments_ALL): #for each element in a row, 0->IHEC Entry identicator (first column), amount_of_segments_ALL-1-> Last column for PSI values (because the segments list starts with [0] for the IHEC entry identicators)
                            segment_vectors[i].append(float(line[i]))
                            


                    #segment_vectors[0] includes the rownames (...fc.signal filenames)
                    #segment_vectors[1] includes all the column values for the first segment
                    #segment_vectors[2] includes all the column values for the second segment
                    #etc.

                    psi_values = segment_vectors[amount_of_segments_ALL-1] #the last column is the indicator for the psi values (you have to calculate amount_of_segments_ALL-1 because there is a list with the indicator [0])
                
                    
                    #Shuffle the PSI value column from 1 to 100 (last column of segments) and calculate the correlations with the segments                    
                    for shuffle_amount in range(0,101):
                        
                        amount_significant_spearman = 0
                        amount_significant_pearson = 0
                        
                        lengths_sig_segments_spearman = []
                        lengths_sig_segments_pearson = []
                        
                        correlation_sig_spearman = []
                        correlation_sig_pearson = []
                        
                        correlation_total_spearman = []
                        correlation_total_pearson = []
                        
                        total_segments = []
                        significant_segments_spearman = []
                        significant_segments_pearson = []
                        
                        if(shuffle_amount == 0):
                            pass #0 times shuffeling -> psi_value column is not shuffeled & therefore, the psi_values column stays the same
                        else:  
                            random.shuffle(psi_values) #shuffle the PSI value column from 1 to 100 times 
                        
                        for i in range(1,amount_of_segments_ALL-1): #go through every segment column and check whether the p value for the segment is significant or not; only until amount_of_segments_ALL-1 to exclude the 'Expression' (PSI value) column
                            if(len(segment_vectors[0]) != len(segment_vectors[i])): #check if everything is correct respectively the amounts of rows and values in the segment column
                                print("There is a different amount of values in the lists.")
                                break

                            #calculate correlations
                            correlation, p_value_pearson = pearsonr(segment_vectors[i], psi_values)
                            rho, p_value_spearman = spearmanr(segment_vectors[i], psi_values)
                            alpha = 0.05
                            
                            correlation_total_pearson.append(correlation)
                            correlation_total_spearman.append(rho)
                            
                            #add the segment to the total_segments list
                            total_segments.append(segments[i])

                            #calculate length of the segment (does not depend on SE or RI)
                            segment_list = segments[i].rstrip().split(":")
                            length_segment_prepare = segment_list[1].rstrip().split("-")
                            length_segment = int(length_segment_prepare[1])-int(length_segment_prepare[0])
                                

                            if (p_value_spearman < alpha):#ignore the p values with a value bigger than alpha
                                amount_significant_spearman = amount_significant_spearman+1
                                lengths_sig_segments_spearman.append(length_segment)
                                correlation_sig_spearman.append(rho)
                                significant_segments_spearman.append(segments[i])


                            if (p_value_pearson < alpha):#ignore the p values with a value bigger alpha
                                amount_significant_pearson = amount_significant_pearson+1
                                lengths_sig_segments_pearson.append(length_segment)
                                correlation_sig_pearson.append(correlation)
                                significant_segments_pearson.append(segments[i])

                        #amount_significant -> amount of significant segments (regarding spearman or pearson) per histone modification per event
                        if(len(lengths_sig_segments_pearson) > 0):
                            mean_length_sig_segments_pearson = statistics.mean(lengths_sig_segments_pearson)
                        else:
                            pass

                        if(len(lengths_sig_segments_spearman) > 0):
                            mean_length_sig_segments_spearman = statistics.mean(lengths_sig_segments_spearman)
                        else:
                            pass
                        
                        #quick sanity check 
                        if (len(significant_segments_spearman) == amount_significant_spearman) and (len(significant_segments_pearson) == amount_significant_pearson):
                            pass
                        else:
                            print("The lengths of the significant segments is different. Look at your code!")
                            break
                        
                        #for later, include: Which segments? How many overlapping? Which ones are overlapping? How many Upstream or Downstream or Included? Which ones are Upstream or Downstream or Included? Those which are not overlapping -> print + Which difference do they have to the region of interest?

                        #Appending data to the current DataFrame
                        data = {
                            'Event': event_id_complete,
                            'Event type': event_type,
                            'Total Amount of IHEC Entries': len(segment_vectors[0]),
                            'Amount Segments total': amount_of_computed_segments,
                            'Segments total': total_segments,
                            'Amount Significant Segments Spearman': amount_significant_spearman,
                            'Significant Segments Spearman': significant_segments_spearman,
                            'Significant Correlation Values Spearman': correlation_sig_spearman, #list of correlation values 
                            'Correlation Values (total) Spearman': correlation_total_spearman,
                            'mean significant segments length Spearman': mean_length_sig_segments_spearman,
                            'Amount Significant Segments Pearson': amount_significant_pearson,
                            'Significant Segments Pearson': significant_segments_pearson,
                            'Significant Correlation Values Pearson': correlation_sig_pearson,
                            'Correlation Values (total) Pearson': correlation_total_pearson,
                            'mean significant segments length Pearson': mean_length_sig_segments_pearson,
                            'Class': histone_modi,
                            'Iteration': shuffle_amount
                        }
                        #'Region of interest': region_of_interest,
                  
                        if p_or_s == "Spearman":
                            df_HM_SegSpearman = df_HM_SegSpearman.append(data, ignore_index=True)
                            
            else:
                print(f'For the event ID {eventID} the generated Segmentation_..._Pearson.txt and Segmentation_..._Spearman.txt output files (by STITCHIT) do not match in the computed segments.')
                print("There is no output file generated for: " + event_id_complete )

df_HM_SegSpearman.to_csv('/nfs/home/students/a.schuhe/scripts/splicingREMs/output_CorrelationShuffle/df_HM_SegSpearman.csv', index=False)


