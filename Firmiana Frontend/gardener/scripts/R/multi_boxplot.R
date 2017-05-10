library(ggplot2)
#library(reshape2)
#library(RColorBrewer)
#library(scales)
#library(grid)

# /usr/bin/Rscript multi_boxplot.R tmp/boxdata.txt tmp/multi_box
Args <- commandArgs()
input_file = Args[6]
out_file_png   = paste(Args[7],".png",sep="")
out_file_pdf   = paste(Args[7],".pdf",sep="")

df<-read.table(input_file,header=T)

samplePlotboxP <- function(tb){

  melttb <- tb
  
  if(TRUE){
  geneSymbol <- melttb$Symbol
  geneSymbol <- as.character(geneSymbol)
  index <- duplicated(geneSymbol)
  gs <- geneSymbol[!index]
  melttb$Symbol <- factor(melttb$Symbol, ordered=TRUE, levels=gs)}
  
# bp <- ggplot(melttb) + geom_boxplot(aes(x=Group,  y=Expression,fill=Symbol) ) + ylab('Log10(Expression)')
  bp <- ggplot(melttb) + geom_boxplot(aes(x=Group, y=Expression,fill=Symbol),alpha=0.9,size=0.1 ) + ylab('Log10(Expression)') +facet_wrap(~Symbol,nrow=1) #+geom_vline(xintercept = )
  bp <- bp + scale_y_log10() + 
  # bp <- bp + geom_vline(xintercept=9,color = "black")
    theme(
      panel.background = element_rect(fill = "white", color = "black"),
      #panel.grid.major = element_blank(),
      #panel.grid.minor = element_blank(),
      legend.title = element_text(face = "bold", color = "black", size = 10),
      legend.text = element_text(color = "black", size = 8),
      axis.title.x = element_blank(),
      axis.text.x = element_text(angle = 90, color = "black", size = 12),
      axis.text.y = element_text(angle = 00, color = "black", size = 8)
    )
  
  pdf(out_file_pdf,width = 20, height = 5)     
  print(bp)
  dev.off()
  
  png(out_file_png, type="cairo",units="in",width = 20,height=5,pointsize=5.2,res=300)
  print(bp)
  dev.off()
}

samplePlotboxP(df)
