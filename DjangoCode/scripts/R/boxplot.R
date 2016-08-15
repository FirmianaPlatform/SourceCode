library(ggplot2)
library(reshape2)
library(RColorBrewer)
library(scales)
library(grid)


Args <- commandArgs(TRUE)

# /usr/bin/Rscript non_cluster_heatmap.R tmp/test.txt tmp/test.png title '#FF0000' '#0000FF'
# Args[6]= test.txt  Args[7]= test.png 

input_file = Args[1] #"/usr/local/firmiana/leafy/static/images/tmp/heatmap_tmp/firheatmap_1442109378.8/boxplot.txt"
out_file   = Args[2]

out_file_png   = paste(Args[2],".png",sep="")
out_file_pdf   = paste(Args[2],".pdf",sep="") #"/usr/local/firmiana/leafy/static/images/tmp/heatmap_tmp/firheatmap_1442109378.8/boxplot.png"

df<-read.csv(input_file,header=T,row.names=1)
samplePlotboxP <- function(tb){
  #melt tb 
  melttb <- melt(tb)
  #rename column
  colnames(melttb) <- c("Samples", "Expression")
  
  #plotting + color
  bp <- ggplot(data = melttb, aes(x=Samples, y=Expression)) + 
    geom_boxplot(aes(fill=Samples)) + 
    scale_fill_brewer("Samples", palette = "Spectral")
  #labels and background
  bp <- bp + scale_y_log10() + 
    theme(
      panel.background = element_rect(fill = "white", color = "black"),
      panel.grid.major = element_blank(),
      panel.grid.minor = element_blank(),
      axis.text.x = element_text(angle = 90, color = "black", size = 15),
      axis.text.y = element_text(angle = 00, color = "black", size = 15),
      axis.title = element_text(face = "bold", color = "black", size = 15),
      legend.title = element_text(face = "bold", color = "black", size = 15),
      legend.text = element_text(color = "black", size = 15)
    )
  print(bp)
}
pdf(out_file_pdf,width = 10, height = 10)
samplePlotboxP(df)
dev.off()
