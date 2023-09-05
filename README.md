# splicingREMs

Author: Aïsha Schuhegger 

Advisor: Quirin Manz

Supervisor: Dr. Markus List

2nd Supervisor: Dr. Josch Pauling 


This repository includes all the scripts I have written, files I have used, and plots I have created to write my thesis. 
For more information or if you have any questions feel free to ask and write an e-mail to a.schuhegger@tum.de. 

In the following, I'd like to explain the repository's structure. After that, I explain its usage: 

**Structure of the repository**

**Archive:**
The /archive folder includes files and plots that I created but did not work with. 

**Correlation analysis:**
The output_CorrelationShuffle/ includes the data frames constructed for the correlation analysis. You must notice that the file "df_HM_SegSpearman.csv" is not included in this repository as it is too big. You need to create it independently with the script "correlation_shuffle.py".

**Discretized and continuous data:**
The discretized and continuous PSI values for every event can be seen in the output_discretized/ and output_continous/ folders. 

**Files:**
The annotation_events.gtf file is based on the gtf format (https://www.ensembl.org/info/website/upload/gff.html) and produced with the file /scripts/gtf.Rmd. It is necessary as input for the algorithm STITCHIT.
The files epiatlas_metadata.csv and events.csv.gz are previously computed datasets and are fundamental for this thesis. 
The hg38.chrom.sizes file includes the chromosome sizes of the human (https://www.ncbi.nlm.nih.gov/assembly/?term=GCA_000001405). 

**Plots:**
All the plots are contained in /plots. 

**Scripts:**
The scripts are available in /scripts. 
The file /scripts/run_stitchit.sh is for the execution of STITCHIT. You have to notice that STICHIT is not part of this repository. You have to set it up on your own (see https://github.com/SchulzLab/STITCHIT). 

**Usage of the repository**
Events.csv serves as the basis for all of my scripts. The scripts hclust-RI.Rmd and hclust-SE.Rmd are used to create three clusters per event type (RI and SE) by hierarchical clustering the events. Moreover, they extract the truly alternatively spliced events from the included or excluded events. Also, they set a threshold for the PSI values of the alternatively spliced events to distinguish whether these are discretized to 0 or 1. The files gtf.Rmd, discretized_form.Rmd and continuous_form.Rmd create the necessary input files for STITCHIT. You find the gtf file under the name "annotation_events.gtf", the events with discretized PSI values in the folder "output_discretized/" and those with continuous PSI values in "output_continuous/".  




