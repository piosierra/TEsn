

# Checks all the reads on a site for a sample, and gets creates a consensus 
# sequence of the edges of clipped reads.

import sys
import pysam
import pandas as pd
import os
from re import search
# from spoa import poa

# Returns the most frequent char on a string. In case of ties it returns the 
# last to tie for it.

def most_freq_char(chars):
    dictionary = dict.fromkeys(chars,0)
    for c in chars:
        dictionary[c]+=1
    return sorted(dictionary.items(), key=lambda item: item[1])[-1][0]
  
    
# Returns the consensus of several strings. Uses the same dictionary as them.
  
def silly_consensus(seq_list):
    seq_list = sorted(seq_list, key=len)
    consensus=""
    while len(seq_list) > 1:
        chars=""
        for i in range(len(seq_list)):
            chars= chars+seq_list[i][0]
            seq_list[i]=seq_list[i][1:]
        seq_list = list(filter(None, seq_list))
        consensus=consensus+most_freq_char(chars)
    if len(seq_list) == 1:
        consensus=consensus+seq_list[0]    
    return consensus
        
output_path = "sites_explored"

if not os.path.exists(output_path):
    os.makedirs(output_path)
os.chdir(output_path)


# print([x for x in snakemake.input if not search("cram",x)])
# sample = snakemake.input.sample[0]
# sites_f = snakemake.input.site[0]

sample_path = sys.argv[1]
sites_f = sys.argv[2]
sample_id = sys.argv[3]

print(samples_f)
print(sites_f)
print(output_path)

if not os.path.exists(sample_id):
    os.makedirs(sample_id)
os.chdir(sample_id)
sample_file = pysam.AlignmentFile(sample_path, "rc")
with open(sites_f) as sites:
    data = []
    c = ""
    for site in sites:
        c,s,e = site.split()
        r = c+":"+s+"-"+e
        iter = sample_file.fetch(region = r)
        start = int(s)
        end = int(e)
        s_l = []
        s_r = []
        consensus_l = "-"
        consensus_r = "-"
        reads_m = 0   # Total full M reads
        clips_l = 0   # Total S+H left clips (at the right of the insertion)
        clips_r = 0   # Total S+H right clips (at the left of the insertion)
        total_reads = 0     # Total # of reads
        for x in iter:
            total_reads +=1
            if x.cigartuples is not None:
                if (x.cigartuples[0][0] == 0 and x.cigartuples[-1][0] == 0 \
                    and x.get_reference_positions()[0] < start and x.get_reference_positions()[-1] > end):                      
                    reads_m +=1
                elif (x.cigartuples[0][0] == 5 or x.cigartuples[0][0] == 4) \
                    and x.cigartuples[-1][0]!= 4 and x.cigartuples[-1][0]!= 5 \
                    and  x.reference_start > start-2 \
                    and x.reference_start < end+2 :
                    s_r.append(x.query_sequence[0:x.cigartuples[0][1]][::-1])            
                    clips_l +=1
                elif (x.cigartuples[-1][0] == 5 or x.cigartuples[-1][0] == 4) \
                    and x.cigartuples[0][0]!= 4 and x.cigartuples[0][0]!= 5 \
                    and (x.reference_start + x.cigartuples[0][1]) > start-2 \
                    and (x.reference_start + x.cigartuples[0][1]) < end+2 :
                    s_l.append(x.query_sequence[-x.cigartuples[-1][1]:])  
                    clips_r +=1
        if len(s_l)>0:
            consensus_l = silly_consensus(s_l)
        if len(s_r)>0:
            consensus_r = silly_consensus(s_r)
        data.append([c,s,e,total_reads,reads_m,clips_r,clips_l,consensus_l, consensus_r])    
    df = pd.DataFrame(data, columns=["ref", "start", "end", "total_reads",
                                    "m_reads", "clips_r", "clips_l", 
                                    "consensus_l", 
                                    "consensus_r"])
    df.to_csv(sample_id+"_" + c, sep="\t", index=False)
os.chdir("..")