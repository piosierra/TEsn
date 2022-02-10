# TEsn
Snakemake version of the TEs identification and genotyping pipeline.

## Inputs:
- File with sites genomic coordinates.  
`cat probeLocationFile_v8.txt | awk '{print $1}' | sed 's/..$//' > sites_list`

```
mkdir -p sites_files
awk -F" " '{print ($1 FS $1)}' sites_list | sed 's/:.* / /' | awk  -F" " '{print $2 >"sites_files/"$1}'
```

Create yaml for conda env:
`conda env export > env.yaml`

Run snakemake
```
snakemake -c1 --use-conda
snakemake --jobs 100 \
          --cluster "sbatch \
          -J sn1 \
          -A DURBIN-SL2-CPU \
          -p cclake \
          --time 29:00:00" \
          --use-conda &
```
Fields of alldatamerge:
ref
start
end
total_reads
m_reads
clips_r
clips_l
consensus_l
consensus_r

snakemake --use-conda -c1

```
