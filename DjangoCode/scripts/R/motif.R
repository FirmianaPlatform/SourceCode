Args <- commandArgs(TRUE)
input_file = Args[1]
out_file   = Args[2]
out_file_png = paste(Args[2], ".png", sep = "")
out_file_pdf = paste(Args[2], ".pdf", sep = "")
setwd(Args[3])
library(motifStack)

#input_file = file.path(find.package("motifStack"),"extdata","cap.txt")
input_file = '/usr/local/firmiana/leafy/gardener/scripts/R/Motif/input.txt'


protein <- read.table(input_file)
protein <- t(protein[,1:20])
motif <- pcm2pfm(protein)
motif <- new("pfm", mat = motif, name = "CAP",color = colorset(alphabet = "AA",colorScheme = "chemistry"))


png(out_file_png, type = "cairo",units = "in",width = 10, height = 5,pointsize = 5.2,res = 300)
plot(motif)
dev.off()

pdf(out_file_pdf, width = 10, height = 5)
plot(motif)
dev.off()
