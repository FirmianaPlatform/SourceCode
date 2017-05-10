library(pheatmap)
Args <- commandArgs(TRUE)

# /usr/bin/Rscript non_cluster_heatmap.R tmp/test.txt tmp/test.png title '#FF0000' '#0000FF'
# Args[6]= test.txt  Args[7]= test.png 

input_file = Args[1]
out_file   = Args[2]

out_file_png   = paste(Args[2],".png",sep="")
out_file_pdf   = paste(Args[2],".pdf",sep="")

title = Args[3]
color1 = Args[4]
color2 = Args[5]

#cat(input_file)
matrix=read.csv(input_file,header=T,row.names=1)
#print(matrix)
#colnames(matrix)=c('c1','c2','c3','c4')
#rownames(matrix)=c('r1','r2','r3','r4')

#chending_color = colorRampPalette(c( "white","white","white","white", color2))(10)
mid_color <- colorRampPalette(c("white", color2))(3)[2]
chending_color = c(colorRampPalette(c( "white",mid_color))(40),colorRampPalette(c( mid_color,color2))(10))
breaks=unique(seq(0,1,length=50))

png(out_file_png, type="cairo",units="in",width = 5, height = 5, pointsize=5.2,res=300)
#breaks=breaks,
pheatmap(matrix,cluster_rows=0,cluster_cols=0, fontsize=9, col=chending_color, fontsize_row=6,border_color = "white",main = title,breaks=breaks,display_numbers = TRUE)
dev.off()

#color.map <- function(mol.biol) { if (mol.biol=="ALL1/AF4") 1 else 2 } 

#patientcolors=c(1,1,2,2,3,3,4,4,4,5,5)
#annotation<-data.frame(Var1=factor(patientcolors,labels=c("Eye","Skin","Lung","Thyroid","Testicle")))
#print(annotation)
pdf(out_file_pdf,width=10,height=10)
pheatmap(matrix,cluster_rows=0,cluster_cols=0, fontsize=9, col=chending_color, fontsize_row=6,border_color = "white",main = title,breaks=breaks,display_numbers = TRUE)
#,annotation = annotation)
dev.off()
