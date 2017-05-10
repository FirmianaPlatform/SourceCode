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

goclusterPlotfunction<-function(plotdata){
	plotdata$Description<-factor(plotdata$Description, levels = plotdata$Description, ordered = TRUE)
	plotdata$diff=c(1:nrow(plotdata))/100
	plotdata$Count=as.numeric(plotdata$Count)
	p=ggplot(plotdata, aes(x=Description, y=Count,fill=diff)) +
	    geom_bar(stat = "identity")+ coord_flip() +
	    theme_bw()+
	    scale_fill_gradientn(colours = rainbow(20))+
	    theme(legend.position="none")+
	    #theme(title = element_text( paste("Organism =", organism,";Ontology =",ont,";Level =",level) ))+
	    theme(axis.text.x = element_text(angle = 0, face="bold",size=13,color="black"))+
	    theme(axis.text.y = element_text(angle = 0, face="bold",size=13,color="black"))+
	    theme(axis.title.y = element_text(size = rel(1.8),angle = 90, face="bold"))+
	    theme(axis.title.x = element_text(size = rel(1.8),angle = 00, face="bold"))
	print(p)
}
	
gMF <- groupGO(gene, organism = organism, ont = ont, level = level, readable=TRUE)
groupGO.summary <- gMF@result #summary(gMF)
groupGO.summary = groupGO.summary[groupGO.summary['Count']>0, ]
write.table(groupGO.summary, file = summaryFile, sep='\t',row.names=FALSE,col.names=TRUE)

num = nrow(groupGO.summary)
myHeight = 10 + trunc(num/20)
print(myHeight)
png(GroupGO_png, type="cairo",units="in",width = 10, height = myHeight,pointsize=5.2,res=300)
plotdata = groupGO.summary[,c(2,3)]
#head( plotdata )
goclusterPlotfunction(plotdata)
#barplot(gMF,drop=T, showCategory=10000)
dev.off()



#kegg <- enrichKEGG(gene = gene, organism = "mouse",readable = TRUE)

