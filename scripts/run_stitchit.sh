#!/bin/bash

start=500
end=689
modifications=('H3K27ac' 'H3K27me3' 'H3K36me3' 'H3K4me1' 'H3K4me3' 'H3K9me3')

for ((i=start; i<=end; i++))
do
  file=$(printf "%015d" "$i")

  for modification in "${modifications[@]}"
  do
    discretized_file="/nfs/home/students/a.schuhe/scripts/splicingREMs/output_discretized/${file}_*_${modification}.txt"
    continous_file="/nfs/home/students/a.schuhe/scripts/splicingREMs/output_continous/${file}_*_${modification}.txt"

    echo "Processing file: ${discretized_file}"

    ./nfs/proj/splicingREMs/STITCHIT_quirinmanz/STITCHIT/build/core/STITCH  -b /nfs/data3/IHEC/ChIP-Seq \
      -a /nfs/home/students/a.schuhe/scripts/splicingREMs/annotation_events.gtf \
      -d $discretized_file \
      -o $continous_file \
      -s /nfs/home/students/a.schuhe/scripts/splicingREMs/hg38.chrom.sizes \
      -w 2500 -c 1 -p 1 -g "${file}" -z 10 \
      -f /nfs/home/students/a.schuhe/scripts/splicingREMs/output_STITCHIT/$modification \
      -r 50000 -t 150
  done
done
