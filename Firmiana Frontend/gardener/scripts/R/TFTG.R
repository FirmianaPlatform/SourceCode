#########enrichment1,3-6,10############
#setwd('D:\\firmiana\\R\\TFTG\\')

Args <- commandArgs(TRUE)

inputDataFile = Args[1]
#inputDataFile = '/usr/local/firmiana/leafy/gardener/scripts/R/TFTG/ifot_coculture_secretome_lg_extracellular.txt' #Args[1]

inputTFTGFile = '/usr/local/firmiana/leafy/gardener/scripts/R/TFTG/TF_TG-Hnf1a.txt' #Args[2] # TF_TG-Hnf1a.txt
#inputTFTGFile = Args[2]

#outFileDesc = paste("/usr/local/firmiana/leafy/gardener/scripts/R/TFTG/TF", "_linear_decreasing.txt", sep="")
#outFileAsc  = paste("/usr/local/firmiana/leafy/gardener/scripts/R/TFTG/TF", "_linear_increasing.txt", sep="")
outFileDesc = paste(Args[3],"_Desc.txt",sep="")
outFileAsc  = paste(Args[3],"_Asc.txt",sep="")

out_file_png  = paste(Args[3],".png",sep="")
out_file_pdf  = paste(Args[3],".pdf",sep="")
#out_file_png = '/usr/local/firmiana/leafy/gardener/scripts/R/TFTG/volc.png'

colnumber = c(1,2,3,4,5,6,7,8)
fileName = c("HC-HC")
  
data = read.table(inputDataFile,header=T,sep="\t",stringsAsFactors=FALSE)
data2 = as.matrix(data[,-1])

TFTG = readLines( inputTFTGFile )

Func <- function(type){


    data3 = data2 #[,c(colnumber[4*k-3]:colnumber[4*k])]
    #rr = which((data3[,1]>0)|(data3[,2]>0)|(data3[,3]>0)|(data3[,4]>0))
    rr = which((data3[,1]>0)|(data3[,2]>0))
    if(type=='DESC'){
      #derr = which((data3[,2]-data3[,1]< 0)&(data3[,3]-data3[,2]< 0)&(data3[,4]-data3[,3]< 0))
      derr = which((data3[,2]-data3[,1]< 0))
    }else{
    #derr = which((data3[,2]-data3[,1]> 0)&(data3[,3]-data3[,2]> 0)&(data3[,4]-data3[,3]> 0))
      derr = which((data3[,2]-data3[,1]> 0))
    }
    
    
    TGs = c()
    for(i in 1:length(TFTG))
    {
      str = unlist(strsplit(TFTG[i],"\t"))
      TGs = union(TGs,str[-1])
    }

    deGenes    = intersect(as.character(data[derr,1]),TGs)
    totalGenes = intersect(as.character(data[rr,1]),TGs)
    
    a1 = length(totalGenes)
    a2 = length(deGenes)
    
    b1 = c()
    b2 = c()
    pval = c()
    ratio = c()
    TFName = c()
    b1set = c()
    b2set = c()
    for(i in 1:length(TFTG))
    {
      str = unlist(strsplit(TFTG[i],"\t"))
      
      TFName[i] = str[1]
      b1[i]     = length(intersect(totalGenes,str[-1]))
      b1set[i]  = paste(intersect(totalGenes,str[-1]),collapse=",")
      b2[i]     = length(intersect(deGenes,str[-1]))
      b2set[i]  = paste(intersect(deGenes,str[-1]),collapse=",")
      pval[i]   = fisher.test(cbind(c(a1-a2,a2),c(b1[i]-b2[i],b2[i])))$p.value
      
      if(b2[i]<b1[i]){ratio[i] = b2[i]/(b1[i]-b2[i])/(a2/(a1-a2))}else{ratio[i]=100}
    }
    res = cbind(TFName,a1)
    res = cbind(res,a2)
    res = cbind(res,b1)
    res = cbind(res,b1set)
    res = cbind(res,b2)
    res = cbind(res,b2set)
    res = cbind(res,ratio)
    res = cbind(res,pval)
    colnames(res) = c("TF","len(totalGenes)","len(deGenes)","B1","B1Gene","B2","B2Gene","Ratio","Pval")
    
    if(type=='DESC'){
      outFile = outFileDesc
    }else{
      outFile = outFileAsc 
    }
    write.table(res,outFile,row.names=FALSE,sep="\t",quote=FALSE)
  	print(outFile)
}


