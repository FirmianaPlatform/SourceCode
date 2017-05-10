volcanoplot = function(x,y,xLimi,yLimi,treatment="treatment")
  {
  LOG10_005 = log10(0.05)
  LOG10_001 = log10(0.01)
  LOG2_2 = log2(2)
  LOG2_15= log2(1.5)

  
  mean.p=cbind(x,y)
  up1=mean.p[mean.p[,1] > LOG2_2 & mean.p[,2] > -LOG10_005, ]
  up2=mean.p[mean.p[,1] > LOG2_15 & mean.p[,1] < LOG2_2 & mean.p[,2] > -LOG10_005, ]
  up3=mean.p[mean.p[,1] > LOG2_2 & mean.p[,2] < -LOG10_005, ]
  
  down1=mean.p[mean.p[,1] < (-LOG2_2) & mean.p[,2] > -LOG10_005, ]
  down2=mean.p[mean.p[,1] < (-LOG2_15) & mean.p[,1] > (-LOG2_2) & mean.p[,2] > -LOG10_005, ]
  down3=mean.p[mean.p[,1] < (-LOG2_2) & mean.p[,2] < -LOG10_005, ]
  
  base =  mean.p[mean.p[,1] > (-LOG2_2) & mean.p[,1] < (LOG2_2) & mean.p[,2] < -LOG10_005, ]
  other = mean.p[mean.p[,1] > (-LOG2_15) & mean.p[,1] < (LOG2_15) & mean.p[,2] > -LOG10_005, ]
  
  up1.col = alpha("red",0.5)
  up2.col = alpha("orange",0.5)
  up3.col = alpha("orange",0.5)
  
  down1.col = alpha("blue",0.5)
  down2.col = alpha("light blue",0.5)
  down3.col = alpha("light blue",0.5)
  
  other.col = alpha("dark grey",0.5)
  line.col = "dark grey"
  
  par(mar = rep(5, 4))   
  plot(
  	#mean.p[,1], mean.p[,2],
  	base[,1],base[,2],
  	xlab=expression(paste("Log" ["2"], "( Ratio )")), ylab=expression(paste("-Log" ["10"], "( P value )")),
  	col=other.col , 
  	pch=16, main=paste("Plot type: ", treatment),
  	xlim=c(-xLimi,xLimi),ylim=c(0,yLimi),
  	cex.lab = 2
  	)
  axis(side=1, at=-xLimi:xLimi)
  if (length(up1)> 2){points(up1[,1], up1[,2],pch=16,col=up1.col)}
  if (length(up1)==2){points(up1[1],  up1[2], pch=16,col=up1.col)}
  
  if (length(up2)> 2){points(up2[,1], up2[,2],pch=16,col= up2.col)}
  if (length(up2)==2){points(up2[1],  up2[2], pch=16,col= up2.col)}
  
  if (length(up3)> 2){points(up3[,1], up3[,2],pch=16,col=up3.col)}
  if (length(up3)==2){points(up3[1],  up3[2], pch=16,col=up3.col)}
  
  if (length(down1)> 2){points(down1[,1], down1[,2],pch=16,col=down1.col )}
  if (length(down1)==2){points(down1[1],  down1[2], pch=16,col=down1.col )}
  
  if (length(down2)> 2){points(down2[,1], down2[,2],pch=16,col=down2.col )}
  if (length(down2)==2){points(down2[1],  down2[2], pch=16,col=down2.col )}
  
  if (length(down3)> 2){points(down3[,1], down3[,2],pch=16,col=down3.col )}
  if (length(down3)==2){points(down3[1],  down3[2], pch=16,col=down3.col )}
  
  if (length(other)> 2){points(other[,1], other[,2],pch=16,col=other.col )}
  if (length(other)==2){points(other[1],  other[2], pch=16,col=other.col )}
  
  abline(h=-LOG10_001, text(0,-LOG10_001 ,labels="Pvalue = 0.01", adj = c(0.5, -.2)),lty=3, col=line.col)
  abline(h=-LOG10_005, text(0,-LOG10_005 ,labels="Pvalue = 0.05", adj = c(0.5, -.2)),lty=3, col=line.col)
  
  abline(v=LOG2_15, lty=3, col=line.col)
  abline(v=-LOG2_15,lty=3, col=line.col)
  abline(v=LOG2_2,   lty=3, col=line.col)
  abline(v=-LOG2_2,  lty=3, col=line.col)

}

ggplotVolcano <- function(x,y)
{
  require(ggplot2)
  
  ##Highlight genes that have an absolute fold change > 2 and a p-value < Bonferroni cut-off
  
  P.Value <- y
  FC <- x
  df <- data.frame(P.Value, FC)
  df$threshold = as.factor(abs(df$FC) > 1 & df$P.Value < 0.05)
  
  ##Construct the plot object
  g = ggplot(data=df, aes(x=FC, y=-log10(P.Value), colour=threshold)) +
    geom_point(alpha=0.4, size=1.75) +
    theme(
        legend.position = "none",
        panel.background = element_rect(fill = "white", color = "black")
    ) + 
    geom_line(x=-log2(1.5)) + geom_line(x=log2(1.5)) + geom_line(x=-log2(2)) +geom_line(x=log2(2)) +
    geom_line(y=-log10(0.01)) + geom_line(y=-log10(0.05)) +
    xlim(c(-6, 6)) + ylim(c(0, 3)) +
    xlab("log2(Ratio)") + ylab("-log10(p-value)")
  print(g)
  return(df)

}

################
# usage:
# x: a vector containing the log2-ratios of your experiment
# y: a vector containing the corresponding p-values of your experiment
# treatment: a text string containing the title of your experiment
#
# example: 'input' contains 'mean-ratios', 'p-value'
# /usr/bin/Rscript volcano.R tmp/volcano_input.txt tmp/volcano_test


library(scales)

Args <- commandArgs(TRUE)
input_file = Args[1]
out_file = Args[2]
out_file_png   = paste(Args[2],".png",sep="")
out_file_pdf   = paste(Args[2],".pdf",sep="")
  
xLimi = as.numeric(Args[3])
yLimi = as.numeric(Args[4])

input=read.table(input_file,header=T,row.names=1,sep="\t")
title = 'Volcano'

png(out_file_png, type="cairo",units="in",width = 5, height = 5,pointsize=5.2,res=200)
#ggplotVolcano(input[,1], input[,2])
volcanoplot(input[,1], input[,2], xLimi,yLimi, title)
dev.off()

pdf(out_file_pdf,width=10,height=10)
#ggplotVolcano(input[,1], input[,2])
volcanoplot(input[,1], input[,2], xLimi,yLimi, title)
dev.off()


