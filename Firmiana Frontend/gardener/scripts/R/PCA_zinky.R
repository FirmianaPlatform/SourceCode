# /usr/bin/Rscript PCA_zinky.R tmp/temp_pca.txt tmp/pca_zinky "PC1,PC2" "Exp001052,Exp001053,Exp001054,Exp001055,Exp001056,Exp001057,Exp001058,Exp001059,Exp001060,Exp001061,Exp001062,Exp001063,Exp001068,Exp001069,Exp001070,Exp001071,Exp001072,Exp001073"

library(ggplot2)
library(reshape2)
library(RColorBrewer)
library(scales)
library(grid)
library(FactoMineR)

Args <- commandArgs()
input_file = Args[6]
out_file_png   = paste(Args[7],".png",sep="")
out_file_pdf   = paste(Args[7],".pdf",sep="")

#input_file = 'D:\\firmiana\\R\\Zinky\\PCA\\data.txt'
#out_file   = 'D:\\firmiana\\R\\Zinky\\PCA\\pca.png'
plotDim1 = unlist(strsplit(Args[8],","))[1]
plotDim2 = unlist(strsplit(Args[8],","))[2]

#conditionstr = "Exp001052,Exp001053,Exp001054,Exp001055,Exp001056,Exp001057,Exp001058,Exp001059,Exp001060,Exp001061,Exp001062,Exp001063,Exp001068,Exp001069,Exp001070,Exp001071,Exp001072,Exp001073"
conditionstr = Args[9]
conditionlist = unlist(strsplit(conditionstr,","))

df<-read.table(input_file,header=T,row.names=1)
#convert userinput data and condition list for PCA analysis
dataForPCAinitialize<-function(data,conditionlist){
  data<-t(data)
  data<-data.frame(condition=conditionlist,data)
  return(data)
}

#get ggplot2 output result
getPCAplot <- function(data,conditionlist,isText=FALSE){
  a<-dataForPCAinitialize(data,conditionlist)
  pca <-PCA(a[,2:ncol(a)], scale.unit=T, graph=F,ncp=3)
  ctri<-pca$eig[,2][1:3]
  names(ctri)<-c("PC1","PC2","PC3")#,"PC4","PC5")
  xlabtemp=paste(plotDim1," (",round(ctri[plotDim1],2),"%)",sep="")
  ylabtemp=paste(plotDim2," (",round(ctri[plotDim2],2),"%)",sep="")
  colnames(pca$ind$coord)<-c("PC1","PC2","PC3")#,"PC4","PC5")
  pc1 <- pca$ind$coord[,plotDim1]
  pc2 <- pca$ind$coord[,plotDim2]
  maxX=max(pc1)*1.1
  maxY=max(pc2)*1.1
  plotdata <- data.frame(Condition=a[,1],pc1,pc2) 
  plotdata$Condition <- factor(plotdata$Condition)
  plot <- ggplot(plotdata, aes(pc1,pc2),environment = environment()) + 
    geom_point(aes(colour = Condition),size = 5) + 
    theme(panel.border = element_rect(linetype = "dashed")) + 
    theme_bw() +
    #ylim(-maxY,maxY)+
    #xlim(-maxX,maxX)+
    scale_x_continuous(xlabtemp,limits=c(-maxX,maxX))+
    scale_y_continuous(ylabtemp,limits=c(-maxY,maxY))+
    theme(legend.text = element_text(colour="blue", size = 16, face = "bold")) + 
    theme(legend.justification=c(1,0),legend.position="right")+
    theme(legend.title = element_text(colour="black", size=16, face="bold"))+
    scale_fill_brewer(palette="Spectral")
  if(isText){
    plot<-plot+geom_text(aes(label=rownames(plotdata)), size=5, hjust=0.5, vjust=-0.5)
  }
  print(plot)
}
#png(out_file_png)
png(out_file_png, type="cairo",units="in",width = 10, height = 7,pointsize=5.2,res=300)
getPCAplot(df,conditionlist,isText=TRUE)

dev.off()
