# splicingREMs

Author: Aïsha Schuhegger 

Advisor: Quirin Manz

Supervisor: Dr. Markus List

2nd Supervisor: Dr. Josch Pauling 


This repository includes all the scripts I have written, files I have used and plots I have created to write my thesis. 
For more information or if you have any questions feel free to ask and write an e-mail to a.schuhegger@tum.de. 

In the following, the structure of the repository is explained: 

**Archive:**
The /archive fodler includes files and plots that I created but did not work with in the end. 

**Correlation analysis:**
The output_CorrelationShuffle/ includes the data frames constructed for the correlation analysis. You have to notice that the fiel "df_HM_SegSpearman.csv" is not included in this repository as it is too big. You need to create it on your own with the script "correlation_shuffle.py".

**Discretized and continous data:**
The discretized and continous PSI values for every event can be seen in the output_discretized/ and output_continous/ folders. 

**Files:**
The annotation_events.gtf file is based on the gtf format (https://www.ensembl.org/info/website/upload/gff.html) and produced with the file /scripts/gtf.Rmd. It is necessary as input for the algorithm STITCHIT.
The file epiatlas_metadata.csv and events.csv.gz are previously computed dataset and serve as fundament for this thesis. 
The hg38.chrom.sizes file includes the chromosome sizes of the human (https://www.ncbi.nlm.nih.gov/assembly/?term=GCA_000001405). 

**Plots:**
All the plots are contained in /plots. 

**Scripts:**
The scripts are available in /scripts. 
The file /scripts/run_stitchit.sh is for the execution of STITCHIT. You have to notice that STICHIT is no part of this repository. You have to set it up on your own (see https://github.com/SchulzLab/STITCHIT). 




