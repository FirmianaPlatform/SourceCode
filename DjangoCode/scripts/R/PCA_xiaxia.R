# pca(input, input_metadata, output_pc, output_name)
library(ggplot2)
library(reshape2)
library(RColorBrewer)
library(scales)
library(grid)

Args <- commandArgs(TRUE)
input_file = Args[1]
sampleInfo_file = Args[2]
cor_matrix_file = paste(Args[3],"_cor_matrix.txt",sep="")
out_file_png    = paste(Args[3],".png",sep="")
out_file_pdf    = paste(Args[3],".pdf",sep="")

plotDim1 = unlist(strsplit(Args[4],","))[1]
plotDim2 = unlist(strsplit(Args[4],","))[2]

metaList = Args[5]

data = read.table(input_file,header=T,stringsAsFactors=FALSE,sep="\t")
k3.cv=as.matrix(data[,-1])
ncol_data = ncol(k3.cv)
nrow_data = nrow(k3.cv)

k3.cv.t=t(k3.cv) #转置数据
k3.mat=as.numeric(k3.cv.t)#提取54个样本的数据
k3.mat=matrix(k3.mat,ncol_data,nrow_data)#将数据转换成矩阵格式
k3.mat.pr=prcomp(na.omit(k3.mat),cor=TRUE)#PCA分析
k3.mat.predict=predict(k3.mat.pr)#计算每一component的值


#print(dim(k3.mat))

sampleInfo = read.table(sampleInfo_file,header=T,sep="\t")
#rr = which(is.na(sampleInfo[,14])==1)
#sampleInfo = sampleInfo[1:ncol_data,]
# 'expName', 'condition','species', 'instrument', 'dateOfExperiment', 'dateOfOperation', 'method','separation','sex','age','reagent','sample','tissueType','strain'

condition = sampleInfo[,2]
species = sampleInfo[,3]
instrument = sampleInfo[,4]
dateOfExperiment = sampleInfo[,5]
dateOfOperation = sampleInfo[,6]
method = sampleInfo[,7]
separation = sampleInfo[,8]
sex = sampleInfo[,9]
age = sampleInfo[,10]
reagent = sampleInfo[,11]
sample = sampleInfo[,12]
tissueType = sampleInfo[,13]
strain = sampleInfo[,14]
circ_time = sampleInfo[,15]

attr = cbind(species,instrument)
attr = cbind(attr,dateOfExperiment)
attr = cbind(attr,dateOfOperation)
attr = cbind(attr,method)
attr = cbind(attr,separation)
attr = cbind(attr,sex)
attr = cbind(attr,age)
attr = cbind(attr,reagent)
attr = cbind(attr,sample)
attr = cbind(attr,tissueType)
attr = cbind(attr,strain)
attr = cbind(attr,circ_time)

#print(attr[,c('instrument','dateOfExp')])

{

	if(metaList!="")
	{
		metadataList = unlist(strsplit(metaList,";"))
		attr = attr[,metadataList]
		
		#print(dim(attr))
		
		#print( dim(k3.mat.predict))
		cor_matrix = cor(k3.mat.predict,attr)
		#           sample        tumor   DateOfExp   instrument      method         sex         age        site  DateOfOper ClinicalClass    inhibitor
		#PC1   0.074509628 -0.035047705 -0.37709218  0.165326874 -0.86435817  0.36726627  0.03463263 -0.01107650 -0.04585038    0.10308617 -0.596978847
		#PC2  -0.236897110 -0.007299681  0.23719608 -0.755307405 -0.21648206  0.10639867  0.12788737 -0.36519250 -0.06236640   -0.37076565 -0.002754285
		#PC3   0.382970716 -0.005794235  0.60461772 -0.278931773  0.03713179  0.17203998 -0.16372571 -0.06137580  0.06437130    0.19989294  0.529430139
		#PC4  -0.129116103  0.062542666 -0.43483494  0.274197909 -0.33144186  0.08893719  0.26186949 -0.13125801 -0.33902436    0.19234538 -0.307325664
		
		colnames(cor_matrix)[1] = paste("\t",colnames(cor_matrix)[1],sep = "")
		write.table(cor_matrix, cor_matrix_file, sep="\t", quote=FALSE)

	}
	else
	{
		write.table('No Correlation Matrix .', cor_matrix_file, sep="\t", quote=FALSE)
	}
}

#k3.mat.predict.2d = cbind(k3.mat.predict, attr)
 k3.mat.predict.2d = k3.mat.predict
 

tissues = sampleInfo[,1]

pc1 = k3.mat.predict[,plotDim1]
pc2 = k3.mat.predict[,plotDim2]

maxX=max(pc1)*2.2
maxY=max(pc2)*2
plotdata <- data.frame(Samples=tissues,Conditions=condition,pc1,pc2) 
plotdata$Samples <- factor(plotdata$Samples)
plot <- ggplot(plotdata, aes(pc1,pc2),environment = environment()) + 
    geom_point(aes(colour = Conditions,shape=Conditions),size = 5) + 
    geom_text( x = pc1, y = pc2, label = tissues,size = 3,hjust=-.1)+
    theme(panel.border = element_rect(linetype = "dashed")) + 
    theme_bw() +
    ylim(-maxY,maxY)+
    xlim(-maxX,maxX)+
    scale_x_continuous(plotDim1,limits=c(-maxX,maxX))+
    scale_y_continuous(plotDim2,limits=c(-maxY,maxY))+
    theme(legend.text = element_text(colour="blue", size =12)) + 
    theme(legend.justification=c(1,0),legend.position="right")+
    theme(legend.title = element_text(colour="black", size=12))+
    theme(legend.key=element_rect(colour='white',fill='white',size=0.5,linetype='dashed')) + 
    #theme(legend.key.linetype='dash') + 
    
    scale_fill_brewer(palette="Spectral")


png(out_file_png, type="cairo",units="in",width = 10, height = 7,pointsize=5.2,res=300)

print(plot)
  
xlimit = c(floor(min(pc1)*1.2),ceiling(max(pc1)*1.2))
ylimit = c(floor(min(pc2)*1.2),ceiling(max(pc2)*1.2))

#plot(panel.first=grid(), pc1, pc2, xlab=plotDim1, ylab=plotDim2, xlim = xlimit,ylim = ylimit)#, axes=FALSE)
#axis(1,at=seq(floor(min(pc1)-1),ceiling(max(pc1)+10),by=20),lwd=2)
#axis(2,at=seq(floor(min(pc2)-1),ceiling(max(pc2)+10),by=20),lwd=2)

#points( pc1, pc2, pch=20, col='blue4',cex=4)
#print(pc1)
#text(pc1, pc2,labels=tissues,col="black",cex=1.5,pos=3)

dev.off()


pdf(out_file_pdf, width = 8, height = 6)

print(plot)

dev.off()