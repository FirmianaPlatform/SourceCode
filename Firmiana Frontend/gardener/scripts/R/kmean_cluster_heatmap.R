library(pheatmap)
Args <- commandArgs(TRUE)

# /usr/bin/Rscript kmean_cluster_heatmap.R test.txt test.png 5
# Args[6]= test.txt  Args[7]= test.png 

input_file = Args[1]
out_file   = Args[2]
out_file_png   = paste(out_file, ".png", sep="")
out_file_pdf   = paste(out_file, ".pdf", sep="")
kmean = Args[3]

c1 = Args[4]
c2 = Args[5]

outfile_kmean = paste(out_file,".kmeanMatrix.txt",sep = "")
title = paste("Clustered Heatmap(K-means=",kmean,")")
#cat(input_file)
dataMatrix=read.csv(input_file,header=T,row.names=1)
km = kmeans(dataMatrix,kmean)


#matrix2 = cbind(dataMatrix,km$cluster)
km.cluster = km$cluster
write(km.cluster,outfile_kmean)

m_col_num = ncol(dataMatrix)
m_row_num = nrow(dataMatrix)

#par(mfrow=c(1,1))
#par(mgp=c(1.6,10,10),mar=c(10,3,2,1))

#dataMatrix.kmcluster = cbind( dataMatrix, t(km.cluster) )
#head(km.cluster)
for(rep_num in 1:kmean){
	flag=0
#	max_area=0
#	for(x in 1:m_row_num){
#  		if(km.cluster[x]==rep_num){
#    		max_area_tmp = max(dataMatrix[x,])
#   			max_area = ifelse(max_area_tmp > max_area,max_area_tmp,max_area)
#  		}
#  		#print(max_area)
#	}
	
	tmpDataMatrix = dataMatrix[ km.cluster == rep_num, ]
	tmpNrow = nrow(tmpDataMatrix)
	max_area = max(  tmpDataMatrix  )
	
	
	kmean_plot_out = paste(out_file,".kmeanCluster_",rep_num,".png",sep = "")
	png(kmean_plot_out, type="cairo",units="in",width = 3, height = 3,pointsize=5.2,res=300)
	
	#kmean_plot_out = paste(out_file,".kmeanCluster_",rep_num,".pdf",sep = "")
	#pdf(kmean_plot_out,width = 4, height = 4)
	
	#png(kmean_plot_out,width=1000,height=1000)
	for(x in 1:tmpNrow){

    		flag = flag+1
    		if(flag==1){
        		plot(panel.first=grid(),type="l",c(1:m_col_num),c(tmpDataMatrix[x,]),xaxt="n",ylab="Area",xlab="",main=paste("K-mean cluster",rep_num),ylim=c(0,max_area))
        		axis(1,labels= colnames(tmpDataMatrix),at=1:m_col_num,las=1)
    		}
    		else{
      			lines(c(1:m_col_num),c(tmpDataMatrix[x,]))
    		}
        	#points(c(1:m_col_num),c(tmpDataMatrix[x,]), pch=1,cex =0.2, col = "dark red")
  		
	}
	dev.off()
	
    flag=0

	kmean_plot_out = paste(out_file,".kmeanCluster_",rep_num,".pdf",sep = "")
	pdf(kmean_plot_out,width = 4, height = 4)
	
    for(x in 1:tmpNrow){

    		flag = flag+1
    		if(flag==1){
        		plot(panel.first=grid(),type="l",c(1:m_col_num),c(tmpDataMatrix[x,]),xaxt="n",ylab="Area",xlab="",main=paste("K-mean cluster",rep_num),ylim=c(0,max_area))
        		axis(1,labels= colnames(tmpDataMatrix),at=1:m_col_num,las=1)
    		}
    		else{
      			lines(c(1:m_col_num),c(tmpDataMatrix[x,]))
    		}
        	#points(c(1:m_col_num),c(tmpDataMatrix[x,]), pch=1,cex =0.2, col = "dark red")
  		
	}
	dev.off()
}


#colnames(dataMatrix)=c('c1','c2','c3','c4')
#rownames(dataMatrix)=c('r1','r2','r3','r4')
#png(out_file)

chending_color = colorRampPalette(c(c1, "white", c2))(50)

png(out_file_png, type="cairo",units="in",width = 5, height = 5,pointsize=5.2,res=300)
pheatmap(km$centers,cluster_rows=0,cluster_cols=0, fontsize=9, fontsize_row=16, col = chending_color, border_color = "white",main =title )
dev.off()

pdf(out_file_pdf,onefile=FALSE)
pheatmap(km$centers,cluster_rows=0,cluster_cols=0, fontsize=9, fontsize_row=16, col = chending_color, border_color = "white",main =title )
dev.off()
