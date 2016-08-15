## GO(input, species, organism, ont, level, output_name )

Args <- commandArgs(TRUE)
inputGeneListFile = Args[1]
organism = Args[2] # "mouse"
ont = Args[3] # MF CC BP
level = as.numeric(Args[4])
summaryFile  = paste(Args[5],"Summary.txt",sep="")

GroupGO_png  = paste(Args[5],".png",sep="")
GroupGO_pdf  = paste(Args[5],".pdf",sep="")

EnrichGO_png = paste(Args[5],".png",sep="")
EnrichGO_pdf = paste(Args[5],".pdf",sep="")

Cnetplot_png = paste(Args[5],"Cnetplot.png",sep="")
Cnetplot_pdf = paste(Args[5],"Cnetplot.pdf",sep="")

type = Args[6]

library('ggplot2')
library('clusterProfiler')
{
	if(organism == 'human'){
		print(organism)
		library('org.Hs.eg.db')
		xx <- as.list(org.Hs.egALIAS2EG)
	}
	else if(organism == 'mouse'){
		print(organism)
		library('org.Mm.eg.db')
		xx <- as.list(org.Mm.egALIAS2EG)
	}
	
}
xx <- xx[!is.na(xx)]
A4<- read.table(inputGeneListFile, header=F, quote="\"")
A4List<-xx[unlist(A4)]
gene=c()
for (i in 1:nrow(A4))
{
  gene=append(gene,(A4List[[i]]))
}

goclusterPlotfunction<-function(x){
	#if(nrow(x)>200) {x = x[c(1:200),]}
	#x$Count<-factor(x$Count, levels = x$Count, ordered =T)
	#x$diff=c(1:nrow(x))/100
	
	p <- ggplot(x, aes(x=Description, y=Count)) + 
	    geom_bar(stat = "identity",color="black",fill="white")+ 
	    coord_flip() +
	    theme_bw()+
	    geom_text(label=x$Count, size=3, hjust= -.1) +
	    #scale_fill_gradientn(colours = rainbow(20))+
	    theme(legend.position="none")+
	    #theme(title = element_text( paste("Organism =", organism,";Ontology =",ont,";Level =",level) ))+
	    theme(axis.text.x = element_text(angle = 90, face="bold",size=10,color="black"))+
	    theme(axis.text.y = element_text(angle = 0, face="bold",size=12,color="black"))+
	    theme(axis.title.y = element_text(size = rel(1.8),angle = 90, face="bold"))+
	    theme(axis.title.x = element_text(size = rel(1.8),angle = 00, face="bold"))
	print(p)
}
	
if(type=='GOClassification')
{
	gMF <- groupGO(gene, organism = organism, ont = ont, level = level, readable=TRUE)
	groupGO.summary <- gMF@result #summary(gMF)
	groupGO.summary = groupGO.summary[groupGO.summary['Count']>0, ]
	write.table(groupGO.summary, file = summaryFile, sep='\t',row.names=FALSE,col.names=TRUE,quote=FALSE)
	
	num = nrow(groupGO.summary)
	myHeight = 10 + trunc(num/20)
	print(myHeight)
	
	plotdata = groupGO.summary[,c(2,3)]
	plotdata = plotdata[order(plotdata[,1]),]
	
	png(GroupGO_png, type="cairo",units="in",width = 10, height = myHeight,pointsize=5.2,res=300)
	goclusterPlotfunction(plotdata)
	#barplot(gMF,drop=T, showCategory=10000)
	dev.off()
	
	pdf(GroupGO_pdf,width = 10, height = myHeight)
	goclusterPlotfunction(plotdata)
	dev.off()
	
}else{
	eMF <- enrichGO(gene, organism = organism, ont = ont, readable=TRUE)
	enrichGO.summary <- eMF@result # summary(eMF)
	
	plotdata.unsort <- enrichGO.summary
	
	plotdata.unsort$pvalue<-as.numeric(plotdata.unsort$pvalue)
	#plotdata <- plotdata.unsort 
	plotdata <- plotdata.unsort[order(plotdata.unsort$pvalue),]
	
	write.table(plotdata, file = summaryFile, append=F, sep='\t',row.names=FALSE,col.names=TRUE,quote=FALSE)
	
	num = nrow(enrichGO.summary)
	myHeight = 30 #+ trunc(num/15)
	print(myHeight)

	#plotdata <- plotdata[order(plotdata[,4]),]
	
	png(EnrichGO_png, type="cairo",units="in",width = 10, height = myHeight, pointsize=5.2,res=300)
	#plotdata <- plotdata[,c(2,9)]
	goclusterPlotfunction(plotdata)
	#barplot(eMF, main=paste("Organism =", organism, ";Ontology =", ont), showCategory=10000)
	dev.off()
	
	pdf(EnrichGO_pdf,width = 10, height = myHeight)
	goclusterPlotfunction(plotdata)
	dev.off()
	
	#enrichMap(eMF)
	
	#png(Cnetplot_png, type="cairo",units="in",width = 5, height = 5,pointsize=5.2,res=300)
	#cnetplot(eMF, categorySize = "pvalue")
	#dev.off()
	
	#pdf(Cnetplot_pdf)
	#cnetplot(eMF, categorySize = "pvalue")
	#dev.off()
}


#kegg <- enrichKEGG(gene = gene, organism = "mouse",readable = TRUE)

