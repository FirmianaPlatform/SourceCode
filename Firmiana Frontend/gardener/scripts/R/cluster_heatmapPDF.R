library(pheatmap)
Args <- commandArgs()

# /usr/bin/Rscript cluster_heatmap.R tmp/temp-heatmap.txt tmp/test title yellow red pdf
# Args[6]= test.txt  Args[7]= test.png 

input_file = Args[6]
out_file_png   = paste(Args[7],".png",sep="")
out_file_pdf   = paste(Args[7],".pdf",sep="")

title = Args[8]
color1 = Args[9]
color2 = Args[10]
format = Args[11]

#cat(input_file)
matrix=read.csv(input_file,header=T,row.names=1)
#print(matrix)
#colnames(matrix)=c('c1','c2','c3','c4')
#rownames(matrix)=c('r1','r2','r3','r4')

chending_color = colorRampPalette(c(color1, "white", color2))(100)
#print(format)
#{
#    if(format=="pdf"){
#        aa=strsplit(out_file, ".png")
#        out_file = paste(aa[1],".pdf",sep="")
#        #print(out_file)
#        pdf(out_file)
#    }
#    else{ 
#        png(out_file, type="cairo",units="in",width = 5, height = 5,pointsize=5.2,res=300)
#    }
#}
num = nrow(matrix)
myHeight = 10 + trunc(num/300)

pdf(out_file_pdf,width = 10, height = myHeight)
pheatmap(matrix,cluster_rows=T,cluster_cols=T, fontsize=15, fontsize_row=15,col = chending_color,border_color = "white",main = title)
dev.off()