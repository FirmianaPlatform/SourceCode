library(pheatmap)
Args <- commandArgs(TRUE)

# /usr/bin/Rscript cluster_heatmap.R tmp/temp-heatmap.txt tmp/test title yellow red pdf
# Args[6]= test.txt  Args[7]= test.png 

input_file = Args[1]
out_file_png   = paste(Args[2],".png",sep="")
out_file_pdf   = paste(Args[2],".pdf",sep="")
out_file_txt   = paste(Args[2],".result.txt",sep="")

title = Args[3]
color1 = Args[4]
color2 = Args[5]
format = Args[6]
fontsize = Args[7]
clusterRow = Args[8]
clusterCol = Args[9]

#cat(input_file)
matrix=read.csv(input_file,header=T,row.names=1)
#print(matrix)
#colnames(matrix)=c('c1','c2','c3','c4')
#rownames(matrix)=c('r1','r2','r3','r4')

chending_color = colorRampPalette(c(color1, "white", color2))(100)
#print(format)
#print(out_file_png)


paint <- function()
{	
	#border_color = "white",display_numbers = F,number_format ="%.1e",cellwidth = 15, cellheight = 12, fontsize=15, ,filename = fname
	result=pheatmap(matrix,cluster_rows=clusterRow,cluster_cols=clusterCol, fontsize_row=fontsize,border_color = "white",col = chending_color,main = title)
	write.table(matrix[result$tree_row$order,result$tree_col$order],sep='\t',file=out_file_txt)
	axis(side=3)
	dev.off()
}

num = nrow(matrix)
myHeight = 10 + trunc(num/50)
if(myHeight>30) myHeight=30
{
    if(format=="pdf"){
        pdf(out_file_pdf,width = 10, height = 300)
        #fname = out_file_pdf
    }else{ 
        png(out_file_png, type="cairo",units="in",width = 10, height = myHeight,pointsize=5.2,res=300)
        #fname = out_file_png
    }
}

paint()


