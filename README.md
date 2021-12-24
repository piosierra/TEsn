# TEsn
Snakemake version of the TEs identification and genotyping pipeline.

## Inputs:
- File with sites genomic coordinates.
`cat probeLocationFile_v8.txt | awk '{print $1}' | sed 's/..$//' > sites_list`

mkdir -p sites_files
awk -F" " '{print ($1 FS $1)}' sites_list | sed 's/:.* / /' | awk  -F" " '{print $2 >"sites_files/"$1}'

- 

snakemake -d "$HOME/rds/rds-durbin-group-8b3VcZwY7rY/projects/cichlid/pio/data2/" -c1