Func('DESC')
Func('ASC')

########volcano plot##########
#par(mfrow=c(1,1))
HCactivator = c("Nr5a2","Sod2","Nr1h4","Gzf1","Hnf4a","Prox1","Foxa2","Irf6","Ptges2","Lrpprc","Phb","Foxa3","Hlf","Hnf1a","Srebf1")
## Highlight genes that have an absolute fold change > 2 and a p-value < Bonferroni cut-off

data <- read.table(outFileDesc,header=TRUE,sep="\t")

r1 = which((data[,8]==100)&(data[,9]==1))
r2 = which(data[,8]<=1)
r3 = union(r1,r2)
a = data[-r3,]
a[which(a[,8]==100),8]=31
rr = match(HCactivator,a[,1])
subRR = rr[!is.na(rr)]
rrs = which(-log10(a[subRR,9])> -log10(0.05))
subRRin = subRR[rrs]

data <- read.table(outFileAsc,header=TRUE,sep="\t")

r4 = which((data[,8]==100)&(data[,9]==1))
r5 = which(data[,8]<=1)
r6 = union(r4,r5)
b = data[-r6,]
b[which(b[,8]==100),8]=31
rr2 = match(HCactivator,b[,1])
subRR2 = rr2[!is.na(rr2)]
rr2s = which(-log10(b[subRR2,9])> -log10(0.05))
subRR2in = subRR2[rr2s]

print( out_file_png )


Paint <- function(){
  LOG10_005 = log10(0.05)
  LOG10_001 = log10(0.01)
  LOG2_2 = log2(2)
  LOG2_15= log2(1.5)
  
	plot(log2(b[,8]),-log10(b[,9]),pch="+",cex=0.5,xlab="log2 (Ratio)",ylab="-log10 (P Value)",main=' Volcano Plot',xlim=c(-5,5),ylim=c(0,10))
	axis(side=1, at=-5:5)
	
	points(log2(b[subRR2in,8]),-log10(b[subRR2in,9]),pch=16,col='red',cex=0.7)
	
	if(nrow(b[subRR2in,])>0) {text(log2(b[subRR2in,8]),-log10(b[subRR2in,9]),labels=b[subRR2in,1],col="red",cex=0.7,pos=3)}
	
	points(-log2(a[,8]),-log10(a[,9]),pch="+",cex=0.5)
	points(-log2(a[subRRin,8]),-log10(a[subRRin,9]),pch=16,col='blue',cex=0.7)

  
	  abline(h=-LOG10_001, text(0,-LOG10_001 ,labels="Pvalue = 0.01", adj = c(0.5, -.2)),col="grey")
	  abline(h=-LOG10_005, text(0,-LOG10_005 ,labels="Pvalue = 0.05", adj = c(0.5, -.2)),col="grey")
	  abline(v=LOG2_15, col="grey")
	  abline(v=-LOG2_15, col="grey")


	if(nrow(a[subRRin,])>0) {text(-log2(a[subRRin,8]),-log10(a[subRRin,9]),labels=a[subRRin,1],col="blue",cex=0.7,pos=3)}

	legend(-4.8,9.8,
       c('enriched in increasing genes (Pvalue<0.05,Ratio>1.5)','enriched in decreasing genes (Pvalue<0.05,Ratio>1.5)','others'),
       pch=c(16,16,16),col=c('red','blue','black'),cex=1)
}

png(out_file_png, type="cairo",units="in",width = 5, height = 5, pointsize=5.2,res=300)
Paint()
dev.off()

pdf(out_file_pdf)
Paint()
dev.off()