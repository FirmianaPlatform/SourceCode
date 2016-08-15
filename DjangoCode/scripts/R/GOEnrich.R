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
print('gene done')

eMF <- enrichGO(gene, organism = organism, ont = ont, readable=TRUE)
enrichGO.summary = eMF@result # summary(eMF)
write.table(enrichGO.summary, file = summaryFile, append=F, sep='\t',row.names=FALSE,col.names=TRUE)

#head( eMF@result )

num = nrow(enrichGO.summary)
myHeight = 10 + trunc(num/15)
print(myHeight)
png(EnrichGO_png, type="cairo",units="in",width = 10, height = myHeight, pointsize=5.2,res=300)
barplot(eMF, main=paste("Organism =", organism, ";Ontology =", ont), showCategory=10000)
dev.off()

#enrichMap(eMF)

#png(Cnetplot_png, type="cairo",units="in",width = 5, height = 5,pointsize=5.2,res=300)
#cnetplot(eMF, categorySize = "pvalue")
#dev.off()

#pdf(Cnetplot_pdf)
#cnetplot(eMF, categorySize = "pvalue")
#dev.off()
	

#kegg <- enrichKEGG(gene = gene, organism = "mouse",readable = TRUE)

