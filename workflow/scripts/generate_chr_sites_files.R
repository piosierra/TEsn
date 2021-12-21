library(stringr)
dir <- snakemake@params[[1]]
sites_list <- read.delim(snakemake@input[[1]], header = F)
setwd(dir)
print("------------------------------------------------------------")
print("Working directory:")
print(dir)

if (!(file.exists("sites_files_"))) {
    dir.create("sites_files_")
}
setwd("sites_files_")


colnames(sites_list) <- c("Site", "samples_list")

sites_list$type <- sub("^.*(.)$", "\\1", sites_list$Site)
sites_list$Site <- sub("_[OG]","", sites_list$Site)
sites_short <- data.frame(ref= gsub("[^:]*$","",sites_list$Site),start=gsub(".*:(.+)-.*", "\\1",sites_list$Site), end=gsub(".*-", "",sites_list$Site))

refs <- unique(substr(sites_short$ref,1,5))

for (i in refs) {
 sites_set <- sites_short[grepl(i,sites_short$ref),]
 sites_set[,1] <- str_replace(sites_set[,1],":","")
 write.table(sites_set, paste0("sites_set_", str_replace(i,":","")), quote = F, col.names = F, row.names = F, sep = "\t")
}
