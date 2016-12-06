
Args <- commandArgs()

# /usr/bin/Rscript stack_plot.R test.txt test
# Args[6]= test.txt  Args[7]= test.png 

input_file = Args[6]
out_file_png   = paste(Args[7],".png",sep="")
out_file_pdf   = paste(Args[7],".pdf",sep="")

library(ggplot2)
library(reshape2)
library(RColorBrewer)
library(scales)
library(grid)
df<-read.csv(input_file,header=T,row.names=1)

stackedDensityP <- function(tb){
  require(scales)
  melttb <- melt(tb)
  colnames(melttb) <- c("Samples", "Expression")
  #calculating log10(counts+1)
  for(x in 1:length(melttb[,1])){
    melttb[x,]$Expression <- log10(melttb[x,]$Expression+1)
  }
  #plotting + color setting
  #best choice of color: "Set3", "Spectral" (both support 10 groups)
  p  <- ggplot(melttb, aes(x=Expression, y = ..count../sum(..count..), fill=Samples)) + 
  #p <- ggplot(melttb, aes(x=Expression, y = ..count.., fill=Samples)) + 
    geom_density(alpha=.35) + 
    scale_fill_brewer("Samples", palette = "Spectral")
  #theme
  p <- p + 
    scale_y_continuous( "Density", labels = percent_format(), expand = c(0,0))+
    scale_x_continuous( "log10(Area +1)",expand = c(0,0))+
    #scale_x_continuous(limits=c(-0.001,0.001)) + 
    theme(
      panel.background = element_rect(fill = "white", color = "black"),
      #panel.grid.major = element_blank(),
      #panel.grid.minor = element_blank(),
      axis.text.y = element_text(angle = 00, color = "black", size = 15),
      axis.title = element_text(face = "bold", color = "black", size = 15),
      legend.title = element_text(face = "bold", color = "black", size = 12),
      legend.text = element_text(color = "black", size = 12),
      #custom theme
      axis.text.x = element_text(angle = 00, color = "black", size = 15)
    )
    
   #p <- p + geom_vline(xintercept=9,color = "black")
  print(p)
}
png(out_file_png, type="cairo",units="in",width = 5, height = 5,pointsize=5.2,res=300)
stackedDensityP(df)
dev.off()

pdf(out_file_pdf)
stackedDensityP(df)
dev.off()